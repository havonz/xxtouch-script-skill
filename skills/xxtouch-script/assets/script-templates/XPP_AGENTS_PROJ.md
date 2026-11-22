### 项目说明
当前是 XXTouch 脚本包项目，根目录 `.config` 的 `type` 为 `xpp`，发布产物是 `.xpa`。

- 入口、显示名、图标和配置界面由根目录 `Info.lua` 定义，其中 `Executable` 指向默认运行脚本。
- `.lua` 和 `.xxt` 模块通常放在项目根目录，通过 `require '模块名'` 引用。
- 资源建议放在 `res/`，脚本中优先用 `xpp.resource_path('res/文件名')` 取得路径。
- 不要假设入口是 `lua/scripts/main.lua`，也不要套用 XXT 单脚本目录结构。
- 修改包结构、`Info.lua`、资源路径、`.xui`/`.xuic` 配置界面前，先查 `xxtouch-script` Skill 的 `references/xpp.md` 和对应 `xpp.*` / `xui.*` API 切片。
- 保留模板里已有的 `_config` 绑定，除非用户明确要求改成固定值。
