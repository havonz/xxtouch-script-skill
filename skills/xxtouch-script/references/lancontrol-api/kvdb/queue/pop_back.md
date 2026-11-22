# Pop From Queue Back (LCC.kvdb.queue.pop_back)

## Signature
```lua
value, err = LCC.kvdb.queue.pop_back(name, timeout?)
values, err = LCC.kvdb.queue.pop_back({name = name, max = n}, timeout?)
```

## Parameters
- name
    String. Queue name (non-empty, max `256` bytes). Pass `{name = "...", max = n}` for batch pop.
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- value  
    String. Item removed from the tail; `nil` when the queue is empty.  
- values
    String array. Items removed in batch mode; `{}` when the queue is empty.
- err
    String or `nil`. Single-value mode returns `'not found'` when the queue is empty or missing.

## Notes
> Removes and returns the last element from the queue.  
> Batch mode returns up to `max` items in actual pop order.
> Handy for LIFO-style consumption.  

## Example
```lua
local value, err = LCC.kvdb.queue.pop_back("pending")
if value then
    print("Processing latest task", value)
end

local values, batch_err = LCC.kvdb.queue.pop_back({name = "pending", max = 3})
for _, item in ipairs(values or {}) do
    print("Processing latest task", item)
end
```
