# Create and Wait (LCC.assist.request)

## Declaration

```lua
result, err, task = LCC.assist.request(options)
```

## Parameters

- options  
    Table. Assist request configuration. See [Common Options and Return Objects](./common-options.md).

## Return Values

- result  
    Table or `nil`. The submitted result object on success.
- err  
    String or `nil`. Failure reason, such as `"cancelled"`, `"expired"`, or `"timeout"`.
- task  
    Table or `nil`. The latest task state.

## Notes

> `request()` calls `LCC.assist.create(options)` to create the request, then calls `LCC.assist.wait(task.id, options.timeout, options.pollIntervalMs)` to block until a result is available.  
> In most scripts, prefer `ask_text()`, `pick_point()`, or `request_control()` because they set the request type automatically.  
> On wait timeout, the SDK attempts to cancel the request and returns `nil, "timeout", task`; `"timeout"` does not confirm successful cancellation on the controller.  

## Example

```lua
local result, err, task = LCC.assist.request({
    type = "control",
    title = "Handle verification",
    text = "Remote-control the device, finish the current verification, then click Done",
    timeout = 300,
})

if not result then
    nLog("assist request not completed", err, task and task.status)
end
```
