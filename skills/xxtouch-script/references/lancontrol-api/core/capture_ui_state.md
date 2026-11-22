# Capture UI State (LCC.capture_ui_state)

## Signature

```lua
local state = LCC.capture_ui_state(options)
```

## Requirements

`LCC.capture_ui_state` requires the `ui_element` module with `ui_element._VERSION` at `0.6.0` or newer. If the module cannot be loaded, has no valid version, is older than `0.6.0`, or lacks UI-state capture support, the call asks the user to update XXTouch before using **capture_ui_state** and does not create a partial state object.

## Parameters

- `options.hit_test_spacing`: optional positive integer; screen hit-test sampling spacing, default `40`.
- `options.force_hit_test`: optional boolean; force screen-sampling hit tests, default `false`.

## Return Value

Returns a UI-state object. It immediately captures the current PNG screenshot and raw text-element tree, then builds one `.xxtuie` archive. Saving and logging later reuse the exact cached bytes without recapturing.

```lua
local state = LCC.capture_ui_state({
    hit_test_spacing = 40,
    force_hit_test = false,
})

local info = state:status()
local ok, err = state:save_to_file(XXT_SCRIPTS_PATH .. "/scene.xxtuie")
if not ok then
    error(err)
end

LCC.log(1, "Scene", state)
state:destroy()
```

## Object Methods

### `state:status()`

Returns a new status table on every call, so changing it never changes internal state. It remains available after the object is destroyed.

- `status`: `complete`, `screenshot`, `elements`, or `unavailable`.
- `captured_at` / `capturedAt`: UTC time at which capture started.
- `screenshot.status`: `captured` or `unavailable`, plus `width` and `height`; failures also include `error`.
- `elements.status`: `captured` or `unavailable`, plus `count`; failures also include `error`.

### `state:save_to_file(path)`

Atomically writes the cached archive to the specified path, replacing an existing file. It returns `true` on success or `nil, err` on failure. The path and extension are used exactly as supplied; `.xxtuie` is recommended so file managers can detect it automatically. Saving is unavailable after destruction.

### `state:destroy()`

Releases the cached archive. It is idempotent. After destruction, `status()` still works, while saving and logging fail.

## Partial Capture Failures

After the version and capability checks pass, the screenshot and element tree are captured independently. If either runtime capture fails, the result is still a valid archive with exactly `manifest.json`, `screenshot.png`, and `elements.json`: an unavailable screenshot uses a transparent 1×1 PNG, an unavailable element tree uses an empty element array, and the manifest stores a short error. `LCC.capture_ui_state()` raises when its dependency is unsupported, parameters are invalid, the archive cannot be built, or the archive exceeds 20 MiB.

The original PNG is limited to 16 MiB, 16384 pixels per side, and 12 megapixels. Element JSON is limited to 4 MiB, 5000 nodes, and depth index 32. Exceeding an individual limit marks that item as `unavailable`.
