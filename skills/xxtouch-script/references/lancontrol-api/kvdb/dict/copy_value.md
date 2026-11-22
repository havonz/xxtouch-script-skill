# Copy A Key (LCC.kvdb.dict.copy_value)

## Signature
```lua
ok, old_value_or_err = LCC.kvdb.dict.copy_value(src_name, src_key, dst_name?, dst_key?, timeout?)
```

## Parameters
- src_name  
    String. Source dictionary name (non-empty, max `256` bytes).  
- src_key  
    String. Source key (must be valid UTF-8 and non-empty).  
- dst_name  
    String, optional. Destination dictionary name, defaults to the source name (non-empty, max `256` bytes).  
- dst_key  
    String, optional. Destination key, defaults to the source key (must be valid UTF-8 and non-empty).  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- ok  
    Boolean. `true` on success, `false` on failure.  
- old_value_or_err  
    String or `nil`. Previous value at the destination (or `nil` when absent); on failure returns an error description.  

## Notes
> Copies the value to the destination key; the source key is preserved.  
> When source and destination are identical it simply returns the existing value while reporting success.  
> Missing source keys return `false`.  

## Example
```lua
local ok, old = LCC.kvdb.dict.copy_value("templates", "default", "user", "default")
if not ok then
    error(old)
end
```
