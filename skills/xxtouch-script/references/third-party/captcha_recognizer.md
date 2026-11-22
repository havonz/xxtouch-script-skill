# captcha_recognizer

Preferred for slider captcha gaps; use [ddddocr](ddddocr.md) for text captchas. Requires native `onnxruntime`, `image.cv`, and Lua `yolo_backend_common`. [Install](vision-modules.md); [download](vision-models.md) preset `captcha-slider`.

## Example

```lua
local recognizer = require('captcha_recognizer')
local model = recognizer.Slider({
    model_dir = XXT_RES_PATH .. '/models/captcha-slider',
    providers = {'cpu'},
})
local ok, offset, confidence = pcall(function()
    return model:identify_offset(XXT_RES_PATH .. '/slider.png')
end)
model:close()
assert(ok, offset)
print(offset, confidence)
```

XPP: resolve models/images with `xpp.resource_path('res/...')`.

## Construction

- `Slider(opts)` or `new({type='slider', ...})`; only `slider` is supported.
- File: `slider.onnx`. Set `model_path` / `model_dir`; default directory: `XXT_HOME_PATH..'/models/captcha_recognizer'`.
- `providers` defaults to CPU; CoreML uses `{'coreml','cpu'}` with optional `fallback_to_cpu`.
- `coreml_compute_units`, `coreml_enable_on_subgraph`, `coreml_require_static_input_shapes`, `coreml_create_mlprogram` pass to the [native session](../api/onnxruntime.session.module.md).

## Calls

Input: path, image bytes, BASE64, or ImageObject. Coordinates refer to the input image; apply crop/scale transforms before touches. Gap `x1` is not automatically the drag distance.

| Method | Result |
| --- | --- |
| `identify(input[, opts])` | `box, confidence, preview`; `box={x1,y1,x2,y2}`; no match: `{}`, `0.0` |
| `identify_offset(input[, opts])` | Leftmost box's `x1, confidence, preview`; no match: `0, 0.0` |
| `predict(input[, opts])` | `{batch}`; `batch.boxes[i]={x1,y1,x2,y2,score,class_id}`, corresponding `batch.masks` |
| `get_model_info()` | Copy of model path, shapes, providers, output metadata |
| `close()` | Releases session; returns nil, so do not assert it |

`identify` / `identify_offset` defaults: `confidence=0.5`, `iou=0.8`; `show=true` returns a preview, released with `preview:destroy()`. `predict` accepts `confidence`, `iou`, `input_size`. Legacy forms: `predict(input, conf, iou, imgsz)` and `identify/identify_offset(input, conf, iou, show)`.

Loading/input/inference errors may throw; no-match results are separate. Close successfully constructed instances even after errors.
