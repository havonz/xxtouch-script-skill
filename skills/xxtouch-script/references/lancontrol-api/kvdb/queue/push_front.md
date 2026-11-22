# Push To Queue Front (LCC.kvdb.queue.push_front)

## Signature
```lua
size, err = LCC.kvdb.queue.push_front(name, value, timeout?)
```

## Parameters
- name  
    String. Queue name (non-empty, max `256` bytes).  
- value
    String, or a continuous string array. Strings must be valid UTF-8.
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- size  
    Number. Queue length after the push; `nil` on failure.  
- err  
    String or `nil`. Error message when the call fails.  

## Notes
> Pushes an item onto the head of the queue.  
> Batch pushes preserve array order. For example, `{"a", "b"}` becomes the new head `a, b, ...`.
> Queue names cannot be empty.  

## Example
```lua
local size, err = LCC.kvdb.queue.push_front("pending", "task#1")
if size then
    LCC.log(1, "Queue size", size)
end

local batch_size, batch_err = LCC.kvdb.queue.push_front("pending", {"task#2", "task#3"})
```
