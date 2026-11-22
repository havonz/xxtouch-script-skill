# Create A Table (LCC.db.create)

## Signature
```lua
ok, err = LCC.db.create(name, columns, timeout?)
```

## Parameters
- name  
    String. Table name. Must be non-empty and no longer than 256 bytes.  
- columns  
    Table. Array of column names. Each name must be non-empty valid UTF-8, must not repeat, and must not be `id`.  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- ok  
    Boolean. `true` on success, `false` on failure.  
- err  
    String or `nil`. Error message on failure; `'table already exists'` when the table is present.  

## Notes
> Creates a new table; every user column is stored as `TEXT`, and an auto-increment `id` is added automatically.  
> An empty table name, a table name longer than 256 bytes, or a column name that is not valid UTF-8 raises a Lua parameter error before the request is sent.  
> Duplicate column names return an error.  

## Example
```lua
local ok, err = LCC.db.create("tasks", {"Name", "Status", "Remark"})
if not ok then
    error(err)
end
```
