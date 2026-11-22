# Copy Files Or Directories (LCC.web_file.copy)

## Signature
```lua
ok, err = LCC.web_file.copy(src, target, mode?, timeout?)
```

## Parameters
- src  
    String. Source path.  
- target  
    String. Destination path.  
- mode  
    String, optional. Copy mode, default `"normal"`; supports `"overwrite"`, `"merge"`, `"overwrite-merge"`.  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- ok  
    Boolean. `true` on success, `nil` on failure.  
- err  
    String or `nil`. Error description when the copy fails.  

## Notes
> Copies files or whole directories.  
> When `src` is a symlink, the link itself is copied rather than the target content.  
> `normal` mode refuses to overwrite existing targets; the other modes behave just like the convenience helpers.  
> Returns `nil, err` when the path is invalid or conflicts occur.  

## Example
```lua
local ok, err = LCC.web_file.copy("/templates", "/backup/templates")
if not ok then
    error(err)
end
```
