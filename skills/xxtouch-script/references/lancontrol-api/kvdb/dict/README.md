# Dictionary APIs

## Import Module

```lua
local LCC = require("XXTLanControl")
```

## Before You Start

Before using any helper, ensure you either invoke `LCC.set_api_url()` or launch the script from the controller, and always complete initialisation by calling `LCC.connect()`.

## Shared Constraints

- All dictionary name parameters such as `name`, `src_name`, and `dst_name` must be non-empty strings and no longer than `256` bytes.
- All key parameters such as `key`, `src_key`, and `dst_key` must be non-empty valid UTF-8 strings.
- All write-value parameters such as `value` must be valid UTF-8 strings.
