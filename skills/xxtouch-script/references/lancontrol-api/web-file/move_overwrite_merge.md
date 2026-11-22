# Move With Overwrite-And-Merge (LCC.web_file.move_overwrite_merge)

## Signature
```lua
ok, err = LCC.web_file.move_overwrite_merge(src, target, timeout?)
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
> Wrapper for `web_file.move` with `mode = "overwrite-merge"`.  
> Overwrites files that exist and moves the remaining missing items.  

## Example
```lua
local ok, err = LCC.web_file.move_overwrite_merge("/assets/temp", "/assets/live")
if not ok then
    error(err)
end
```
