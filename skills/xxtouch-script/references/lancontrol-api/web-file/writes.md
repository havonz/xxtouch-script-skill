# Overwrite Controller File Content (LCC.web_file.writes)

## Signature
```lua
ok, err = LCC.web_file.writes(path, data, timeout?)
```

## Parameters
- path  
    String. Destination file path.  
- data  
    String. Content to write.  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- ok  
    Boolean. `true` when the write succeeds, `false` otherwise.  
- err  
    String or `nil`. Error description when the operation fails.  

## Notes
> Replaces the file contents completely.  
> Missing parent directories and the file itself are created automatically.  
> To write binary data, ensure the string carries the raw bytes.  

## Example
```lua
local ok, err = LCC.web_file.writes("/config/app.conf", "mode=auto\n")
if not ok then
    error(err)
end
```
