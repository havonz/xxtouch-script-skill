# Request a Text Reply (LCC.assist.ask_text)

## Declaration

```lua
result, err, task = LCC.assist.ask_text(options)
```

## Parameters

- options  
    Table. Assist request configuration. See [Common Options and Return Objects](./common-options.md). This function sets `type = "text"` automatically.

## Return Values

- result  
    Table or `nil`. Usually `{ kind = "text-reply", text = "..." }` on success.
- err  
    String or `nil`. Failure reason.
- task  
    Table or `nil`. The latest task state.

## Notes

> Use this for captchas, SMS codes, passcodes, or other cases where the operator provides text and the script can continue.  
> Do not use text reply when the operator needs to decide what the next action should be. Use `request_control()` instead.  

## Example

```lua
local result, err = LCC.assist.ask_text({
    title = "Enter captcha",
    text = "Please read the captcha in the screenshot and enter it",
    screenshotLocalPath = XXT_SCRIPTS_PATH .. "/captcha.png",
    timeout = 120,
})

if result then
    sys.input_text(result.text, false)
else
    nLog("assist failed", err)
end
```
