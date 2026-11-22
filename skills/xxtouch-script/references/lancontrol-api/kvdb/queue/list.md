# List Queue Contents (LCC.kvdb.queue.list)

## Signature
```lua
values, err = LCC.kvdb.queue.list(name, timeout?)
```

## Parameters
- name  
    String. Queue name (non-empty, max `256` bytes).  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- values  
    Table. Array of strings in queue order; returns an empty array when the queue is empty, or `nil` on failure.  
- err  
    String or `nil`. Error description when the call fails.  

## Notes
> Returns a snapshot of the entire queue.  
> The array preserves order (index 1 equals the head of the queue).  
> An empty queue returns an empty array, not `nil`.  

## Example
```lua
local values, err = LCC.kvdb.queue.list("pending")
if values then
    for i, v in ipairs(values) do
        print(i, v)
    end
end
```
