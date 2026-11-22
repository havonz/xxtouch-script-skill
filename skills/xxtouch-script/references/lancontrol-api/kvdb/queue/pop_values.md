# Remove Items By Value (LCC.kvdb.queue.pop_values)

## Signature
```lua
count, err = LCC.kvdb.queue.pop_values(name, value, timeout?)
```

## Parameters
- name  
    String. Queue name (non-empty, max `256` bytes).  
- value  
    String. Value to delete everywhere (must be valid UTF-8).  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- count  
    Number. Number of removed items; `nil` on failure.  
- err  
    String or `nil`. Error description when the call fails.  

## Notes
> Atomically removes every entry matching the given value.  
> The return value reports how many items were removed.  

## Example
```lua
local removed, err = LCC.kvdb.queue.pop_values("pending", "timeout")
if removed then
    LCC.log(2, "Purged stale tasks", removed)
end
```
