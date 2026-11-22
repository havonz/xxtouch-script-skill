# Insert A Single Line (LCC.web_file.insert_line)

## Signature
```lua
ok, err = LCC.web_file.insert_line(path, line_number, line, timeout?)
```

## Parameters
- path  
    String. File path.  
- line_number  
    Number. Reference line index for insertion. Positive numbers start at `1` and insert before that line; negative values count from the end, `0` appends after the last line, and `-1` inserts before the last line.  
- line  
    String. Text to insert.  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- ok  
    Boolean. `true` on success, `false` on failure.  
- err  
    String or `nil`. Error description when the operation fails.  

## Notes
> Inserts one line before the specified line index.  
> See the parameter description above for line-number rules.  
> Useful for inserting new configuration or log content after a fixed heading.  

## Example
```lua
local ok, err = LCC.web_file.insert_line("/config/list.txt", 1, "Header")
if not ok then
    error(err)
end
```
