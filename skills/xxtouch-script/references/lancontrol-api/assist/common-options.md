# Common Options and Return Objects

This page describes the shared `options`, task object, result objects, and error statuses used by `LCC.assist` APIs.

## options Fields

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `type` | string | `"text"` | Request type. Recognized aliases: `"text"`/`"text-reply"`, `"point"`/`"pick-point"`, `"control"`/`"device-control"`. Convenience wrappers set this automatically. |
| `title` | string | `"脚本请求人工辅助"` | Title shown in the control center. |
| `text` / `prompt` | string | `""` | Instructions shown to the operator. Make them actionable; do not write vague text such as "provide more information". |
| `timeout` | number | `300` | Wait timeout in seconds; also used as the backend task expiration when creating the task. |
| `pollIntervalMs` | number | `1000` | Polling interval in milliseconds. Values below `250` are clamped to `250`. |
| `screenshotLocalPath` | string |  | Local image path on the device; the SDK uploads it as a temporary resource on the controller. |
| `screenshotPath` | string |  | Existing image path under the control center `files` root. |
| `screenshotImage` / `image` | ImageObject |  | XXTouch image object. The SDK exports it as a data URL and writes it to `input.imageSrc`. |
| `screenshotImageData` / `imageData` | string |  | PNG/JPEG binary image data. The SDK converts it to a data URL and writes it to `input.imageSrc`. |
| `screenshotImageFormat` / `imageFormat` | string | `"jpeg"` | Export format for `screenshotImage`. Supported values are `"jpeg"` and `"png"`. |
| `screenshotImageQuality` / `imageQuality` | number | `0.7` | JPEG quality used when exporting `screenshotImage`, from `0.0` to `1.0`. |
| `screenshotImageMimeType` / `imageMimeType` | string | auto-detect | MIME type for `screenshotImageData`; PNG/JPEG data usually does not need this. |
| `imageRect` | table |  | Crop-to-device coordinate mapping, for example `{ left = 100, top = 200, width = 300, height = 120 }`. |
| `input` | table | `{}` | Extra structured metadata passed through to the control center. The SDK adds `requestType` and `scriptRequestId`. |

`screenshotLocalPath` has higher priority than `screenshotPath`. If `screenshotLocalPath` is provided, the SDK uploads the file and uses the uploaded path.

If `input.imageSrc`, `screenshotLocalPath`, and `screenshotPath` are not provided, the SDK tries to convert `screenshotImage` or `screenshotImageData` into `input.imageSrc`. The caller owns the `ImageObject`; the SDK does not call `destroy()` automatically.

### Pass an ImageObject Directly

```lua
local img = screen.image()
local result, err = LCC.assist.request_control({
    title = "Need human handling",
    text = "Remote-control the device, finish the current verification, then click Done",
    screenshotImage = img,
    screenshotImageQuality = 0.6,
})
if img.destroy then
    img:destroy()
end
```

### Pass Image Data Directly

```lua
local img = screen.image()
local data = img:png_data()
if img.destroy then
    img:destroy()
end

local result, err = LCC.assist.request_control({
    title = "Need human handling",
    text = "Remote-control the device, finish the current verification, then click Done",
    screenshotImageData = data,
})
```

### Pass an Image URL Directly

```lua
local result, err = LCC.assist.request_control({
    title = "Need human handling",
    text = "Remote-control the device, finish the current verification, then click Done",
    input = {
        imageSrc = "data:image/jpeg;base64,...",
    },
})
```

`input.imageSrc` does not upload a file and does not populate `screenshotPath`.

After a task is submitted, cancelled, or expired, the returned object no longer includes `imageSrc` in `input`.

Automatically uploaded screenshots are cleaned up when the controller starts. Save a separate copy under a resource path you manage for long-term reuse; do not treat the generated `screenshotPath` as a permanent file reference.

## Task Object

`task` is the assist task stored by the control center. Common fields:

```lua
{
    id = "assist_xxx",
    kind = "text-reply",
    title = "Enter captcha",
    prompt = "Enter the captcha shown in the screenshot",
    status = "pending",
    deviceId = "device UDID",
    source = "lua-script",
    screenshotPath = "assist/...",
    input = {},
    result = nil,
    createdAt = 1781196058792,
    updatedAt = 1781196058792,
    expiresAt = 1781196358792,
}
```

Timestamp fields are milliseconds since epoch. Script-created requests automatically set `deviceId = device.udid()` and `source = "lua-script"`.

## Result Objects

Successful text reply:

```lua
{ kind = "text-reply", text = "1234" }
```

Successful picked point:

```lua
{
    kind = "pick-point",
    x = 123,
    y = 456,
    imageX = 123,
    imageY = 456,
    color = "AABBCC",
}
```

`x` and `y` are physical device coordinates and can be used directly with `touch.tap`. `imageX` and `imageY` are coordinates inside the screenshot.

Remote control when the operator clicks Done:

```lua
{ kind = "device-control", completed = true }
```

When the operator expands Manual Submit and submits valid JSON, `result` is the Lua value decoded from that JSON. For example, submitting:

```json
{"allowed":true,"reason":"confirmed by operator"}
```

returns:

```lua
{ allowed = true, reason = "confirmed by operator" }
```

When the operator manually submits non-JSON plain text:

```lua
{ note = "plain text content" }
```

Empty Manual Submit content is not submitted, so the script keeps waiting.

## Errors and Statuses

On wait failure:

```lua
nil, err, task
```

Common `err` values:

- `"cancelled"`: cancelled by the user or script.
- `"expired"`: expired on the backend.
- `"timeout"`: the script wait timeout was reached; the SDK has attempted to cancel the task.
- `"not found"`: the task does not exist, often because the backend restarted or cleaned it up.
- Other strings: network error, screenshot upload error, or backend response text.

Only `submitted` returns a `result`. Treat `cancelled`, `expired`, and `timeout` as no human result.
