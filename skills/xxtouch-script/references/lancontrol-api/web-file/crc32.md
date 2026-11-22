# Calculate File CRC32 (LCC.web_file.crc32)

## Signature
```lua
checksum, err = LCC.web_file.crc32(path, timeout?)
```

## Parameters
- path  
    String. File to check.  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- checksum  
    String. 8-character hexadecimal CRC32; `nil` on failure.  
- err  
    String or `nil`. Error description when the call fails.  

## Notes
> Computes the file's CRC32 checksum on the controller.  
> Useful for quick integrity verification.  

## Example
```lua
local crc32, err = LCC.web_file.crc32("/firmware/patch.bin")
if crc32 then
    print("CRC32=" .. crc32)
end
```
