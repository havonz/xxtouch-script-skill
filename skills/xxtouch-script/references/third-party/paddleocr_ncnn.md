# paddleocr_ncnn

Only for explicitly requested full PaddleOCR; ordinary OCR uses built-in Paddle Lite / Apple Vision. Requires native `ncnn`; installation includes `yolo_backend_common` and `paddleocr_ncnn_dict`. [Install](vision-modules.md); [models](vision-models.md).

Original Paddle/ONNX models need [NCNN conversion](paddleocr_ncnn_conversion.md). This wrapper accepts matching `.param/.bin` artifacts, not Paddle or `.onnx` files.

## Example

After installation, fetch `ppocrv5-mobile-ncnn`: already converted, adapted for dynamic dimensions, and validated. Do not reconvert it.

```lua
local paddleocr = require('paddleocr_ncnn')
local ocr = paddleocr.new({
    model_dir = XXT_RES_PATH .. '/models/ppocrv5-mobile-ncnn',
    threads = 1,
    use_vulkan_compute = false,
})
local ok, result = pcall(function()
    return ocr:recognize(XXT_RES_PATH .. '/page.png', {return_stats = true})
end)
ocr:close()
assert(ok, result)
print(result.text, #result.lines)
```

XPP: resolve models/images with `xpp.resource_path('res/...')`.

## Models and Options

- Preset files: `PP_OCRv5_mobile_det.ncnn.param`, `PP_OCRv5_mobile_det.ncnn.bin`, `PP_OCRv5_mobile_rec.ncnn.param`, `PP_OCRv5_mobile_rec.ncnn.bin`.
- REC is required; DET is optional for single-line recognition. Default root: `XXT_HOME_PATH..'/models/paddleocr_ncnn'`.
- Override `det_param_path`, `det_model_path`, `rec_param_path`, `rec_model_path`, or `det_model_dir` / `rec_model_dir`.
- `dict_path` / `rec_keys_path` supplies an external charset; otherwise the bundled PP-OCRv5 table is used. Match custom REC's character order; do not read the large Lua dictionary into context.

| Options | Fields |
| --- | --- |
| Backend | `threads`, `use_vulkan_compute`, `fallback_to_cpu`; query `has_vulkan()`, not ONNX `providers` |
| I/O | Defaults `in0` / `out0`; override `det_input_name`, `det_output_names`, `rec_input_name`, `rec_output_names` |
| DET | `max_side_len=960`, `det_db_thresh=0.3`, `det_db_box_thresh=0.5`, `det_db_unclip_ratio=1.6`, `det_db_use_dilate`, `det_use_polygon_score` |
| REC | `rec_image_height=48`, `rec_min_width=16`, `rec_max_width=960`, `rec_bucket_width`, `rec_bucket_width_stride`, `rec_apply_softmax`, `rec_values_are_probabilities`, `use_space_char` |

Recognition runs per detected box; ONNX REC batch options do not apply.

## API

Module: `new(opts)`, aliases `create` / `open`, plus `version()`, `backend_version()`, `has_vulkan()`. Input: path, image bytes, BASE64, or ImageObject.

| Method | Result |
| --- | --- |
| `recognize(input[, opts])` / `ocr(input[, opts])` | `{text, lines}`; `return_stats=true` adds `stats.det.count`, `stats.rec` |
| `recognize_line(input[, opts])` | `{text, confidence, ...}`; `return_text_only=true` returns text |
| `classification(input[, opts])` | Text by default |
| `detect(input)` / `det(input)` | Array of `{box, confidence, x, y, w, h}` |
| `get_model_info()` | Copies: `rec`, `det`, `dict_path`, `det_config`, `rec_config`; absent DET: `det=nil` |
| `close()` | Releases sessions; repeated calls return true |

Lines include `text`, `confidence`, `det_confidence`, `box`, `x/y/w/h`. `box` contains four `{x=...,y=...}` points in input-image coordinates; add screen-crop offsets. Empty detections mean no matches. `stats.rec.enabled=false` means no batching, not failure.

Missing REC, detection without DET, bad input, or session failures throw. Use `pcall` for recovery and close constructed instances after errors too.
