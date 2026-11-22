# Read Script UI Configuration (LCC.get_ui_config)

## Signature
```lua
config = LCC.get_ui_config()
```

## Parameters
- none  

## Returns
- config  
    Table containing the `Config` section of `main.json` together with default values of UI controls.  

## Notes
> Flat scripts read `XXT_SCRIPTS_PATH .. "/main.json"`; XPP packages read the package file returned by `xpp.resource_path("main.json")`. The `Config` block is then merged with control defaults to build the final configuration table.
> ComboBox/RadioGroup values return the selected label; CheckBoxGroup returns mappings such as `{ ['Option A'] = true }`.  
> Returns an empty table when `main.json` is missing or malformed.  

## Example
```lua
local conf = LCC.get_ui_config()
if conf["Target Group"] then
    print("Running against group: " .. conf["Target Group"])
end
```
