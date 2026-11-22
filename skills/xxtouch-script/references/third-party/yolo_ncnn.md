# yolo_ncnn

YOLO detection, classification, OBB, and profile-based segmentation/pose/tracking. Requires native `ncnn`; [installation](vision-modules.md) supplies `yolo_backend_common`, `yolo_profile_runtime`, `yolo_tracker`. [Model preparation](vision-models.md) is separate. Read only the selected backend.

## Example

With compatible project model `my-yolo`:

```lua
local yolo = require('yolo_ncnn')
local model_dir = XXT_RES_PATH .. '/models/my-yolo'
local model = yolo.new({
    param_path = model_dir .. '/model.param',
    model_path = model_dir .. '/model.bin',
    task = 'detect', threads = 1, use_vulkan_compute = false,
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

- Set both `param_path` and `model_path`, or `model_dir` containing `model.param` / `model.param.bin` and `model.bin`. Default root: `XXT_HOME_PATH..'/models/yolo_ncnn'`.
- I/O defaults: `in0`, `{'out0'}`; segmentation uses `{'out0','out1'}`. Override `input_name`, `output_names`, and where needed `output_shapes` / `profile`.
- Backend options: `use_vulkan_compute`, `fallback_to_cpu`, `threads`, `gpu_device`, `light_mode`. Query `has_vulkan()`; do not use ONNX `providers`.
- Input is batchless CHW: `layout` only `chw` / `nchw`; `add_batch=true` throws. Classification defaults to stretch, others to letterbox. Options: `resize_mode`, `letterbox_mode`, `pad_color`, `scale`, `mean`, `std`, `channel_order`.
- Constructor: `new(opts)`, with no `create` / `open` / `tracker` aliases. Module functions: `version()`, `backend_version()`, `has_vulkan()`, `supported_tasks()`.
- `yolo-ncnn-custom` requires a supplied model; output layouts vary by export.

## API

- `task`: `detect` (default), `classify`, `obb`, `seg` / `segment`, `pose`, `track`. Match the export; `supported_tasks()` is not a model-compatibility guarantee.
- Constructor options: `input_width`, `input_height`, `confidence`, `iou`, `max_det`, `class_ids`, `class_agnostic`, `class_names`, `profile`.
- `class_names`: array, label path, or `coco80` / `imagenet1000` / `dota15` presets requiring companion text files. `class_id` is zero-based; labels are one-based.
- Input: path, image bytes, BASE64, ImageObject. `run(input[, opts])` dispatches by task; `predict` is its alias.
- `detect(input[, conf][, iou][, opts])` also accepts an options table at `conf`. `obb`, `segment`, `pose`, `track` use the same threshold forms.
- `classify(input[, opts])` accepts `topk`, `return_logits`. `get_model_info()` exposes I/O, task, and profile metadata.

| Task | Result |
| --- | --- |
| Detect | Array with `box={x1,y1,x2,y2}`, `score`, `class_id`; usually `x1/y1/x2/y2`, `width/height`, `cx/cy`, optional `label` |
| Classify | `class_id`, `score`, optional `label`, `classes`; optional `logits` |
| OBB | Also `cx/cy/w/h/theta`, `points`, enclosing box |
| Seg / pose / track | Adds `mask`, `keypoints`, or tracking fields; see [profiles](yolo_profile_runtime.md) / [tracker](yolo_tracker.md) only as needed |

Coordinates map to the input image; add screen-crop offsets. Empty detections mean no targets; loading, labels, shapes, or inference errors may throw. Always `close()` constructed models, including after errors. Reuse tracking instances across frames. Ordinary detection needs no profile-source reading.
