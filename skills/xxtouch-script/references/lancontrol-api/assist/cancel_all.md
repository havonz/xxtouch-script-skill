# Cancel Current Script Requests (LCC.assist.cancel_all)

## Declaration

```lua
count = LCC.assist.cancel_all(timeout?)
```

## Parameters

- timeout  
    Number, optional. Per-request cancel timeout in seconds. Defaults to `5`.

## Return Values

- count  
    Number. Count of successfully cancelled requests.

## Notes

> Cancels only unfinished requests created and still tracked by the current script instance.  
> It does not cancel requests from other devices or requests created by other script instances.  
> When the script exits, the SDK automatically calls `cancel_all(3)` to clean up unfinished requests.  

## Example

```lua
local count = LCC.assist.cancel_all()
nLog("cancelled assist requests", count)
```
