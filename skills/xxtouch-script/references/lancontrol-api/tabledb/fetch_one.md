# Atomically Fetch And Update A Row (LCC.db.fetch_one)

## Signature
```lua
row, err = LCC.db.fetch_one(name, opts, timeout?)
```

## Parameters
- name  
    String. Table name. Must be non-empty and no longer than 256 bytes.  
- opts  
    Table with:
    - `conditions`: table of equality filters (default `{}`)
    - `update`: table of fields to update after the row is claimed
    - `pick`: string, choose `"min"`, `"max"`, or `"random"`; defaults to `"min"` based on `id`  
- timeout  
    Number, optional. Request timeout in seconds, default `60`.  

## Returns
- row  
    Table. The claimed row; `nil` on failure or when nothing matched.  
- err  
    String or `nil`. Error description; `'not found'` when no row matched, `'unknown table'` when the table is missing.  

## Notes
> Atomically reads and updates a single row, ideal for task assignment under concurrency.  
> Fields in `update` are persisted immediately so the same record is not handed out twice.  
> Omitting `update` still performs an atomic selection but skips the write-back.  

## Example
```lua
local row, err = LCC.db.fetch_one("tasks", {
    conditions = { Status = "Idle" },
    update = { Status = "Running" },
    pick = "min"
})
if row then
    print("Claimed task", row.id, row.Name)
elseif err == "not found" then
    print("No idle tasks available")
end
```
