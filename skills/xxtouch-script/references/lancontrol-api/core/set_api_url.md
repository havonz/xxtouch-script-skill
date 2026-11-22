# Set Controller Endpoint (LCC.set_api_url)

## Signature
```lua
LCC.set_api_url(url)
```

## Parameters
- url  
    String. HTTP base URL of the controller server (for example `http://192.168.1.100:46990`).  

## Returns
- none  

## Notes
> Stores the controller address for all subsequent API calls.  
> When the script is not launched by the controller, you must invoke this before `LCC.connect()`.  
> This replaces the previously configured address.  

## Example
```lua
LCC.set_api_url("http://192.168.1.100:46990")
if not LCC.connect() then
    error("Unable to reach controller")
end
```
