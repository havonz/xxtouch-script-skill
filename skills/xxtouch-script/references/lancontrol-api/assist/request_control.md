# Request Remote Control (LCC.assist.request_control)

## Declaration

```lua
result, err, task = LCC.assist.request_control(options)
```

## Parameters

- options  
    Table. Assist request configuration. See [Common Options and Return Objects](./common-options.md). This function sets `type = "control"` automatically.

## Return Values

- result  
    Table or `nil`. The submitted result on success. Clicking Done returns `{ kind = "device-control", completed = true }`. Expanding Manual Submit and submitting valid JSON returns the Lua table decoded from that JSON; submitting plain text returns `{ note = "text content" }`.
- err  
    String or `nil`. Failure reason.
- task  
    Table or `nil`. The latest task state.

## Notes

> Use this for slider verification, human checks, login, security checks, permission prompts, and complex flows where the script should not keep guessing.  
> The operator remote-controls the device, finishes the step, clicks Done, and the script continues.  
> Make the `text` field clearly state what the operator needs to finish.  

Done and Manual Submit are different submit paths:

- Click Done when the operator only needs to mark the remote-control work complete. It always returns `{ kind = "device-control", completed = true }`.
- Click Submit inside Manual Submit when the operator needs to return extra information to the script. Valid JSON is returned as structured data; non-JSON text is returned as `{ note = "..." }`; empty content is not submitted.

## Example

```lua
local result, err = LCC.assist.request_control({
    title = "Handle verification",
    text = "Remote-control the device, finish verification, then click Done",
    timeout = 300,
})

if not result then
    nLog("remote control not completed", err)
end
```

Pass the current screenshot directly:

```lua
local img = screen.image()

local result, err = LCC.assist.request_control({
    title = "Need human handling",
    text = "Remote-control the device, finish the current verification, then click Done",
    screenshotImage = img,
    screenshotImageQuality = 0.6,
    timeout = 300,
})

if img.destroy then
    img:destroy()
end
```
