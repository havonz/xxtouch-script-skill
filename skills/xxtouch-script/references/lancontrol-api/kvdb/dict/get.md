# Read A Key (LCC.kvdb.dict.get)

## Signature
```lua
value, err = LCC.kvdb.dict.get(name, key, timeout?)
```

## Parameters
- name  
    String. Dictionary name (non-empty, max `256` bytes).  
- key  
    String. Key to read (must be valid UTF-8 and non-empty).  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- value  
    String. Value stored for the key; `nil` when missing.  
- err  
    String or `nil`. Returns `'not found'` when the key is absent, or an error description for other failures.  

## Notes
> Fetches the value for the given key.  
> Missing keys return `nil, 'not found'`.  

## Example
```lua
local value, err = LCC.kvdb.dict.get("settings", "retry")
if value then
    print("Current retry count:", value)
end
```
