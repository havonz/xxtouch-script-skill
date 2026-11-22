#!/usr/bin/env python3
"""List models, fetch weights, or generate a device downloader."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import tempfile
import urllib.request
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import urlsplit

from ensure_config_ignores import append_missing, ensure_array, load_config, normalize_ignore_entry, write_config
from install_modules import SKILL_ROOT, load_manifest


CATALOG_PATH = SKILL_ROOT / "assets" / "models" / "catalog.json"


def load_catalog(extra: Path | None = None) -> dict[str, Any]:
    models: dict[str, Any] = {}
    modules = load_manifest()["modules"]
    for path in [CATALOG_PATH] + ([extra] if extra else []):
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or data.get("schema_version") != 1 or not isinstance(data.get("models"), dict):
            raise ValueError(f"不支持的模型清单格式：{path}")
        for model_id, model in data["models"].items():
            if not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", model_id) or model_id in models:
                raise ValueError(f"无效或重复的模型标识：{model_id}")
            if not isinstance(model, dict):
                raise ValueError(f"模型 {model_id} 必须为对象")
            if model.get("module") not in modules:
                raise ValueError(f"模型 {model_id} 指向未知模块")
            if model.get("status") not in {"downloadable", "needs-model"}:
                raise ValueError(f"模型 {model_id} 的状态无效")
            files = model.get("files", [])
            if not isinstance(files, list) or (model["status"] == "downloadable" and not files):
                raise ValueError(f"模型 {model_id} 缺少配套文件清单")
            if not model.get("source") or not model.get("revision"):
                raise ValueError(f"模型 {model_id} 缺少来源或固定版本")
            seen: set[str] = set()
            for entry in files:
                if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
                    raise ValueError(f"模型 {model_id} 的文件条目需要字符串 path")
                filename = entry.get("path", "")
                parts = filename.split("/")
                if (not re.fullmatch(r"[A-Za-z0-9_./-]+", filename)
                        or any(part in {"", ".", ".."} for part in parts)):
                    raise ValueError(f"不安全的模型文件路径：{filename}")
                # 同一清单需要在大小写不敏感的文件系统上也保持一致。
                normalized = filename.casefold()
                if any(normalized == p or normalized.startswith(p + "/") or p.startswith(normalized + "/") for p in seen):
                    raise ValueError(f"模型文件路径冲突：{filename}")
                seen.add(normalized)
                url = entry.get("url", "")
                if not isinstance(url, str):
                    raise ValueError(f"模型 {model_id} 的下载地址必须为字符串")
                parsed = urlsplit(url)
                if (parsed.scheme not in {"https", "http"} or not parsed.hostname
                        or parsed.username or parsed.password or any(ord(c) < 32 for c in url)):
                    raise ValueError(f"模型 {model_id} 需要有效的 HTTP(S) 下载地址")
                if type(entry.get("size")) is not int or entry["size"] <= 0:
                    raise ValueError(f"模型 {model_id} 缺少有效文件大小：{filename}")
                if not isinstance(entry.get("sha256"), str) or not re.fullmatch(r"[0-9a-f]{64}", entry["sha256"]):
                    raise ValueError(f"模型 {model_id} 缺少 SHA256：{filename}")
            models[model_id] = model
    return models


def verified_file(path: Path, entry: dict[str, Any]) -> bool:
    if not path.is_file() or path.stat().st_size != entry["size"]:
        return False
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest() == entry["sha256"]


def fetch_model(root: Path, model_id: str, model: dict[str, Any], timeout: float = 120) -> dict[str, Any]:
    root = root.resolve()
    config_path = root / ".config"
    config = load_config(config_path)
    ignores = config.get("ignores", [])
    if ignores is None:
        ignores = []
    if not isinstance(ignores, list):
        raise ValueError(".config.ignores 必须为数组")
    model_root = root / "res" / "models" / model_id
    targets = [(entry, model_root.joinpath(*PurePosixPath(entry["path"]).parts)) for entry in model["files"]]
    for entry, target in targets:
        if target.resolve() != target or target.is_symlink():
            raise ValueError(f"模型目标位于项目之外或为符号链接：{target}")
        if target.exists() and not target.is_file():
            raise ValueError(f"模型文件目标被目录占用：{target}")
        for ignored in ignores:
            if not isinstance(ignored, str):
                continue
            normalized = normalize_ignore_entry(ignored)
            relative = target.relative_to(root).as_posix()
            if normalized and (relative == normalized or relative.startswith(normalized + "/")):
                raise ValueError(f"模型被 .config.ignores 排除，开发时无法传输：{ignored}；请先调整该配置")

    added = append_missing(ensure_array(config, "buildIgnores"), ["/res/models"])
    if added:
        write_config(config_path, config)
    result: dict[str, Any] = {"model": model_id, "directory": str(model_root), "buildIgnoresAdded": added, "files": []}
    for entry, target in targets:
        if verified_file(target, entry):
            result["files"].append({"path": entry["path"], "action": "cached"})
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temporary = tempfile.mkstemp(prefix=target.name + ".", suffix=".part", dir=target.parent)
        partial = Path(temporary)
        try:
            request = urllib.request.Request(entry["url"], headers={"User-Agent": "XXTouch-Skill-Models/1"})
            with os.fdopen(descriptor, "wb") as output, urllib.request.urlopen(request, timeout=timeout) as response:
                if response.status != 200:
                    raise ValueError(f"模型下载失败 HTTP {response.status}：{entry['path']}")
                received = 0
                for chunk in iter(lambda: response.read(1024 * 1024), b""):
                    received += len(chunk)
                    if received > entry["size"]:
                        raise ValueError(f"模型大小超过清单记录：{entry['path']}")
                    output.write(chunk)
            if not verified_file(partial, entry):
                raise ValueError(f"模型大小或 SHA256 校验失败：{entry['path']}")
            partial.replace(target)
            result["files"].append({"path": entry["path"], "action": "downloaded"})
        finally:
            partial.unlink(missing_ok=True)
    result["constructorOptions"] = model.get("constructor_options", {})
    return result


def emit_lua(model_id: str, model: dict[str, Any], timeout: float = 120) -> str:
    template = (SKILL_ROOT / "assets" / "templates" / "download_model.lua").read_text(encoding="utf-8")
    # URL 和路径已通过清单校验；保留 Unicode，避免生成 Lua 不支持的 JSON \u 转义。
    entries = []
    for entry in model["files"]:
        values = ", ".join(f"{key} = {json.dumps(entry[key], ensure_ascii=False)}" for key in ("path", "url", "size", "sha256"))
        entries.append("    {" + values + "},")
    return (template.replace("@@MODEL_ID@@", model_id)
            .replace("@@FILES@@", "\n".join(entries)).replace("@@TIMEOUT@@", str(timeout)))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest="command", required=True)
    listing = subcommands.add_parser("list", help="List model metadata")
    listing.add_argument("--module")
    listing.add_argument("--model", help="Show full metadata for one model")
    fetch = subcommands.add_parser("fetch", help="Download weights and update buildIgnores only")
    fetch.add_argument("project_root", type=Path)
    fetch.add_argument("model")
    emit = subcommands.add_parser("emit-lua", help="Emit a standalone Lua downloader")
    emit.add_argument("model")
    emit.add_argument("--output", type=Path, help="Output file (default: stdout); conflicting files are preserved")
    for command in (listing, fetch, emit):
        command.add_argument("--catalog", type=Path, help="Additional model catalog with unique IDs")
    for command in (fetch, emit):
        command.add_argument("--timeout", type=float, default=120, help="Timeout in seconds per download")
    args = parser.parse_args()
    models = load_catalog(args.catalog)
    if args.command == "list":
        if args.module and args.module not in load_manifest()["modules"]:
            raise ValueError(f"未知模块：{args.module}")
        if args.model:
            if args.model not in models:
                raise ValueError(f"未知模型：{args.model}")
            output = {args.model: models[args.model]}
        else:
            output = [{"id": model_id, "module": model["module"], "status": model["status"],
                       "description": model.get("description", ""), "bytes": sum(f["size"] for f in model.get("files", [])),
                       "reason": model.get("reason")} for model_id, model in models.items()
                      if not args.module or model["module"] == args.module]
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return
    if not math.isfinite(args.timeout) or args.timeout <= 0:
        raise ValueError("下载超时必须是正数")
    if args.model not in models:
        raise ValueError(f"未知模型：{args.model}；先运行 list 查询")
    model = models[args.model]
    if model["status"] != "downloadable":
        raise ValueError(model.get("reason", "需要开发者提供匹配的模型及下载清单"))
    if args.command == "fetch":
        print(json.dumps(fetch_model(args.project_root, args.model, model, args.timeout), ensure_ascii=False, indent=2))
    else:
        source = emit_lua(args.model, model, args.timeout)
        if args.output:
            if args.output.exists():
                if not args.output.is_file() or args.output.read_text(encoding="utf-8") != source:
                    raise ValueError(f"输出文件已存在且内容不同：{args.output}")
            else:
                args.output.parent.mkdir(parents=True, exist_ok=True)
                with args.output.open("x", encoding="utf-8") as output:
                    output.write(source)
        else:
            print(source, end="")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from None
