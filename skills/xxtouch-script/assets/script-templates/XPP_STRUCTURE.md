## 项目结构
通过 Info.lua 配置脚本信息（包括启动文件及主配置界面文件）
扩展名为 *.xxt 和 *.lua 格式模块直接放到项目根目录，可通过 require "<module_name>" 引用。
资源文件放到当前项目的 `res/` 目录下，可以在脚本中 `xpp.resource_path` 函数访问，例如 `xpp.resource_path("res/1.png")`。
```
脚本路径/
├── res/
│   ├── 1.png
│   └── 2.png
├── a.lua
├── b.xxt
├── main.lua
├── interface.xui
└── Info.lua
```

## XPP 脚本包说明

XPP 脚本包实际上是带有 `.xpp` 扩展名的目录，XXTouch 会像读取单一文件一样加载其内容。包中最少需要提供 `Info.lua` 与至少一个可执行脚本；根据脚本需求，还可以附带界面配置和资源文件。

### 基础布局
- `Info.lua`：存放脚本应用包的元数据，XXTouch 通过它识别入口脚本、显示名称、兼容性等信息。
- 可执行脚本：至少包含一个 `.lua` 或 `.xxt` 文件，必要时可在 XUI 界面中触发不同入口。
- 界面配置：可选的 `.xui`/`.xuic` 配置，用于提供设置界面。
- 资源：按需放置图片、音频、配置等文件，推荐集中在 `res/` 并使用相对路径访问。

### Info.lua 字段
`Info.lua` 应当仅返回一个常量表，避免执行额外逻辑。下表整理了主要字段及含义（带 * 为强烈建议填写）：

| 键 | 是否必填 | 说明 |
| --- | --- | --- |
| `BundleIdentifier`* | 是 | 反向域名格式的唯一标识，创建后不应再变更。|
| `BundleVersion`* | 是 | 语义类似 `主版本.副版本[.发布号]`，发布时需递增。|
| `BundleName`* | 是 | ≤16 字符的短名称，可用于脚本或通知展示。|
| `BundleDisplayName` | 否 | 列表中显示的全名，超出 16 字符也可；缺省时回退到 `BundleName`。|
| `BundleIconFile` | 否 | PNG 图标基名，需同时打包 @2x/@3x 版本（64/128/192 像素）。|
| `Executable`* | 否 | 默认运行的入口脚本路径（`.lua` 或 `.xxt`）。未设置时脚本列表不显示启动按钮。|
| `MainInterfaceFile` | 否 | 关联的 `.xui`/`.xuic` 配置界面，未设置则不显示“配置”按钮。|
| `MinimumSystemVersion` | 否 | 允许运行的最低 iOS 版本。|
| `MaximumSystemVersion` | 否 | 允许运行的最高 iOS 版本。|
| `MinimumXXTVersion` | 否 | 运行所需的最低 XXTouch 服务版本，默认兼容 v1.2-1 及以上。|
| `SupportedDeviceTypes` | 否 | 支持的设备类型代号数组，不匹配时提示不兼容。|
| `SupportedResolutions` | 否 | 支持的物理分辨率数组（`width`/`height`），用于限制设备尺寸。|
| `PackageControl` | 否 | 附加信息字典，可包含作者、标签、版权等元数据。|

若有新增字段，保持常量表结构即可；XXTouch 未识别的键会被忽略。下面给出简化示例：

```lua
return {
    BundleIdentifier = 'com.example.demo';
    BundleVersion = '1.0.0';
    BundleName = 'Demo';
    BundleDisplayName = '演示脚本';
    BundleIconFile = 'appicon.png';
    Executable = 'main.lua';
    MainInterfaceFile = 'interface.xui';
    SupportedResolutions = {
        { width = 640; height = 1136; };
    };
    PackageControl = {
        AuthorName = 'Your Name';
        Homepage = 'https://example.com';
    };
};
```

### 本地化策略
- `Info.lua`、`.strings` 等可放入 `xx.lproj/` 目录以实现多语言，与 iOS 本地化规则一致。
- `BundleDisplayName`、`BundleName` 以及 XUI 字段均可通过多语言资源替换；缺省时回退到默认语言。
- 静态资源引用建议结合语言子目录或使用逻辑在运行时根据 `xpp.locale_path()` 管理。


## XUI 文件说明
### 基础概念
- `.xui` 是 UTF-8 编码的 Lua 脚本，执行后需 `return` 一张描述界面的字典表；可按需加密为 `.xuic` 防篡改。
- `.xui` 仅允许调用极少数运行时模块，下表之外的任意 API 都会在加载阶段直接报错，请严格遵守：
    - **xpp** ：XPP 脚本包模块。
    - **xui** ：XUI 配置界面模块。
    - **string**：仅支持 `string.compare_version`。
    - **app**：仅支持 `app.open_url`。
    - **screen**：仅支持 `screen.size`。
    - **sys**：仅支持 `sys.version`、`sys.xtversion`。
    - **device**：仅支持 `device.type`、`device.name`。
    - **plist**：仅支持 `plist.read`、`plist.write`。
    - **json**：仅支持 `json.encode`、`json.decode`、`json.null`。
