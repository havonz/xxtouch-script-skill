# Set Log Column Aliases (LCC.set_log_aliases)

## Signature
```lua
LCC.set_log_aliases(aliases)
```

## Parameters
- aliases  
    Table. Ordered list of alias strings for log channels 1 through 6.  

## Returns
- none  

## Notes
> Persists the aliases so the controller UI and the dictionary form of `LCC.log` can use them.  
> Only six channels are supported; extra entries are ignored.  

## Example
```lua
LCC.set_log_aliases({
    "Status", "Progress", "Error", "Debug", "Spare 1", "Spare 2"
})
```
