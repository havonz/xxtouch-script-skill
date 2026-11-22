# ddddocr

Text captcha OCR and detection within captcha images. Prefer [captcha_recognizer](captcha_recognizer.md) for slider captchas. Requires native `onnxruntime`, `image.cv`, and Lua `yolo_backend_common`. [Install](vision-modules.md); [models](vision-models.md).

## Example

```lua
local ddddocr = require('ddddocr')
local ocr = ddddocr.new({
    model_dir = XXT_RES_PATH .. '/models/ddddocr-old',
    providers = {'cpu'},
    show_ad = false,
})
local ok, result = pcall(function()
    return ocr:classification(XXT_RES_PATH .. '/captcha.png', {
        charset_range = '0123456789', probability = true,
    })
end)
ocr:close()
assert(ok, result)
print(result.text, result.confidence)
```

XPP: resolve models/images with `xpp.resource_path('res/...')`.

## Construction

| Mode | Options | Preset / files |
| --- | --- | --- |
| Default text OCR | `ocr=true` (default) | `ddddocr-old`: `common_old.onnx`, `common_old.json` |
| Newer text OCR | `beta=true` | `ddddocr-beta`: `common.onnx`, `common.json` |
| Captcha detection | `det=true` | `ddddocr-det`: `common_det.onnx` |
| Slider helpers only | `ocr=false`, no custom model | No session |

`old` and `beta` cannot both be true. `det=true` takes precedence; OCR/DET calls require separate instance modes. Custom OCR requires matching `import_onnx_path` and `charsets_path`.

Set `model_dir`; default: `XXT_HOME_PATH..'/models/ddddocr'`. `providers` defaults to CPU; `{'coreml','cpu'}`, `fallback_to_cpu`, and [CoreML session options](../api/onnxruntime.session.module.md) are supported.

## Calls

Input: path, image bytes, BASE64, or ImageObject.

- `classification(input[, opts])` / `ocr(input[, opts])`: text; with `probability=true`, `{text, confidence, probabilities, charset}`.
- `charset_range` limits one call; `set_ranges(value)` sets the instance's range; `get_charset()` returns its charset.
- OCR options: `png_fix`, `color_filter_colors={'red','blue'}`, `color_filter_custom_ranges={{{h_min,s_min,v_min},{h_max,s_max,v_max}}}`. Query presets with `available_colors()`.
- `det(input)` / `detect(input)` / `detection(input)`: `{{x1,y1,x2,y2}, ...}`; empty means no detections.
- `get_model_info()`: copied model/I/O/mode metadata. `close()`: release session.

## Explicit Slider Matching / Comparison

Use only when these operations or ddddocr are specifically required:

```lua
local ddddocr = require('ddddocr')
local match = ddddocr.slide_match(target_img, background_img)
local difference = ddddocr.slide_comparison(background_with_gap, background_without_gap)
print(match.target_x, match.target_y, match.confidence)
```

Module/instance APIs: `slide_match(target, background[, simple_target])`, `slide_comparison(target, background)`. No OCR/DET weights or OCR instance are needed for module-level calls. Comparison requires equal image dimensions.

Returns `target={center_x,center_y}`, `target_x`, `target_y`, `confidence`. Apply input-image crop/scale offsets before screen actions. Loading/inference may throw; use `pcall` for recovery and always close constructed instances.
