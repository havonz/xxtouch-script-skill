# Count Lines (LCC.web_file.line_count)

## Signature
```lua
count, err = LCC.web_file.line_count(path, timeout?)
```

## Parameters
- path  
    String. File whose lines should be counted.  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- count  
    Number. Total lines; `nil` on failure.  
- err  
    String or `nil`. Error description when the call fails.  

## Notes
> Returns the file's line count more efficiently than calling `get_lines` and then counting the result.  
> Works well for large files.  

## Example
```lua
local count, err = LCC.web_file.line_count("/logs/task.log")
if count then
    print("Log lines:" .. count)
end
```
