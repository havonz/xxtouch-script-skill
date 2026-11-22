# Query Rows With Conditions (LCC.db.list)

## Signature
```lua
rows, err = LCC.db.list(name, opts?, timeout?)
```

## Parameters
- name  
    String. Table name. Must be non-empty and no longer than 256 bytes.  
- opts  
    Table, optional. Query options:
    - `conditions`: key/value pairs combined with AND
    - `order_by`: string, column to sort by (`"id"` by default)
    - `desc`: boolean, `true` for descending order, default `false`
    - `limit`: integer, maximum rows to return
    - `offset`: integer, number of rows to skip (default `0`)  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- rows  
    Table. Array of rows that match; `nil` on failure.  
- err  
    String or `nil`. Error description such as `unknown column` or `unknown table`.  

## Notes
> Queries rows by condition; all user column values are strings.  
> User columns in returned objects are strings, while `id` is a number.  
> Without `opts` it returns every record in ascending `id` order.  

## Example
```lua
local rows, err = LCC.db.list("tasks", {
    conditions = { Status = "Idle" },
    order_by = "id",
    limit = 20
})
if rows then
    print("Idle tasks:", #rows)
end
```
