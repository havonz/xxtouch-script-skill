# paddleocr_onnx

Only for explicitly requested full PaddleOCR; ordinary OCR uses built-in Paddle Lite / Apple Vision. Requires native `onnxruntime`, `image.cv`, and Lua `yolo_backend_common`. [Install](vision-modules.md); [models](vision-models.md).

## Example

Download `ppocrv5-onnx-chinese` or `ppocrv5-onnx-english` with `manage_models.py fetch <project-root> <model-id>`. These are download presets, not bundled weights.

```lua
local paddleocr = require('paddleocr_onnx')
local ocr = paddleocr.new({
    model_dir = XXT_RES_PATH .. '/models/ppocrv5-onnx-chinese',
    providers = {'cpu'},
    use_space_char = true,
})
local ok, result = pcall(function()
    return ocr:recognize(XXT_RES_PATH .. '/page.png')
end)
ocr:close()
assert(ok, result)
print(result.text)
```

XPP: resolve models/images with `xpp.resource_path('res/...')`.

## Models and Options

- Required: `rec.onnx` + matching `dict.txt`. `recognize` / `detect` also require `det.onnx`; REC-only supports `recognize_line` / `classification`.
- Set `model_dir`, or `det_model_path`, `rec_model_path`, `dict_path`; `det_model_dir` / `rec_model_dir` are supported. Default root: `XXT_HOME_PATH..'/models/paddleocr_onnx'`.
- [Chinese/English presets](https://huggingface.co/monkt/paddleocr-onnx/tree/7b02d0a30a07ba2b92ad1ff5a8941ae2c633de65) share v5 DET with language-specific REC/dictionaries. REC: dynamic width, height 48, probabilities. Keep `rec_apply_softmax=false`, `rec_values_are_probabilities=true`, `use_space_char=true` to match CTC blank/space classes.
- Other models use a custom catalog; `paddleocr-onnx-custom` is a placeholder. Paddle / `.pt` weights are not ONNX; exported ONNX needs no NCNN conversion.

| Options | Fields |
| --- | --- |
| Backend | `providers={'cpu'}` (default) or `{'coreml','cpu'}`, `fallback_to_cpu`, `threads` |
| DET | `max_side_len`, `det_db_thresh`, `det_db_box_thresh`, `det_db_unclip_ratio`, `det_db_use_dilate`, `det_use_polygon_score` |
| REC | `rec_batch`, `rec_batch_size`, `rec_batch_min_size`, `rec_bucket_width`, `rec_bucket_width_stride`, `rec_apply_softmax`, `rec_values_are_probabilities`, `use_space_char` |

CoreML options pass to the [native session](../api/onnxruntime.session.module.md). Match REC class count, dictionary order, and probabilities/logits to the model.

## API

Constructor: `new(opts)`; aliases `create` / `open`. Input: path, image bytes, BASE64, or ImageObject.

| Method | Result |
| --- | --- |
| `recognize(input[, opts])` / `ocr(input[, opts])` | `{text, lines}`; joined line text |
| `recognize_line(input[, opts])` | `{text, confidence, ...}`; `return_text_only=true` returns text |
| `classification(input[, opts])` | Single-line text by default |
| `detect(input)` / `det(input)` | Array of `{box, confidence, x, y, w, h}` |
| `get_model_info()` | Copies: `rec`, `det`, `dict_path`, `det_config`, `rec_config`; absent DET: `det=nil` |
| `close()` | Release REC/DET sessions; returns nil |

`return_stats=true` on `recognize` adds `stats.det.count` and `stats.rec`. Lines include `text`, `confidence`, `det_confidence`, `box`, `x/y/w/h`; `box` is four `{x=...,y=...}` points in input-image coordinates. Add screen-crop offsets.

No text yields empty lines/text; missing models, bad input, or inference failures may throw. Use `pcall` where recovery is needed and close constructed instances after errors too.