- XUI 作为 XPP 脚本包的主配置界面，通过 `Info.lua` 的 `MainInterfaceFile` 字段关联；配置值存放在 `uicfg/<defaults>.plist`。
- 读取、写入配置时调用 `xui.get(defaults, key)` 等 API，配合组件的 `defaults` 与 `key` 字段完成落盘和取值。

### 顶层结构（根级字典）
| 键 | 类型 | 是否必填 | 说明 |
| --- | --- | --- | --- |
| `title` | 字符串 | 否 | 顶部导航栏标题，可本地化 |
| `header` / `subheader` | 字符串 | 否 | 页首主、副标题，可本地化 |
| `defaults` | 字符串 | 是 | 配置分区标识符，对应存储的 plist 文件名 |
| `items` | 数组（元素为字典） | 是 | 组件列表，按顺序渲染 |
| `theme` | 字典 | 否 | 全局主题，所有子页面会继承，可被局部覆盖 |
| `stringsTable` | 字符串 | 否 | 指定多语言表（默认 `Localizable`） |

### 组件通用字段
| 键 | 类型 | 说明 |
| --- | --- | --- |
| `cell` | 字符串 | 组件类型标识，例如 `Switch`、`Link`、`Option` 等 |
| `label` | 字符串 | 组件标题，常显示在左侧（部分组件不支持） |
| `defaults` / `key` | 字符串 | 指定配置分区与键名，若组件需持久化必须配置 |
| `default` | 基本类型 | 初始化默认值，在未保存值时写入 `value` |
| `value` | 基本类型 | 组件当前值，未指定时使用 `default` |
| `icon` | 字符串 | 左侧图标文件名（部分组件不支持） |
| `readonly` | 布尔型 | 设为 `true` 时界面只读且不可进入子页面 |
| `height` | 数值 | 自定义单元高度（用于 `Image`/`AnimatedImage` 等） |
| `theme` | 字典 | 局部主题，覆盖并合并根级 `theme` 中相同字段 |

> 约定：没有显式值的组件默认读取 `default`；删除条目时会回落到默认值。组件的 `defaults` 可覆盖根级，从而将部分配置写入独立 plist。

### 主题键合并规则
- `theme` 以根级为基础，组件本身的 `theme` 键会覆盖同名字段；若通过 `Link` 打开的子 XUI 页面，子页面的 `theme` 再与父页面合并。
- 颜色以 `#RRGGBB` 或 `#RRGGBBAA` 表示。常用分类：界面（`style`、`tintColor` 等）、导航栏、页首/页尾、通用单元（`labelColor`、`valueColor` 等）、状态色（`dangerColor` 等）。
- `Option`/`MultipleOption`/`OrderedOption`/`EditableList` 这类跳转原生子界面的组件，子界面主题只继承组件级 `theme`，不继承根级以外的设置。

