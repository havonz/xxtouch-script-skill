# Recognition Modules

Ordinary OCR uses built-in Paddle Lite / Apple Vision through [screen.ocr_text](../api/screen.ocr_text.md) or [ImageObject:ocr_text](../api/ImageObject.ocr_text.md), with explicit `engine="paddle"` / `"apple"`. Full PaddleOCR requires an explicit developer request, including a named NCNN/ONNX wrapper; poor built-in results alone are not a reason to switch.

Choose one module below. For native API learning instead, use the [source examples](../inference-examples.md) without installing wrappers or downloading weights.

| Need | Module / guide |
| --- | --- |
| Slider captcha gaps | Prefer [captcha_recognizer](captcha_recognizer.md) |
| Text captchas / captcha detection | [ddddocr](ddddocr.md) |
| Requested full PaddleOCR, ONNX | [paddleocr_onnx](paddleocr_onnx.md) |
| Requested full PaddleOCR, NCNN | [paddleocr_ncnn](paddleocr_ncnn.md) |
| YOLO, ONNX / NCNN / CoreML | [yolo_onnx](yolo_onnx.md) / [yolo_ncnn](yolo_ncnn.md) / [yolo_coreml](yolo_coreml.md) |
| Track detection IDs across frames | [yolo_tracker](yolo_tracker.md) |
| Segmentation, pose, custom output layouts | YOLO [profile](yolo_profile_runtime.md) |

Both captcha modules are specialized for captchas. Use ddddocr slider helpers only for specifically required `slide_match` / `slide_comparison` operations or projects specifying ddddocr. General object detection uses YOLO.

Choose one backend matching available models and device APIs. Native `ncnn`, `onnxruntime`, global `coreml`, and weights are not installed with Lua wrappers. Original PaddleOCR models usually need [NCNN conversion](paddleocr_ncnn_conversion.md); its preset downloads are already converted.

## Installation

Sources and their dependency `manifest.json` live in `assets/frameworks/` beside `XXTDo.lua`; XXTDo retains its own installer. From the skill root:

```bash
python3 scripts/install_modules.py <project-root> paddleocr_ncnn
python3 scripts/install_modules.py <project-root> paddleocr_ncnn --apply
```

Default: preview. `--apply`: copy. Type comes from `.config.type` or layout; override with `--type xxt` / `--type xpp`.

- XXT: `lua/`, preserving existing `lua/scripts/<module>.lua`. XPP: package root.
- Checks all dependencies and source SHA256 before copying; any conflict blocks all copies. Reuses identical files; refuses differing/encrypted targets or duplicate names.
- Resolve conflicts by comparing versions and preserving local changes, not deleting files to bypass checks.
- Keep original `require` names; never point `package.path` at the installed skill directory.

| Selected module | Copied dependencies |
| --- | --- |
| `captcha_recognizer`, `ddddocr`, `paddleocr_onnx` | `yolo_backend_common` |
| `paddleocr_ncnn` | `yolo_backend_common`, `paddleocr_ncnn_dict` |
| Any YOLO backend | `yolo_backend_common`, `yolo_profile_runtime`, `yolo_tracker` |
| `yolo_profile_runtime`, `yolo_tracker` | `yolo_backend_common` |

Do not read helpers or large dictionaries for ordinary usage. The Lua dictionary is a module dependency and belongs in the build; it is not an excluded weight file. Read [model management](vision-models.md) only when preparing weights.
