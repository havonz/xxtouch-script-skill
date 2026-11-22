# Send Controller Logs (LCC.log)

## Signature
```lua
LCC.log(id, ...)
LCC.log(log_map)
```

## Parameters
- id  
    Integer from 1 to 6, pointing to one of the controller's six log channels.  
- ...
    Variadic arguments. Strings, tables, `ImageObject`, or a UI-state object returned by `LCC.capture_ui_state()`; regular tables are serialised with `table.deep_dump`, and strings can embed `[DATE]` and `[LINE]` placeholders.
- log_map
    Table whose keys match the aliases defined via `set_log_aliases`; values can be strings, tables, `ImageObject`, UI-state objects, or array tables containing those values.

## Returns
- none  

## Notes
> Validates that a controller address has been configured, otherwise raises an error.  
> Retries on network issues until the log is delivered; during retries a `sys.toast` notification is shown.  
> When using the alias map form, only keys that match an alias are sent, routed to the corresponding channel number.  
> If no alias keys match, the call returns without sending a request.

## Example
```lua
LCC.log(1, "[DATE] sync starting", { count = 128 })

LCC.log({
    ["Status"] = "Sync complete",
    ["Error"] = "0"
})
```

## Image Logs

`LCC.log` supports mixed text, regular tables, and images. Passing an `ImageObject` writes the image as PNG by default. Passing a string in the form `data:image/png;base64,...` or `data:image/jpeg;base64,...` is also detected as an image.

```lua
LCC.log(1, "Start", screen.image(100, 100, 200, 200), "Done")
```

If you want a smaller payload, compress the image yourself and pass a JPEG data URL:

```lua
local img = screen.image(100, 100, 200, 200)
local jpg = "data:image/jpeg;base64," .. img:jpeg_data(0.7):base64_encode()
LCC.log(1, "Compressed screenshot", jpg)
img:destroy()
```

The alias map form supports image logs too. A regular table without images is still rendered through `table.deep_dump`; an array table containing images is rendered in array order as mixed text and images.

```lua
LCC.set_log_aliases({ "Status", "Error" })

LCC.log({
    ["Status"] = { "Hello", screen.image(243, 247, 336, 345), "World" },
    ["Error"] = "0"
})
```

Image logs are best used for diagnostics or important visual evidence, not as part of routine progress logging. A single image can be up to 20 MiB, all images in one log entry can total up to 20 MiB, each image can be up to 12 megapixels, and one log entry can contain up to 8 images. If a limit is exceeded or the image format is unsupported, `LCC.log` raises an error. Prefer logging screenshots only at important checkpoints and crop them to the area you need to inspect; for continuous sampling, lower the frequency or pass a self-compressed JPEG data URL.

## UI-State Logs

`LCC.log` accepts the object returned by `LCC.capture_ui_state()` as a log content argument or an alias-map value. A UI-state object is not itself an alias map, so a log channel is required; `LCC.log(state)` raises an argument error. `LCC.capture_ui_state()` requires device-side `ui_element` version 0.6.0 or later. If the module is unavailable or outdated, update XXTouch before using **capture_ui_state**. It uploads the exact cached `.xxtuie` bytes and uses `[界面状态]` as the plain-text fallback. Alias maps and mixed-content arrays support UI-state objects as well.

```lua
local state = LCC.capture_ui_state()
LCC.log(1, "Submission failed", state)
state:destroy()
```

One HTTP request can contain at most one UI state. Regular images and the UI state in that request must total no more than 20 MiB after decoding. A destroyed object can no longer be logged. See [`LCC.capture_ui_state`](./capture_ui_state.md) for capture status, local saving, and resource cleanup.

Log history shows images and UI states as attachment cards. Click an image to preview the original and open it in the Color Picker; click a UI-state card to restore its screenshot and element tree in the Text Elements tool. When exporting logs with attachments, you can choose plain text only or a zip containing browsable HTML, original images, and original `.xxtuie` files. If an attachment file is missing, the HTML shows a missing-file placeholder while retaining the other log content and available attachments.
