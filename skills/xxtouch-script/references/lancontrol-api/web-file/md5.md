# Calculate File MD5 (LCC.web_file.md5)

## Signature
```lua
hash, err = LCC.web_file.md5(path, timeout?)
```

## Parameters
- path  
    String. File to hash.  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- hash  
    String. 32-character hexadecimal MD5 digest; `nil` on failure.  
- err  
    String or `nil`. Error description when the call fails.  

## Notes
> Computes the file's MD5 digest on the controller.  
> Applies to files only; returns `nil` when the path is missing or a directory.  

## Example
```lua
local md5, err = LCC.web_file.md5("/scripts/main.lua")
if md5 then
    print("MD5=" .. md5)
end
```
