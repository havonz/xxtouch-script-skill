# Core

## Import the Module

```lua
local LCC = require("XXTLanControl")
```

## Before You Start

- Make sure the XXTouch version on the device is new enough.
- `LCC.capture_ui_state()` requires device-side `ui_element` version 0.6.0 or later. If the module is unavailable or outdated, update XXTouch before using **capture_ui_state**.
- If the script is not started from the control center, call `LCC.set_api_url()` first.
- Always call `LCC.connect()` before using other helpers.

If the module version does not match, `LCC.connect()` will try to download the newer module from the control center and reconnect automatically.

## What This Section Covers

- set connection retry count with `set_retry_count`
- set the control center address with `set_api_url`
- set aliases for log channels 1 to 6 with `set_log_aliases`
- send logs back to the control center with `log`
- capture and save UI state with [`capture_ui_state`](./capture_ui_state.md)
- read script UI configuration values with `get_ui_config`
