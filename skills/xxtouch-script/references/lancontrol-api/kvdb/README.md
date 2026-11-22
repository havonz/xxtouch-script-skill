# KVDB Overview

`LCC.kvdb` wraps the control center's key-value database:

- **queue**: FIFO queue storage with push, pop, move, and bulk removal operations
- **dict**: dictionary storage with write, copy, increment, and clear helpers

If you already maintain queues, dictionaries, or task state in the UI, your scripts can continue working with that data directly through `LCC.kvdb`.

> Queue names, dictionary names, and keys in KVDB may contain Chinese characters.
