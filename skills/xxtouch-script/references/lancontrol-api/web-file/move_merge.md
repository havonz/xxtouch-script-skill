# Move And Merge Missing Items (LCC.web_file.move_merge)

## Signature
```lua
ok, err = LCC.web_file.move_merge(src, target, timeout?)
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
> Shorthand for `web_file.move` with `mode = "merge"`.  
> Keeps existing files at the destination and only moves missing ones.  

## Example
```lua
local ok, err = LCC.web_file.move_merge("/assets/temp", "/assets/live")
if not ok then
    error(err)
end
```
