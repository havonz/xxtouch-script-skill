# YOLO Profiles

For segmentation, pose, tracking, or custom layouts. Read the selected backend's guide first; pass `profile` through its constructor or call options. Ordinary code need not require this dependency directly.

## Tasks and Overrides

- Tasks: `detect`, `seg`, `pose`, `obb`, `track`, `classify`; `segment` / `segmentation` normalize to `seg`.
- Per-call `opts.profile` deep-merges over constructor `profile`; named methods such as `segment()` force the task.
- Standard shapes may allow inference; verify custom layouts with `get_model_info().outputs`.
- `profile.input`: dimensions, layout, channels, normalization, resize, letterbox. NCNN requires batchless CHW; no `add_batch=true`.

## Segmentation

Example for rows of `4 box fields + 80 class scores + 32 mask coefficients`, with prototypes in output 2:

```lua
local profile = {
    task = 'seg',
    outputs = {det = 1, proto = 2},
    decode = {class_start = 4, class_end = 84},
    seg = {coeff_start = 84, coeff_dim = 32, threshold = 0.0},
}
-- Pass to the selected YOLO backend through new({..., profile=profile}).
```

`outputs` indices are one-based, or use real output names. Feature offsets `class_start`, `class_end`, `coeff_start`, `keypoint_start` are zero-based with exclusive slice ends.

`decode` supports `kind` (default `decoded_matrix`), `prediction_layout`, `box_format`, `has_objectness`, `objectness_index`. Objectness and multi-scale anchor-grid exports need model-specific layouts; check the native decoder.

## Pose and Tracking

Single class, 17 keypoints with three components each:

```lua
local pose_profile = {
    task = 'pose',
    outputs = {det = 1},
    decode = {class_start = 4, class_end = 5},
    pose = {keypoint_start = 5, keypoint_count = 17, keypoint_dim = 3},
}
local tracking_profile = {
    task = 'track',
    track = {base_task = 'detect'},
}
```

Tracking supports `detect`, `seg`, `pose`, `obb`, not classification. Reuse instances across frames; [tracker](yolo_tracker.md) covers state/reset behavior.

`profile.postprocess`: `confidence`, `iou`, `max_det`, `class_ids`, `class_aware`; per-call options can override thresholds. Results add `mask`, `keypoints`, or track IDs. Coordinates map to the input image; masks have backend-specific layout/resolution, not necessarily screen dimensions.

Missing outputs or incompatible shapes throw. Close models after errors to release session/decoder/tracker resources. For native post-processing examples or debugging, follow the [source index](../inference-examples.md).
