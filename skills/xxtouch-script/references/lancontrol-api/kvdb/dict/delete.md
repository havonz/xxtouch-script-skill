# Delete A Key (LCC.kvdb.dict.delete)

## Signature
```lua
value, err = LCC.kvdb.dict.delete(name, key, timeout?)
```

## Parameters
- name  
    String. Dictionary name (non-empty, max `256` bytes).  
- key  
    String. Key to remove (must be valid UTF-8 and non-empty).  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- value  
    String. Removed value; `nil` when the key was absent.  
- err  
    String or `nil`. Returns `'not found'` when nothing was deleted, or an error description for other failures.  

## Notes
> Deletes the specified key and returns its previous value.  
> Handy for read-and-delete workflows when paired with `get`.  

## Example
```lua
local old, err = LCC.kvdb.dict.delete("settings", "temporary")
if old then
    LCC.log(2, "Removed stale config", old)
end
```
