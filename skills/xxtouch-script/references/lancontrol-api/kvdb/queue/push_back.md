# Push To Queue Back (LCC.kvdb.queue.push_back)

## Signature
```lua
size, err = LCC.kvdb.queue.push_back(name, value, timeout?)
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
    String or `nil`. Error description when the call fails.  

## Notes
> Pushes an item onto the tail of the queue.  
> Batch pushes preserve array order. For example, `{"a", "b"}` becomes the new tail `..., a, b`.
> Shares the same constraints as `push_front`.  

## Example
```lua
local size, err = LCC.kvdb.queue.push_back("pending", "task#2")
if not size then
    error(err)
end

local batch_size, batch_err = LCC.kvdb.queue.push_back("pending", {"task#3", "task#4"})
```
