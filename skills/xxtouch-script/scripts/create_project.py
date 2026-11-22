#!/usr/bin/env python3
"""Create an XXT or XPP project."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
from pathlib import Path
from typing import Any

from ensure_config_ignores import append_missing, ensure_array, load_config, write_config
from xxtouch_assist_common import print_json


TEMPLATE_ROOT = Path(__file__).resolve().parents[1] / "assets" / "development-project-templates"
PROMPT_ROOT = Path(__file__).resolve().parents[1] / "assets" / "script-templates"


def create_project(
    project_root: Path, project_type: str, name: str, *, bid: str | None = None, apply: bool = False
) -> dict[str, Any]:
    if project_type not in {"xxt", "xpp"}:
        raise ValueError("项目类型必须是 xxt 或 xpp")
    name = name.strip()
    bid = name if bid is None else bid.strip()
    for label, value in (("项目名称", name), ("项目标识", bid)):
        if not value or value in {".", ".."}:
            raise ValueError(f"{label}不能为空或为 .、..")
        if any(char in '/\\:*?"<>|' or ord(char) < 32 for char in value):
            raise ValueError(f"{label}不能包含 / \\ : * ? \" < > | 或控制字符")

    # 先检查路径本身，避免 resolve 将悬空符号链接转为可创建的目标。
    root = Path(os.path.abspath(project_root.expanduser()))
    if root.exists() or root.is_symlink():
        raise FileExistsError(f"目标路径已存在，不能覆盖：{root}")
    root = root.parent.resolve() / root.name
    if root.is_relative_to(TEMPLATE_ROOT.resolve()):
        raise ValueError("目标路径不能位于项目模板目录中")
    template = TEMPLATE_ROOT / f"{project_type}-script-template"
    if not template.is_dir():
        raise FileNotFoundError(f"项目模板不存在：{template}")
    entry = "lua/scripts/main.lua" if project_type == "xxt" else "main.lua"
    if not (template / entry).is_file():
        raise FileNotFoundError(f"模板缺少入口脚本：{template / entry}")

    config = load_config(template / ".config")
    config.update(type=project_type, bid=bid, name=name)
    if project_type == "xxt":
        for row in config.get("information", []):
            if isinstance(row, list) and len(row) >= 2:
                if row[0] == "Name":
                    row[1] = name
                elif row[0] == "Description" and isinstance(row[1], str):
                    row[1] = row[1].replace("xxt-script-template", name)
    for key in ("ignores", "buildIgnores"):
        append_missing(ensure_array(config, key), [".tmp"])
    config.setdefault("libs", [])

    info = None
    if project_type == "xpp":
        info = (template / "Info.lua").read_text(encoding="utf-8")
        for field, value in (("BundleIdentifier", bid), ("BundleDisplayName", name), ("BundleName", name)):
            literal = json.dumps(value, ensure_ascii=False)
            info, count = re.subn(
                rf"(?m)^(\s*{field}\s*=\s*)[^;\n]+;",
                lambda match: f"{match[1]}{literal};",
                info,
                count=1,
            )
            if count != 1:
                raise ValueError(f"模板 Info.lua 缺少字段：{field}")

    prompts = {
        filename: (PROMPT_ROOT / filename).read_text(encoding="utf-8")
        for filename in ("AGENTS.md", "xxtouch-script-guide.md")
    }
    if project_type == "xpp":
        # 两种创建入口共用文档源，避免 XPP 项目带入 XXT 的入口和资源路径规则。
        for filename, start_marker, next_marker, replacement_name in (
            ("AGENTS.md", "### 项目说明", "### 必须使用的文档流程", "XPP_AGENTS_PROJ.md"),
            ("xxtouch-script-guide.md", "## 项目结构", "## ", "XPP_STRUCTURE.md"),
        ):
            content = prompts[filename]
            start = content.find(start_marker)
            end = content.find("\n" + next_marker, start + len(start_marker))
            if start < 0 or end < 0:
                raise ValueError(f"文档模板缺少项目章节：{filename}")
            replacement = (PROMPT_ROOT / replacement_name).read_text(encoding="utf-8")
            prompts[filename] = content[:start] + replacement.rstrip("\n") + "\n\n" + content[end + 1:]

    summary = {
        "projectRoot": str(root),
        "projectType": project_type,
        "name": name,
        "bid": bid,
        "entry": entry,
        "template": str(template),
        "dryRun": not apply,
        "created": False,
    }
    if apply:
        root.parent.mkdir(parents=True, exist_ok=True)
        # 独占创建目录，失败时只清理本次创建的目录，保留调用方原有内容。
        root.mkdir()
        try:
            shutil.copytree(
                template, root, dirs_exist_ok=True,
                ignore=shutil.ignore_patterns(".DS_Store", "._*", ".gitkeep"),
            )
            write_config(root / ".config", config)
            if info is not None:
                (root / "Info.lua").write_text(info, encoding="utf-8")
            for filename, content in prompts.items():
                (root / filename).write_text(content, encoding="utf-8")
        except BaseException:
            shutil.rmtree(root)
            raise
        summary["created"] = True
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", type=Path, help="Exact destination, which must not exist")
    parser.add_argument("--type", required=True, choices=("xxt", "xpp"), help="Project type")
    parser.add_argument("--name", required=True, help="Project name")
    parser.add_argument("--bid", help="Bundle ID (default: name)")
    parser.add_argument("--apply", action="store_true", help="Create the project (default: preview)")
    args = parser.parse_args()
    print_json(create_project(args.project_root, args.type, args.name, bid=args.bid, apply=args.apply))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from None
