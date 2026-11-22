# Copy And Merge Missing Items (LCC.web_file.copy_merge)

## Signature
```lua
ok, err = LCC.web_file.copy_merge(src, target, timeout?)
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
> Shortcut for `web_file.copy` with `mode = "merge"`.  
> Only missing files/directories are added; existing ones stay untouched.  

## Example
```lua
local ok, err = LCC.web_file.copy_merge("/templates", "/deploy/templates")
if not ok then
    error(err)
end
```
