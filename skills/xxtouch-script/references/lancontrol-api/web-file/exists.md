# Check Path Existence (LCC.web_file.exists)

## Signature
```lua
type_or_false = LCC.web_file.exists(path, timeout?)
```

## Parameters
- path  
    String. File or directory to check.  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- type_or_false  
    String or boolean. Returns `"file"` or `"directory"` when present, otherwise `false`.  

## Notes
> Checks whether a path exists and returns its type.  
> It does not raise errors; network failures also yield `false`.  

## Example
```lua
local typ = LCC.web_file.exists("/scripts/main.lua")
if typ == "file" then
    print("Script found")
end
```
