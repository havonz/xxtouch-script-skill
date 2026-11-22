# Delete Files Or Directories (LCC.web_file.delete)

## Signature
```lua
ok, err = LCC.web_file.delete(path, force?, timeout?)
```

## Parameters
- path  
    String. File or directory path to remove.  
- force  
    Boolean, optional. Set to `true` to delete non-empty directories; default `false`.  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- ok  
    Boolean. `true` on success, `false` on failure.  
- err  
    String or `nil`. Error description; when the target is missing it's `'not found'`.  

## Notes
> Deletes the specified file or directory.  
> Deleting a non-empty directory without `force` fails.  
> Missing targets return `false, 'not found'`.  

## Example
```lua
local ok, err = LCC.web_file.delete("/reports/temp.txt")
if not ok then
    LCC.log(3, "Delete failed", err)
end
```
