#!/usr/bin/env python3
"""Install bundled Lua modules and dependencies (default: preview)."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from install_xxtdo import detect_project_type


SKILL_ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = SKILL_ROOT / "assets" / "frameworks"


def load_manifest() -> dict[str, Any]:
    manifest = json.loads((ASSET_ROOT / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("schema_version") != 1 or not isinstance(manifest.get("modules"), dict):
        raise ValueError("不支持的模块清单格式")
    for name, item in manifest["modules"].items():
        if not re.fullmatch(r"[a-z][a-z0-9_]*", name) or item.get("file") != name + ".lua":
            raise ValueError(f"无效模块文件名：{name}")
        if not isinstance(item.get("dependencies"), list):
            raise ValueError(f"无效模块依赖：{name}")
        if not re.fullmatch(r"[0-9a-f]{64}", item.get("sha256", "")):
            raise ValueError(f"无效模块校验值：{name}")
    return manifest


def resolve_modules(modules: dict[str, Any], requested: list[str]) -> list[str]:
    resolved: list[str] = []
    visiting: set[str] = set()

    def visit(name: str) -> None:
        if name not in modules:
            raise ValueError(f"未知模块：{name}")
        if name in visiting:
            raise ValueError(f"模块依赖形成循环：{name}")
        if name in resolved:
            return
        visiting.add(name)
        for dependency in modules[name]["dependencies"]:
            visit(dependency)
        visiting.remove(name)
        resolved.append(name)

    for name in requested:
        visit(name)
    return resolved


def install_modules(root: Path, requested: list[str], project_type: str | None = None,
                    apply: bool = False) -> dict[str, Any]:
    root = root.resolve()
    if not root.is_dir():
        raise ValueError(f"项目目录不存在：{root}")
    project_type = detect_project_type(root, project_type)
    modules = load_manifest()["modules"]
    names = resolve_modules(modules, requested)
    directories = [root] if project_type == "xpp" else [root / "lua", root / "lua" / "scripts"]
    files: list[dict[str, Any]] = []
    contents: dict[str, bytes] = {}

    for name in names:
        item = modules[name]
        data = (ASSET_ROOT / item["file"]).read_bytes()
        if hashlib.sha256(data).hexdigest() != item["sha256"]:
            raise ValueError(f"Skill 源码快照校验失败：{name}")
        contents[name] = data
        candidates = [directory / (name + suffix) for directory in directories for suffix in (".lua", ".xxt")]
        existing = [path for path in candidates if path.exists() or path.is_symlink()]
        target = existing[0] if len(existing) == 1 else directories[0] / item["file"]
        conflict = None
        if len(existing) > 1:
            conflict = "存在多个同名模块，请先统一 require 路径"
        elif target.resolve() != target or target.is_symlink():
            conflict = "目标为符号链接或位于项目目录之外"
        elif existing and (not target.is_file() or target.suffix != ".lua" or target.read_bytes() != data):
            conflict = "已有模块与快照不同，请先比较并决定保留哪个版本"
        files.append({
            "module": name, "target": str(target),
            "action": "conflict" if conflict else "unchanged" if existing else "copy",
            "conflict": conflict, "reference": item["reference"],
        })

    summary = {
        "projectRoot": str(root), "projectType": project_type, "dryRun": not apply,
        "files": files, "conflicts": [item for item in files if item["conflict"]],
        "runtimeModules": sorted({dependency for name in names for dependency in modules[name]["runtime_modules"]}),
        "changed": False,
    }
    # 先检查完整依赖集合，避免发现冲突时已经拷入半套模块。
    if apply and not summary["conflicts"]:
        for item in files:
            if item["action"] == "copy":
                target = Path(item["target"])
                target.parent.mkdir(parents=True, exist_ok=True)
                with target.open("xb") as output:
                    output.write(contents[item["module"]])
                summary["changed"] = True
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", type=Path)
    parser.add_argument("modules", nargs="+")
    parser.add_argument("--type", choices=("xxt", "xpp"))
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    summary = install_modules(args.project_root, args.modules, args.type, args.apply)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if summary["conflicts"]:
        raise SystemExit(1)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from None
