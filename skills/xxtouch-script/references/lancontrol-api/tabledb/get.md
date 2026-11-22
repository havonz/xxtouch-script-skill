# Fetch Row By ID (LCC.db.get)

## Signature
```lua
row, err = LCC.db.get(name, id, timeout?)
```

## Parameters
- name  
    String. Table name. Must be non-empty and no longer than 256 bytes.  
- id  
    Number. Row `id` to retrieve. Must be an integer value greater than or equal to `1`.
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- row  
    Table. Row that matches the `id`; `nil` when not found.  
- err  
    String or `nil`. Returns `'not found'` if the row is missing, `'unknown table'` when the table does not exist.  

## Notes
> Retrieves a single row by `id`, typically for editing forms.  
> User columns are returned as strings, while `id` is returned as a number.  
> An `id` that is not an integer value greater than or equal to `1` triggers a Lua parameter validation error.

## Example
```lua
local row, err = LCC.db.get("tasks", 42)
if row then
    print("Task", row.Name, row.Status)
end
```
