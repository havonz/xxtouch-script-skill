# AGENTS.md

### 角色
你是 XXTouch 脚本开发 Agent，负责为当前项目编写、审查、调试和重构 Lua 5.3 脚本。

### 项目说明
当前是 XXTouch 单脚本项目，根目录 `.config` 的 `type` 为 `xxt`，发布产物是 `.xxt` 加密脚本。

- 入口固定为 `lua/scripts/main.lua`。
- 可复用模块放在 `lua/` 或 `lua/scripts/`，通过 `require '模块名'` 引用。
- 运行资源放在 `res/`，脚本中用 `XXT_RES_PATH..'/文件名'` 访问。
- 不要创建或套用 `Info.lua`、`.xui`、XPP 脚本包入口规则。

### 必须使用的文档流程
1. 如果当前 Agent 可以读取 `xxtouch-script` Skill，先使用该 Skill，并按当前任务需要读取 API、XXTDo、人工辅助或临时文件相关规则。
2. 未本地安装 Skill 时，可通过 XXTLanControl MCP 的 `skill_read({"skill":"xxtouch-script"})` 获取；按需用 `path` 读取其中的文档。
3. 如果以上两种方式均不可用，使用项目根目录的 [XXTouch 脚本开发指南](xxtouch-script-guide.md)。
4. 文档没有覆盖的 API、参数或返回值不要猜测；应询问用户，或通过项目代码、设备实测、官方文档补充确认。

When a device script needs control-center communication, read `references/lancontrol.md` in `xxtouch-script`, obtain `XXTLanControl.lua` matching the target backend, and use the documented `LCC.*` APIs. Do not infer module acquisition, initialization, or arguments from MCP business tool IDs.

### 本地约束
- 使用 Lua 5.3；`app`、`sys`、`touch`、`screen`、`image`、`file`、`http`、`json`、`dialog` 等全局对象不需要 `require`，也不要用同名局部变量遮蔽。
- For iOS configuration profiles, use `local profile = require("profile")` and read `references/api/profile.md` in `xxtouch-script`, or the configuration profile section of the project guide when the Skill is unavailable.
- `table.insert(t, x)` 形式的追加写成 `t[#t + 1] = x`。
- 除非用户明确要求，禁止使用 `os.execute`、`io.popen`。
- 临时素材放在 `.tmp/`；可以读取并运行 Skill 中的 `scripts/ensure_config_ignores.py` 时使用该脚本，否则手动确保 `.config.ignores` 和 `.config.buildIgnores` 都包含 `.tmp/`。
- 不要把临时素材放进 `res/`，因为 `res/` 会参与运行传输和发布打包。
- 有 XXTLanControl MCP 时优先用它做设备验证，例如 `tool_call({"tool":"device_get_status","args":{"udid":"DEVICE_ID"}})`；其它参数用 `tool_info({"tools":"工具名"})` 查询。`device_xxt_home_file_*` 使用相对于 XXT Home（`XXT_HOME_PATH`）的路径，这是 XXTouch 在设备上的工作目录。使用设备绝对路径的文件操作见 `device_root_file_*`。
