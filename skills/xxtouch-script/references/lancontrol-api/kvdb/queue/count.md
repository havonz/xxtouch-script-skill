# Count Value Occurrences (LCC.kvdb.queue.count)

## Signature
```lua
count, err = LCC.kvdb.queue.count(name, value, timeout?)
```

## Parameters
- name  
    String. Queue name (non-empty, max `256` bytes).  
- value  
    String. Value to count within the queue (must be valid UTF-8).  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- count  
    Number. Occurrence count; `nil` on failure.  
- err  
    String or `nil`. Error description when the call fails.  

## Notes
> Counts how many times the given value appears in the queue (server-side).  
> Useful for rate limiting or queue monitoring.  

## Example
```lua
local cnt, err = LCC.kvdb.queue.count("pending", "timeout")
if cnt then
    print("Tasks pending retry:", cnt)
end
```