### 组件明细
| 组件 (`cell`) | 专有键 | 返回值 / 行为 | 限制与提示 |
| --- | --- | --- | --- |
| `Group` | `footerText` | 无返回值，分节标题 | 不支持 `icon`/`height`，常用作段落说明 |
| `Link` | `url` | 无，点按后打开子界面或 URL | 可跳转 `.xui`/`.xuic`、本地文件或网页 |
| `Switch` | `negate`、`trueValue`、`falseValue` | `true`/`false` 或映射值 | 可设 `readonly`；主题含 `onTintColor` 等 |
| `Button` | `action`、`args`、`alignment` | 动作返回值会写回配置 | 支持 `Reload:`、`RunCommand:`、`LaunchScript:`、`OpenURL:`、`ScanQRCode:`、`SendMail:`、`Null:` 等动作 |
| `TextField` | `alignment`、`keyboard`、`placeholder`、`isSecure`、`clearButtonMode`、`maxLength`、`validationRegex`、`prompt`、`message`、`okTitle`、`cancelTitle` | 字符串 | 不支持 `icon`；设置 `prompt`/`message` 时输入改在弹窗内完成 |
| `Radio` / `Checkbox` | `options`、`numPerLine`、`minCount`、`maxCount` | 单选返回单值，多选返回数组 | 不支持 `label`/`icon`/`height`；`options` 元素含 `title`/`value` |
| `Segment` | `options` | 选中项值 | 官方说明不支持 `icon`；适合候选数较少的单选 |
| `Option` | `options`、`footerText`、`popoverMode` | 选中项值 | 可设置 `shortTitle`、`icon`；子页面为单选列表 |
| `MultipleOption` | `options`、`footerText`、`maxCount`、`popoverMode` | 选中值数组 | 与 `Option` 类似但保存多选 |
| `OrderedOption` | `options`、`footerText`、`popoverMode`、`minCount`、`maxCount` | 有序选中值数组 | 支持拖拽排序；可限制选择数量 |
| `EditableList` | `footerText`、`itemFooterText`、`maxCount`、`validationRegex` | 字符串列表 | 子页面可增删改；支持正则校验 |
| `Slider` | `min`、`max`、`step`、`showValue` | 数值 | 官方说明不支持 `label`/`icon`，如需标题请配合 `Group`；`step=0` 表示连续值 |
| `Stepper` | `min`、`max`、`step`、`isInteger`、`autoRepeat` | 数值 | 不支持 `icon`；适合整数/浮点微调 |
| `DateTime` | `min`、`max`、`minuteInterval`、`mode`、`format` | Unix 时间戳或格式化字符串 | 不支持 `label`/`icon`；`mode` 可设 `datetime`/`date`/`time`/`interval` |
| `TitleValue` | `value`、`snippet` | 显示值；可调用代码片段并写回 | 可左滑清除配置；配合 `defaults`/`key` 展示运行时数据 |
| `StaticText` | `label`、`alignment`、`selectable` | 无配置值，纯展示 | 不支持 `icon`/`height`；`selectable=true` 允许复制 |
| `Textarea` | `maxLength`、`keyboard`、`autoCapitalization`、`autoCorrection` | 字符串 | 打开子页面输入多行文本；不支持字体调整 |
| `Image` / `AnimatedImage` | `path` | 无返回值，展示图片 | 必须设置 `height`；`AnimatedImage` 支持 http/https GIF 缓存 |
| `File` | `initialPath`、`allowedExtensions`、`label`、`footerText`、`isFile` | 绝对路径字符串 | 左滑可清除；默认仅选文件，`isFile=false` 时改为目录 |
| `About` | `icon` | 无，仅展示 | 配合通用 `label`/`value` 作为标题与说明 |

### 多语言与资源管理
- 通过 `stringsTable` 指向脚本包中的 `.strings` 文件；所有标记“可本地化”的字段会按 iOS 国际化规则解析。
- 图片、图标等资源建议放在脚本包 `res/` 目录，引用时写相对路径并准备 `@2x`/`@3x` 版本以适配视网膜。

### 编写与调试建议
- 简单示例：
```lua
return {
    title = '示例界面';
    defaults = 'com.example.demo';
    items = {
        {
            cell = 'Group';
            label = '基础配置';
        };
        {
            cell = 'Switch';
            key = 'enabled';
            label = '启用功能';
            default = true;
        };
    };
};
```
- 组件值的清除通常通过左滑删除或使用 `default` 回退；需要防修改时设置 `readonly=true`。
- 不支持 `label` 的组件（如 `Slider`、`DateTime` 等）可结合 `Group` 组件补充标题或说明文字。


## 配置界面模块
### 类 xui*

### xui.show(fileName)
```lua
-- 展示一个配置界面
xui.show('interface.xui')
```

### xui.dismiss()
```lua
-- 收起正在展示的配置界面
xui.dismiss()
```

### xui.reload()
```lua
-- 重新加载当前正在展示的配置界面
xui.reload()
```

### xui.setup(fileName)
```lua
-- 校验并初始化配置界面配置
xui.setup('interface.xui')
```

### xui.clear(defaults)
```lua
-- 清除某个配置分区所有配置
xui.clear('com.yourcompany.demo')
```

### xui.get(defaults, key)
```lua
-- 获取配置界面上的某个配置值
local enabled = xui.get('com.yourcompany.demo', 'enabled')
```

### xui.set(defaults, key, value)
```lua
-- 设置配置界面上的某个配置值
xui.set('com.yourcompany.demo', 'enabled', true)
```

### xui.read(defaults)
```lua
-- 读取某个配置分区的全部配置
local cfg = xui.read('com.yourcompany.demo')
nLog(cfg)
```

### xui.write(defaults, config)
```lua
-- 覆盖写入配置分区的配置
xui.write('com.yourcompany.demo', {enabled = true, city = '北京'})
```

## 脚本包模块
### 类 xpp*

### xpp.info()
```lua
-- 获取当前脚本包的元信息
local info = xpp.info()
nLog(info and info.name, info and info.version)
```

### xpp.bundle_path()
```lua
-- 获取当前脚本包的包路径
nLog(xpp.bundle_path())
```

### xpp.resource_path(resourceName)
```lua
-- 获取当前脚本包中的资源路径
local icon = xpp.resource_path('assets/icon.png')
nLog(icon)
```