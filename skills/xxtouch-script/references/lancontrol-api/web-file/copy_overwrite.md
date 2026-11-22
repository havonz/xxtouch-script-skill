# Copy And Overwrite (LCC.web_file.copy_overwrite)

## Signature
```lua
ok, err = LCC.web_file.copy_overwrite(src, target, timeout?)
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
> Convenience wrapper around `web_file.copy` with `mode = "overwrite"`.  
> Existing targets are deleted before copying.  

## Example
```lua
local ok, err = LCC.web_file.copy_overwrite("/scripts", "/deploy/scripts")
if not ok then
    error(err)
end
```
