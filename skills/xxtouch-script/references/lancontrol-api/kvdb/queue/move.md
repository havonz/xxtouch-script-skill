# Atomically Move Queue Items (LCC.kvdb.queue.move)

## Signature
```lua
value, err = LCC.kvdb.queue.move(from_name, pop?, to_name, push?, timeout?)
```

## Parameters
- from_name  
    String. Source queue name (non-empty, max `256` bytes).  
- pop  
    String, optional. Pop direction of the source queue, `"front"` or `"back"`; defaults to `"front"`.  
- to_name  
    String. Destination queue name (non-empty, max `256` bytes).  
- push  
    String, optional. Push direction for the destination queue, `"front"` or `"back"`; defaults to `"back"`.  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- value  
    String. The moved entry; `nil` when the source queue is empty.  
- err  
    String or `nil`. Returns `'not found'` on empty source queues or when the operation fails.  

## Notes
> Atomically pops from the source queue and pushes into the destination.  
> Ideal for task hand-offs without race conditions.  
> Returns `nil, 'not found'` when the source queue is empty.  

## Example
```lua
local value, err = LCC.kvdb.queue.move("pending", "front", "running", "back")
if value then
    print("Claimed", value)
end
```
