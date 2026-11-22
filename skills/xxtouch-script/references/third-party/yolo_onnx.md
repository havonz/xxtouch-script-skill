# yolo_onnx

YOLO detection, classification, OBB, and profile-based segmentation/pose/tracking. Requires native `onnxruntime`; [installation](vision-modules.md) supplies `yolo_backend_common`, `yolo_profile_runtime`, `yolo_tracker`. [Model preparation](vision-models.md) is separate. Read only the selected backend.

## Example

With compatible project model `my-yolo`:

```lua
local yolo = require('yolo_onnx')
local model = yolo.new({
    model_path = XXT_RES_PATH .. '/models/my-yolo/model.onnx',
    task = 'detect', providers = {'cpu'},
})
local ok, detections = pcall(function()
    return model:detect(XXT_RES_PATH .. '/target.png')
end)
model:close()
assert(ok, detections)
for i = 1, #detections do
    local det = detections[i]
    print(det.class_id, det.score, det.box[1], det.box[2])
end
```

XPP: resolve model/image resources with `xpp.resource_path('res/...')`.

## Backend

- Set `model_path` or `model_dir`; default `XXT_HOME_PATH..'/models/yolo_onnx/model.onnx'`. Preserve any external-data paths.
- `providers={'cpu'}` (default) or `{'coreml','cpu'}`, `fallback_to_cpu`, `threads`. Removed `use_gpu` raises an error.
- `coreml_compute_units`, `coreml_enable_on_subgraph`, `coreml_require_static_input_shapes`, `coreml_create_mlprogram` pass to the [native session](../api/onnxruntime.session.module.md).
- `new(opts)` has `create` / `open` aliases; module functions include `tracker(opts)` and `supported_tasks()`.
- `yolo-onnx-custom` requires a supplied export; `.pt` is not converted automatically.

## API

- `task`: `detect` (default), `classify`, `obb`, `seg` / `segment`, `pose`, `track`. Match the export; `supported_tasks()` is not a model-compatibility guarantee.
- Constructor options: `input_width`, `input_height`, `confidence`, `iou`, `max_det`, `class_ids`, `class_agnostic`, `class_names`, `profile`.
- `class_names`: array, label path, or `coco80` / `imagenet1000` / `dota15` presets requiring companion text files. `class_id` is zero-based; labels are one-based.
- Input: path, image bytes, BASE64, ImageObject. `run(input[, opts])` dispatches by task; `predict` is its alias.
- `detect(input[, conf][, iou][, opts])` also accepts an options table at `conf`. `obb` / `detect_obb`, `segment`, `pose`, `track` use the same threshold forms.
- `classify(input[, opts])` accepts `topk`, `return_logits`. `get_model_info()` exposes I/O, task, and profile metadata.

| Task | Result |
| --- | --- |
| Detect | Array with `box={x1,y1,x2,y2}`, `score`, `class_id`; usually `x1/y1/x2/y2`, `width/height`, `cx/cy`, optional `label` |
| Classify | `class_id`, `score`, optional `label`, `classes`; optional `logits` |
| OBB | Also `cx/cy/w/h/theta`, `points`, enclosing box |
| Seg / pose / track | Adds `mask`, `keypoints`, or tracking fields; see [profiles](yolo_profile_runtime.md) / [tracker](yolo_tracker.md) only as needed |

Coordinates map to the input image; add screen-crop offsets. Empty detections mean no targets; loading, labels, shapes, or inference errors may throw. Always `close()` constructed models, including after errors. Reuse tracking instances across frames. Ordinary detection needs no profile-source reading.
