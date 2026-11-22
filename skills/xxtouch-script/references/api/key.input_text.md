# key.input_text

Purpose: Input text without using the shared pasteboard

Available in versions after 20260816.

## Signature
```lua
success, error = key.input_text(text [, need_enter ])
```

## Example
```lua
local ok, err = key.input_text("Hello, XXTouch 🙂", true)
assert(ok, err)
```

## Parameters
- text
    string, valid UTF-8 text to input. It may be empty. Each `"\b"` performs one Backspace operation in sequence.
- need_enter
    boolean, whether to press Return after input finishes. Defaults to `false`. With empty text, `true` sends Return only.

## Returns
- success
    boolean, `true` when the simulated input operation was sent, or `false` on failure.
- error
    string, the failure reason when `success` is `false`.

## Notes
- Enters text by simulating the way an input method commits selected text.
- Does not read or modify the shared system pasteboard.
- Cannot enter text into password fields; use `sys.input_text` for password fields.
- If a later text segment, Backspace, or Return operation fails, text already entered is not rolled back.
- A `true` return value does not guarantee that the focused field accepted the text. Keep the device unlocked, the target app in the foreground, and the target field focused.
