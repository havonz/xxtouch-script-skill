# Connect To The Controller (LCC.connect)

## Signature
```lua
ok = LCC.connect()
```

## Parameters
- none  

## Returns
- ok  
    Boolean. Returns `true` when the connection and version check succeed; otherwise `false`.  

## Notes
> Loads configuration, completes initialisation, and reports the script state to the controller.  
> If the module version mismatches, it attempts to download a newer `XXTLanControl.lua` from the control center and hot-update automatically.  
> The controller is automatically notified when the script stops.  
> When no address was set via `LCC.set_api_url()` and the script is not launched by the controller, the function returns `false` immediately.  

## Example
```lua
if not LCC.connect() then
    error("Unable to connect to the controller")
end
```
