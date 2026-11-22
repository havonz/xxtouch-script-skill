# Overwrite With Multiple Lines (LCC.web_file.set_lines)

## Signature
```lua
ok, err = LCC.web_file.set_lines(path, lines, timeout?)
```

## Parameters
- path  
    String. File to write.  
- lines  
    Table. Ordered array of strings.  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- ok  
    Boolean. `true` on success, `false` on failure.  
- err  
    String or `nil`. Error description when the write fails.  

## Notes
> Joins the lines and replaces the entire file.  
> Missing parent directories and the file itself are created automatically.  
> Ideal for rebuilding configuration or template files.  

## Example
```lua
local ok, err = LCC.web_file.set_lines("/config/list.txt", {"A", "B", "C"})
if not ok then
    error(err)
end
```
