# Move Files Or Directories (LCC.web_file.move)

## Signature
```lua
ok, err = LCC.web_file.move(src, target, mode?, timeout?)
```

## Parameters
- src  
    String. Source path.  
- target  
    String. Destination path.  
- mode  
    String, optional. Move mode, default `"normal"`; supports `"overwrite"`, `"merge"`, `"overwrite-merge"`.  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- ok  
    Boolean. `true` on success, `nil` on failure.  
- err  
    String or `nil`. Error description when the move fails.  

## Notes
> Moves files or directories; also useful for renaming.  
> When `src` is a symlink, the move operates on the link itself and does not rewrite or remove the target content.  
> In `normal` mode the operation fails if the target already exists; other modes behave like their shorthand helpers.  

## Example
```lua
local ok, err = LCC.web_file.move("/scripts/temp.lua", "/scripts/main.lua", "overwrite")
if not ok then
    error(err)
end
```
