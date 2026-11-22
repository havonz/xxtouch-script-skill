# Clear Entire Queue (LCC.kvdb.queue.clear)

## Signature
```lua
values, err = LCC.kvdb.queue.clear(name, timeout?)
```

## Parameters
- name  
    String. Queue name (non-empty, max `256` bytes).  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- values  
    Table. Array of elements before clearing; returns an empty array when the queue was already empty, or `nil` on failure.  
- err  
    String or `nil`. Error description when the call fails.  

## Notes
> Clears the queue and returns a snapshot of the previous items.  
> Handy for resetting queue state or migrating data.  

## Example
```lua
local removed, err = LCC.kvdb.queue.clear("pending")
if removed then
    LCC.log(1, "Queue cleared", #removed)
end
```
