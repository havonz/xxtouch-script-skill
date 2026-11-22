# Move A Key (LCC.kvdb.dict.move_value)

## Signature
```lua
ok, old_value_or_err = LCC.kvdb.dict.move_value(src_name, src_key, dst_name?, dst_key?, timeout?)
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
    String or `nil`. Previous value at the destination (or `nil` when absent); on failure it usually contains an error description, but missing source keys do not guarantee a fixed message.

## Notes
> Atomically transfers the key from the source dictionary to the destination.  
> When source and destination are identical, the function raises an error.  
> A successful move with no previous destination value yields `true, nil`.  
> Missing source keys return `false`, and the second return value does not guarantee a fixed message.

## Example
```lua
local ok, old = LCC.kvdb.dict.move_value("pending", "task#1", "running", "task#1")
if not ok then
    error(old)
end
```
