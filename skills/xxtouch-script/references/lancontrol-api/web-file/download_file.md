# Download Controller File To Device (LCC.web_file.download_file)

## Signature
```lua
ok, err = LCC.web_file.download_file(path, target_path, timeout?)
```

## Parameters
- path  
    String. Source path on the controller.  
- target_path  
    String. Absolute destination path on the device.  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- ok  
    Boolean. `true` when the download succeeds, `false` otherwise.  
- err  
    String or `nil`. Error description when the operation fails.  

## Notes
> Downloads a file from the controller and saves it to the device.  
> Returns `false` if the target directory is missing or the write fails.  

## Example
```lua
local ok, err = LCC.web_file.download_file("/scripts/main.lua", XXT_SCRIPTS_PATH.."/cache.lua")
if not ok then
    error(err)
end
```
