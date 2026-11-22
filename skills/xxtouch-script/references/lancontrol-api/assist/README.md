# Human Assist

`LCC.assist` lets a device script ask the control center for human assistance. A request can include a screenshot and clear instructions, block until the operator submits a result, and then continue.

## Request Types

| Type | API | Use case | Typical script action |
| --- | --- | --- | --- |
| Text reply | `LCC.assist.ask_text()` | Captcha, SMS code, passcode, one-time token | Input `result.text` into the focused field |
| Pick point | `LCC.assist.pick_point()` | The operator needs to decide where to tap, such as a visual button or abnormal dialog | Call `touch.tap(result.x, result.y)` |
| Remote control | `LCC.assist.request_control()` | Slider verification, human check, login, security check, permission prompt, or other unstable flow | Wait for the operator to finish, then capture the new screen and continue |

Instructions shown to the operator should be concrete and actionable. Do not use vague text such as "provide more information". Use direct instructions such as "remote-control the device, finish the current verification, then click Done", "enter the captcha in the screenshot", or "pick the center of the confirm button".

## Screenshot Sources

An assist request can include an image in several ways:

- `screenshotLocalPath`: Local image path on the device; the SDK uploads it as a temporary resource on the controller.
- `screenshotPath`: an existing relative path under the control center `files` root.
- `screenshotImage`: an XXTouch `ImageObject`. The SDK converts it to a data URL without saving a file first.
- `screenshotImageData`: PNG/JPEG binary image data. The SDK converts it to a data URL.
- `input.imageSrc`: when the script already has a `data:image/...`, `http(s)://...`, or `/api/...` image URL, pass it through the `input` object for the frontend to display.

The SDK does not overwrite `input.imageSrc`. If `input.imageSrc` and path-based screenshots are not provided, the SDK converts `screenshotImage` or `screenshotImageData` into `input.imageSrc`.

## Lifecycle

Request states are `pending` (waiting), `active` (being handled), `submitted` (result submitted), `cancelled`, and `expired`. Only `submitted` indicates that a human result is available.

If `LCC.assist.request()` times out while waiting, it attempts to cancel that request. On normal script exit, cancellation is attempted for unfinished requests from the current instance. Tasks and results do not survive a controller restart; save results separately if they are needed later.

When the controller receives a device-stopped state, it cancels that device’s `lua-script` assist requests still in `pending` / `active`. This batch cancellation does not affect other devices, other sources, or submitted results.

Automatically uploaded screenshots are cleaned up when the controller starts. Save a separate copy under a resource path you manage for long-term reuse; do not treat the generated `screenshotPath` as a permanent file reference.

Inline images are no longer retained after a request is submitted, cancelled, or expired.

## API List

- [Common Options and Return Objects](./common-options.md)
- [Create an Assist Request `LCC.assist.create()`](./create.md)
- [Wait for an Assist Result `LCC.assist.wait()`](./wait.md)
- [Create and Wait `LCC.assist.request()`](./request.md)
- [Request a Text Reply `LCC.assist.ask_text()`](./ask_text.md)
- [Request a Picked Point `LCC.assist.pick_point()`](./pick_point.md)
- [Request Remote Control `LCC.assist.request_control()`](./request_control.md)
- [Cancel One Request `LCC.assist.cancel()`](./cancel.md)
- [Cancel Current Script Requests `LCC.assist.cancel_all()`](./cancel_all.md)
