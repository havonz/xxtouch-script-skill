# yolo_tracker

Assigns `track_id` across detection frames; no image inference or weights. Requires Lua `yolo_backend_common`. Uses an available native ONNX Runtime / CoreML tracker, otherwise Lua IoU matching.

## Example

```lua
local tracker = require('yolo_tracker').tracker({
    iou_threshold = 0.3, max_age = 30, min_hits = 1,
})
local tracked = tracker:update({
    {box = {10, 20, 60, 80}, score = 0.9, class_id = 0},
}, 0)
print(tracked[1].track_id)
tracker:close()
```

Constructor: `tracker(opts)`, not `new()`. Reuse one instance per sequence.

## API

- `update(detections[, timestamp])`: input records need `box={x1,y1,x2,y2}`, with optional `score`, zero-based `class_id`, labels, etc. Returns current detections with tracking fields.
- Fields: `track_id`, `track_hits`, `track_age`; ID may be absent before `min_hits`. Array indices are not IDs.
- Defaults: `iou_threshold=0.3`, `max_age=30` unmatched updates (not seconds), `min_hits=1`.
- Call `update({})` on empty frames. Keep timestamps increasing with consistent units.
- `reset()`: clear tracks and ID counter when changing scenes/sequences. `state()`: track state. `close()`: end use.

Use the same coordinate system/scale across frames; convert crop offsets before matching. Lua IoU fallback need not match native occlusion recovery.

`yolo_onnx.tracker(opts)` and `yolo_coreml.tracker(opts)` are aliases; `yolo_ncnn` has none. `model:track(image)` owns its tracker: see [profiles](yolo_profile_runtime.md); do not wrap its results in another tracker.
