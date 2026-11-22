# Read A Range Of Lines (LCC.web_file.get_range_lines)

## Signature
```lua
lines, err = LCC.web_file.get_range_lines(path, start_line?, count?, timeout?)
```

## Parameters
- path  
    String. File to read.  
- start_line  
    Number, optional. Starting line index, default `1`; positive numbers start at `1`, negative values count from the end (`-1` is the last line), and `0` means after the last line.  
- count  
    Number, optional. Number of lines to fetch; default `-1` for the rest of the file.  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- lines  
    Table. Array of strings with normalised `\n`; `nil` on failure.  
- err  
    String or `nil`. Error description when the call fails.  

## Notes
> Reads a range of lines from the file, useful for paginating large logs.  
> Positive numbers start at `1`; negative values count from the end (`-1` is the last line, `-2` the second-to-last); `0` means after the last line.  
> Returns `nil` when the selected range has no content.  

## Example
```lua
local lines, err = LCC.web_file.get_range_lines("/logs/task.log", 101, 20)
if lines then
    for _, line in ipairs(lines) do
        print(line)
    end
end
```
