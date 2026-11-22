---
name: xxtouch-script
description: Create XXT/XPP projects and develop or debug XXTouch Lua 5.3 scripts, XUI, screen/touch automation, and XXTDo. Integrate XXTLanControl.lua for device-to-controller communication.
---

# XXTouch scripting

Read the user's `AGENTS.md` if present. Identify XXT or XPP and any existing XXTDo. Follow project language conventions for replies, code comments, and user-facing text.

## Lookup

Open a reference in the installed Skill or via MCP, e.g. `skill_read({skill:"xxtouch-script",path:"references/api/touch.tap.md"})`. Omit `path` for this guide. For unknown paths, search `references/api-index.tsv` by symbol or `references/aliases.tsv` by English keyword. Use MCP or local `rg`. Check arguments, returns, callbacks, and minimum versions. For undocumented behavior, inspect the user's script or ask.

`skill_list` and `skill_read` return a `downloadUrl` for the whole Skill. Reuse it when helpers or templates are needed. Run helper commands from the installed or extracted Skill directory.

## Projects

To create a project, pass an unused destination (including no symlink), type, and name. `--bid` defaults to the name. Use `--apply` when creation is requested. Omit it for a JSON preview.

```sh
python3 scripts/create_project.py "$PROJECT_DIR" --type xxt --name Demo --bid com.example.demo --apply
```

The helper installs the bundled template, editor settings, project instructions, and `.tmp` ignores. Keep an existing project's type unless conversion is requested.

- [XXT scripts](references/xxt.md) start at `lua/scripts/main.lua`. Read `res/` via `XXT_RES_PATH`. Use `dialog` / `Dialog` for temporary UI.
- [XPP bundles](references/xpp.md) use `Info.lua.Executable` and `xpp.resource_path`. Only XPP uses `xui.*`, `.xui`, and `.xuic`. See [XUI format](references/xui-format.md).
- When a device script communicates with XXTLanControl for logs, data, shared files, or human assistance, [obtain XXTLanControl.lua](references/lancontrol.md) and read the relevant `LCC.*` page.
- Use XXTDo when requested or already present. Prefer it for UI-state automation unless plain XXTouch is requested. Read [setup](references/xxtdo.md) and [patterns](references/xxtdo-patterns.md). If requested and missing, run `python3 scripts/install_xxtdo.py "$PROJECT_DIR" --apply`. XPP uses root `XXTDo.lua`. XXT uses `lua/XXTDo.lua` or its existing `lua/scripts/XXTDo.lua`.

## Task references

- [Device paths and rootless/rootful](references/api/xxt.env.md) · [XUI-backed dialogs](references/api/Dialog.xui.md) · [System alerts](references/api/alerthelper.md).
- Use `local profile = require("profile")` for [.mobileconfig profiles](references/api/profile.md).
- [UI elements](references/third-party/ui_element.md) for `device_ui_element_*`. [Other modules](references/third-party/index.md).
- [Screen, touch, image patterns](references/workflow.md) · [Color similarity](references/color-similarity.md) (`scripts/color_similarity.py`) · [Code style](references/style.md).
- [OpenCV](references/api/image.cv.md) · [cv functions](references/api/image.cv.functions.md) · [matrix methods](references/api/cv.mat.md).
- Use [human-assist helpers](references/human-assist.md) for screenshots, colors, points, rectangles, matrix dictionaries, and confirmations. If unavailable, request samples.

## Recognition

- For ordinary OCR, use [screen.ocr_text](references/api/screen.ocr_text.md) or [ImageObject:ocr_text](references/api/ImageObject.ocr_text.md) with `engine="paddle"` or `"apple"`. Load full PaddleOCR wrappers and weights only on explicit request.
- For requested recognition modules, see [vision modules](references/third-party/vision-modules.md). Prefer `captcha_recognizer` for sliders and `ddddocr` for text captchas. `scripts/install_modules.py` includes dependencies.
- Exclude [model weights](references/third-party/vision-models.md) through `buildIgnores` only. Generate device download code only on request.
- Study [ONNX/CoreML examples](references/inference-examples.md) using the API and relevant functions in `assets/frameworks/`. Skip installs, weights, and dictionaries for code study.

## Scripting

Use documented Lua 5.3 APIs. Built-ins such as `app`, `sys`, `touch`, `screen`, `image`, `file`, `http`, `json`, and `dialog` are globals. Do not require or shadow them. Prefer built-ins and append with `t[#t+1] = value`. For shell commands prefer [os.run](references/api/os.run.md) for stdin, stdout, stderr, and a timeout in seconds. Use `os.execute` or `io.popen` only on explicit request. Use project-relative paths or supplied values. Keep temporary files in `.tmp/` and exclude them with `scripts/ensure_config_ignores.py`.

For device checks, use the connected controller's MCP, e.g. `tool_call({tool:"device_get_status",args:{udid:"DEVICE_ID"}})`. Read its control guide (`xxtlancontrol` or `xxtcloudcontrol`) for script execution and logs. Discover IDs with `tool_list` or fetch argument schemas and `readOnly` via `tool_info({tools:"device_get_status"})`. Without a connected device, use the documented APIs.
