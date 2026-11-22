# Append To Controller File (LCC.web_file.appends)

## Signature
```lua
ok, err = LCC.web_file.appends(path, data, timeout?)
```

## Parameters
- path  
    String. File path to append.  
- data  
    String. Content to append.  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- ok  
    Boolean. `true` on success, `false` on failure.  
- err  
    String or `nil`. Error description when the operation fails.  

## Notes
> Appends data to the end of the file.  
> Missing parent directories and the target file are created automatically.  
> Useful for continuously extending logs or export records.  

## Example
```lua
local ok, err = LCC.web_file.appends("/logs/task.log", "Finished at 2024-01-01\n")
if not ok then
    LCC.log(3, "Append failed", err)
end
```
