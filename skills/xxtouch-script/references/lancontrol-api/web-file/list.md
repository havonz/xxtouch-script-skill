# List Files On The Controller (LCC.web_file.list)

## Signature
```lua
list, err = LCC.web_file.list(path, recursive?, timeout?)
```

## Parameters
- path  
    String. Directory path on the controller to inspect.  
- recursive  
    Boolean, optional. When `true`, lists subfolders recursively; default `false`.  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- list  
    Table. Array of file/directory descriptors from the controller; `nil` on failure.  
- err  
    String or `nil`. Error description when the call fails.  

## Notes
> Lists files and subdirectories under the given path.  
> Requires the controller address to be set or the script to be launched by the controller.  
> Each entry includes `name`, `path`, `dir`, `symlink`, `size`, and `modification`.  
> `symlink` indicates whether the entry itself is a symlink; when the target is reachable, `dir` and `size` reflect the target state.  

## Example
```lua
local nodes, err = LCC.web_file.list("/scripts", true)
if not nodes then
    error(err)
end
```
