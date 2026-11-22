# TableDB Overview

`LCC.db` provides structured storage where every user column is stored as a string and each row has an auto-increment `id`.

- create tables, then add, edit, and delete rows in batches
- read rows through `get`, `list`, `count`, and `fetch_one`
- use `fetch_one` to claim one row safely under concurrency
- keep using tables that are already maintained in the UI or used by schedules

## Import the Module

```lua
local LCC = require("XXTLanControl")
```

## Before You Start

Before using any helper, make sure you either call `LCC.set_api_url()` or start the script from the control center, and always complete initialization with `LCC.connect()`.
