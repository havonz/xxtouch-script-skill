# Configure Request Retries (LCC.set_retry_count)

## Signature
```lua
LCC.set_retry_count(retry_count)
```

## Parameters
- retry_count  
    Integer. When `> 0` it limits the number of extra retries; `<= 0` means retry indefinitely until a definitive result is returned.  

## Returns
- none  

## Notes
> Controls the timeout/retry behaviour for every controller-side API that the module calls.  
> For network failures or `5xx` responses the module waits 1 second and retries until the limit is reached or the call succeeds.  
> The default is `0` (retry forever). Leave it as-is in automated scenarios, or cap it in ad-hoc scripts to avoid blocking.  

## Example
```lua
LCC.set_retry_count(5)  -- retry at most 5 additional times
```
