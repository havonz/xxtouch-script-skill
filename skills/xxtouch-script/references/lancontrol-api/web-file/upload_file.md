# Upload Device File To Controller (LCC.web_file.upload_file)

## Signature
```lua
ok, err = LCC.web_file.upload_file(local_path, remote_path, timeout?)
```

## Parameters
- local_path  
    String. Source path on the device.  
- remote_path  
    String. Destination path on the controller.  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- ok  
    Boolean. `true` on success, `false` on failure.  
- err  
    String or `nil`. Error description when the upload fails.  

## Notes
> Uploads a local device file to the controller, overwriting any existing file.  
> Missing parent directories are created automatically.  

## Example
```lua
local ok, err = LCC.web_file.upload_file(XXT_SCRIPTS_PATH.."/result.txt", "/result.txt")
if not ok then
    error(err)
end
```
