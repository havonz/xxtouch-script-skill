# Create A Controller Directory (LCC.web_file.mkdir)

## Signature
```lua
ok, err = LCC.web_file.mkdir(path, timeout?)
```

## Parameters
- path  
    String. Directory to create.  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- ok  
    Boolean. `true` on success, `false` on failure.  
- err  
    String or `nil`. Error description when the operation fails.  

## Notes
> Creates a directory, including any missing parent directories.  
> When the directory already exists the call is still considered successful.  
> Any controller-side error text is forwarded unchanged.  

## Example
```lua
local ok, err = LCC.web_file.mkdir("/backups", 30)
if not ok then
    LCC.log(2, "Failed to create directory", err)
end
```
