# Move And Overwrite (LCC.web_file.move_overwrite)

## Signature
```lua
ok, err = LCC.web_file.move_overwrite(src, target, timeout?)
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
    String or `nil`. Error description when the move fails.  

## Notes
> Wrapper for `web_file.move` with `mode = "overwrite"`.  
> Existing targets are deleted before moving.  

## Example
```lua
local ok, err = LCC.web_file.move_overwrite("/logs/current.log", "/logs/history.log")
if not ok then
    error(err)
end
```
