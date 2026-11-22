# Calculate File SHA1 (LCC.web_file.sha1)

## Signature
```lua
hash, err = LCC.web_file.sha1(path, timeout?)
```

## Parameters
- path  
    String. File to hash.  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- hash  
    String. 40-character hexadecimal SHA1 digest; `nil` on failure.  
- err  
    String or `nil`. Error description when the call fails.  

## Notes
> Computes the file's SHA1 digest on the controller.  
> Returns `nil` with an error message when the path is missing or not a file.  

## Example
```lua
local sha1, err = LCC.web_file.sha1("/assets/config.json")
if sha1 then
    print("SHA1=" .. sha1)
end
```
