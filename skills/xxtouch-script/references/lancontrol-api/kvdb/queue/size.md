# Retrieve Queue Length (LCC.kvdb.queue.size)

## Signature
```lua
size, err = LCC.kvdb.queue.size(name, timeout?)
```

## Parameters
- name  
    String. Queue name (non-empty, max `256` bytes).  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- size  
    Number. Current number of items; returns `0` for empty queues, or `nil` on failure.  
- err  
    String or `nil`. Error description when the call fails.  

## Notes
> Returns the queue length directly, faster than calling `list` and counting.  
> Empty queues return `0`.  

## Example
```lua
local size, err = LCC.kvdb.queue.size("pending")
if size then
    print("Queued:", size)
end
```
