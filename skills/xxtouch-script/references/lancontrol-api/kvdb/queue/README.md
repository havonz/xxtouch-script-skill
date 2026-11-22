# Queue APIs

## Import Module

```lua
local LCC = require("XXTLanControl")
```

## Before You Start

Before using any helper, ensure you either invoke `LCC.set_api_url()` or launch the script from the controller, and always complete initialisation by calling `LCC.connect()`.

## Shared Constraints

- All queue name parameters such as `name`, `from_name`, and `to_name` must be non-empty strings and no longer than `256` bytes.
- All value parameters such as `value` must be valid UTF-8 strings; batch pushes accept a continuous string array.
