# Write Key And Return Previous Value (LCC.kvdb.dict.put)

## Signature
```lua
old_value, err = LCC.kvdb.dict.put(name, key, value, timeout?)
```

## Parameters
- name  
    String. Dictionary name (non-empty, max `256` bytes).  
- key  
    String. Key (must be valid UTF-8 and non-empty).  
- value  
    String. New value (must be valid UTF-8).  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- old_value  
    String or `nil`. Previous value when the key existed; `nil` for new keys.  
- err  
    String or `nil`. `nil` on success; contains the error message when the request fails.

## Notes
> Writes a key and atomically returns its previous value—useful for "set-and-get-old" operations.  
> When the request fails, the function returns `false` followed by the error message.  

## Example
```lua
local old, err = LCC.kvdb.dict.put("settings", "retry", "3")
if old == false then
    error(err)
end
```
