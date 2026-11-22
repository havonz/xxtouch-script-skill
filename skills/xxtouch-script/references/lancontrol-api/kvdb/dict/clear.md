# Clear Dictionary (LCC.kvdb.dict.clear)

## Signature
```lua
values, err = LCC.kvdb.dict.clear(name, timeout?)
```

## Parameters
- name  
    String. Dictionary name (non-empty, max `256` bytes).  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- values  
    Table. Snapshot of key/value pairs before clearing; returns an empty table when the dictionary was already empty, or `nil` on failure.  
- err  
    String or `nil`. Error description when the call fails.  

## Notes
> Clears every key in the dictionary and returns a snapshot of the previous entries.  
> The returned value can be serialized as a backup.  

## Example
```lua
local values, err = LCC.kvdb.dict.clear("cache")
if values then
    local count = 0
    for _ in pairs(values) do count = count + 1 end
    LCC.log(1, "Cache cleared", count)
end
```
