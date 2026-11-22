# Pop From Queue Front (LCC.kvdb.queue.pop_front)

## Signature
```lua
value, err = LCC.kvdb.queue.pop_front(name, timeout?)
values, err = LCC.kvdb.queue.pop_front({name = name, max = n}, timeout?)
```

## Parameters
- name
    String. Queue name (non-empty, max `256` bytes). Pass `{name = "...", max = n}` for batch pop.
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- value  
    String. The item removed from the head; `nil` when the queue is empty.  
- values
    String array. Items removed in batch mode; `{}` when the queue is empty.
- err
    String or `nil`. Single-value mode returns `'not found'` when the queue is empty or missing.

## Notes
> Removes and returns the first element from the queue.  
> Batch mode returns up to `max` items in actual pop order.
> Returns `nil, 'not found'` when the queue is empty.  

## Example
```lua
local value, err = LCC.kvdb.queue.pop_front("pending")
if value then
    print("Processing", value)
end

local values, batch_err = LCC.kvdb.queue.pop_front({name = "pending", max = 3})
for _, item in ipairs(values or {}) do
    print("Processing", item)
end
```
