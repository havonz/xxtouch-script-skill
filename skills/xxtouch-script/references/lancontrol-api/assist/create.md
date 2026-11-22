# Create an Assist Request (LCC.assist.create)

## Declaration

```lua
task, err = LCC.assist.create(options)
```

## Parameters

- options  
    Table. Assist request configuration. See [Common Options and Return Objects](./common-options.md).

## Return Values

- task  
    Table or `nil`. The control-center task object on success.
- err  
    String or `nil`. Failure reason.

## Notes

> Creates the task only and does not wait for a human result.  
> If `screenshotLocalPath` is provided, the SDK uploads the local device screenshot before creating the task.  
> If `screenshotImage` or `screenshotImageData` is provided, the SDK converts it to a data URL and sends it in the request body without saving a file first.  
> Use `cancel_all()` to cancel all unfinished requests from the current script.  
> Script-created tasks automatically set `deviceId = device.udid()` and `source = "lua-script"`.  

## Example

```lua
local task, err = LCC.assist.create({
    type = "control",
    title = "Handle verification",
    text = "Remote-control the device, finish the current verification, then click Done",
    timeout = 300,
})

if not task then
    nLog("failed to create assist request", err)
    return
end

local result, waitErr = LCC.assist.wait(task.id, 300, 1000)
if not result then
    nLog("assist request not completed", waitErr)
end
```
