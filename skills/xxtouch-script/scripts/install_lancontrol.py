#!/usr/bin/env python3
"""Install XXTLanControl.lua from the target controller."""

from __future__ import annotations

import argparse
import os
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from install_xxtdo import detect_project_type
from xxtouch_assist_common import print_json


def install_lancontrol(project_root: Path, backend_url: str, *, project_type: str | None = None,
                       apply: bool = False, force: bool = False) -> dict[str, Any]:
    root = project_root.expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"项目目录不存在：{root}")
    project_type = detect_project_type(root, project_type)
    parsed = urllib.parse.urlsplit(backend_url.strip())
    if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.query or parsed.fragment or parsed.username or parsed.password:
        raise ValueError("中控地址必须是无凭据、查询参数和片段的 HTTP/HTTPS 基础地址")
    if parsed.path.rstrip("/").endswith("/mcp"):
        raise ValueError("请传中控基础地址，不要包含 /mcp")
    url = urllib.parse.urlunsplit(parsed).rstrip("/") + "/api/down/XXTLanControl.lua"
    directories = [root] if project_type == "xpp" else [root / "lua" / "scripts", root / "lua"]
    candidates = [directory / ("XXTLanControl" + suffix) for directory in directories for suffix in (".lua", ".xxt")]
    existing = [filename for filename in candidates if filename.exists() or filename.is_symlink()]
    if len(existing) > 1 or any(filename.suffix == ".xxt" for filename in existing):
        raise ValueError("发现重复或加密的 XXTLanControl 模块，请先确认并整理现有副本")
    target = existing[0] if existing else directories[0] / "XXTLanControl.lua"
    if target.is_symlink() or not target.resolve().is_relative_to(root):
        raise ValueError("模块目标不能是符号链接或位于项目目录之外")
    if target.exists() and not target.is_file():
        raise ValueError(f"模块目标不是文件：{target}")
    summary: dict[str, Any] = {
        "projectRoot": str(root), "projectType": project_type, "downloadUrl": url,
        "target": str(target), "exists": target.exists(), "dryRun": not apply, "changed": False,
    }
    if not apply:
        return summary
    request = urllib.request.Request(url, headers={"Accept": "application/octet-stream"})
    with urllib.request.urlopen(request, timeout=30) as response:
        data = response.read(2 * 1024 * 1024 + 1)
    if len(data) > 2 * 1024 * 1024:
        raise ValueError("模块下载内容过大")
    text = data.decode("utf-8")
    if "function XXTLanControl.connect(" not in text or not text.rstrip().endswith("return XXTLanControl"):
        raise ValueError("下载内容不是 XXTLanControl.lua，请检查中控地址和响应")
    if target.exists():
        if target.read_bytes() == data:
            return summary
        if not force:
            raise ValueError(f"现有模块与下载版本不同，请先比较；确认替换时使用 --force：{target}")
    # 完整下载和校验后才替换，网络失败不能破坏项目里已有的模块。
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(data)
        temporary.chmod(0o644)
        os.replace(temporary, target)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    summary.update(exists=True, changed=True)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", type=Path)
    parser.add_argument("--backend-url", required=True, help="Controller base URL without /mcp")
    parser.add_argument("--type", choices=("xxt", "xpp"), dest="project_type")
    parser.add_argument("--apply", action="store_true", help="Download and install (default: offline preview)")
    parser.add_argument("--force", action="store_true", help="Replace a differing installed module")
    args = parser.parse_args()
    print_json(install_lancontrol(args.project_root, args.backend_url, project_type=args.project_type,
                                 apply=args.apply, force=args.force))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, urllib.error.URLError) as error:
        raise SystemExit(str(error)) from None
