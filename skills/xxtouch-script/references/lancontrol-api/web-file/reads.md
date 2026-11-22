# Read Controller File Content (LCC.web_file.reads)

## Signature
```lua
data, err = LCC.web_file.reads(path, timeout?)
```

## Parameters
- path  
    String. File path to read.  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- data  
    String. File content; `nil` on failure.  
- err  
    String or `nil`. Error description when the call fails.  

## Notes
> Reads text or binary content from the controller.  
> Returned data is raw, so binary files can be written directly to the device.  

## Example
```lua
local content, err = LCC.web_file.reads("/config/app.conf")
if not content then
    error(err)
end
```
