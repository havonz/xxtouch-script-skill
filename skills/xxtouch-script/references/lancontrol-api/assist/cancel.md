# Cancel One Request (LCC.assist.cancel)

## Declaration

```lua
ok, err, task = LCC.assist.cancel(id, timeout?)
```

## Parameters

- id  
    String. Assist request ID.
- timeout  
    Number, optional. Cancel request timeout in seconds. Defaults to `10`.

## Return Values

- ok  
    Boolean. `true` when cancellation succeeds; otherwise `false`.
- err  
    String or `nil`. Failure reason.
- task  
    Table or `nil`. The cancelled task object.

## Notes

> Cancels one unfinished assist request.  
> After a cancellation returns a failure, `LCC.assist.cancel_all()` will not retry that task. Keep its ID; if cancellation must be retried, call `LCC.assist.cancel(id)` explicitly and check `ok` and `err`.  

## Example

```lua
local ok, err, task = LCC.assist.cancel(taskId)
if not ok then
    nLog("failed to cancel assist request", err)
end
```
