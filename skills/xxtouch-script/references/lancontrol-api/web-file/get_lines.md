# Read File As Lines (LCC.web_file.get_lines)

## Signature
```lua
lines, err = LCC.web_file.get_lines(path, timeout?)
```

## Parameters
- path  
    String. File path to read.  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- lines  
    Table. Array of lines with normalised `\n` endings; `nil` on failure.  
- err  
    String or `nil`. Error description when the call fails.  

## Notes
> Reads the entire file and splits it into a line array.  
> `\r\n` is normalised to `\n` before splitting.  

## Pairing reads and writes

When a file ends with a newline, `get_lines` keeps the empty string produced by splitting at the end. For example, the two-line text `"A\nB\n"` returns `{"A", "B", ""}`; passing this array to `set_range_lines(path, 1, lines)` writes three lines, with a blank last line.

To read and replace content by line number, pair [`get_range_lines`](./get_range_lines.md) with `set_range_lines`. To read, modify, and overwrite the whole file, pair `get_lines` with [`set_lines`](./set_lines.md). `set_lines` overwrites the entire file and is not suitable for partial replacements.

In both pairs, reading and writing are separate requests, so the complete read-modify-write sequence is not atomic. Coordinate access when there are concurrent writes to avoid overwriting changes made after the read.

## Example
```lua
local lines, err = LCC.web_file.get_lines("/config/list.txt")
if not lines then
    error(err)
end
print("Lines:", #lines)
```
