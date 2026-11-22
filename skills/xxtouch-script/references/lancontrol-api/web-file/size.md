# Get Path Size (LCC.web_file.size)

## Signature
```lua
size, err = LCC.web_file.size(path, timeout?)
```

## Parameters
- path  
    String. File to inspect.  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- size  
    Number. Size when the path exists; `nil` otherwise.  
- err  
    String or `nil`. Returns `'not found'` when the size cannot be determined.

## Notes
> Regular files return their byte size; directories currently return `0`.  
> Returns `nil, 'not found'` whenever the size cannot be determined.  

## Example
```lua
local size, err = LCC.web_file.size("/reports/log.txt")
if size then
    print("Log size: " .. size .. " bytes")
end
```
