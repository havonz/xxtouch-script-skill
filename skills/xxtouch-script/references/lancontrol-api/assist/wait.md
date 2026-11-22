# Wait for an Assist Result (LCC.assist.wait)

## Declaration

```lua
result, err, task = LCC.assist.wait(id, timeout?, pollIntervalMs?)
```

## Parameters

- id  
    String. Assist request ID.
- timeout  
    Number, optional. Wait timeout in seconds. Defaults to `300`.
- pollIntervalMs  
    Number, optional. Polling interval in milliseconds. Defaults to `1000`; values below `250` are clamped to `250`.

## Return Values

- result  
    Table or `nil`. Submitted result when the task reaches `submitted`.
- err  
    String or `nil`. Failure reason.
- task  
    Table or `nil`. The latest task state.

## Notes

> Polls the control center until the task is submitted, cancelled, expired, not found, or timed out locally.  
> On local timeout, the SDK attempts to cancel the request and returns `nil, "timeout", task`.  
> Only `submitted` returns a `result`.  

## Example

```lua
local result, err, task = LCC.assist.wait("assist_xxx", 300, 1000)
if result then
    nLog("assist completed")
else
    nLog("assist failed", err, task and task.status)
end
```
