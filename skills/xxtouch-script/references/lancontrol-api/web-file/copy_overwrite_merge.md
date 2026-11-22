# Copy With Overwrite-And-Merge (LCC.web_file.copy_overwrite_merge)

## Signature
```lua
ok, err = LCC.web_file.copy_overwrite_merge(src, target, timeout?)
```

## Parameters
- src  
    String. Source path.  
- target  
    String. Destination path.  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- ok  
    Boolean. `true` on success, `nil` on failure.  
- err  
    String or `nil`. Error description when the copy fails.  

## Notes
> Alias for `web_file.copy` with `mode = "overwrite-merge"`.  
> Overwrites files that exist at the destination, then fills in missing entries.  

## Example
```lua
local ok, err = LCC.web_file.copy_overwrite_merge("/templates", "/deploy/templates")
if not ok then
    error(err)
end
```
