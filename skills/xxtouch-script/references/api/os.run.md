# os.run

Use this synchronous alternative to `os.execute` for stdin, captured output, and a command timeout.

`ok, reason, status, stdout, stderr = os.run(command [, timeout_s [, stdin]])`

- Pass a shell string or an argv table for direct execution, e.g. `{path, "arg", 1, env={LANG="C"}}`. The first entry is the executable path. String and number arguments are supported. The environment table is optional.
- `timeout_s` is in seconds. Zero or omitted means no deadline. Above one second, termination can begin one second before the deadline.
- Pass a string for stdin. Its write end closes after the data is sent. Use `""` for immediate EOF or `0` for a timeout-free call with input.
- `ok` means `status == 0`. Normal reasons are `"exit"`, `"signal"`, and `"unknown"`. A forced timeout reports `"killed"`. Both output streams are returned as strings, including on failure.

```lua
local ok, reason, status, stdout, stderr = os.run("cat", 2, "hello\n")
if ok then nLog(stdout) else nLog(reason, status, stderr) end
```
