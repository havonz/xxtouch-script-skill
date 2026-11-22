# xxtouch-script

供 AI 编程助手编写和调试 XXTouch Lua 5.3 脚本的 Skill，包含 API 参考、XXT/XPP 项目模板和脚本开发工具。XXTLanControl 与 XXTCloudControl 都可以分发这份 Skill。

## 使用

将整个 `skills/xxtouch-script` 目录复制到助手的 skills 目录。助手通过 `SKILL.md` 读取使用说明，按需查阅 API 或调用模板工具。[Skill 入口](skills/xxtouch-script/SKILL.md) · [API 索引](skills/xxtouch-script/references/api-index.tsv) · [IKEv2 配置示例](skills/xxtouch-script/references/api/vpnconf.md#ikev2-example)

## 发布版本

在 GitHub Actions 的 **Release Skill** 工作流选择 `main` 并运行。CI 按发版时的 UTC 时间生成 `vYYYYMMDDHHMM` 版本号，写入 `skills/xxtouch-script/VERSION`，再为同一提交打标签并发布包含 `xxtouch-script.zip` 的 GitHub Release。两端控制器固定到这个提交，随包分发同一个版本号。[发布工作流](https://github.com/havonz/xxtouch-script-skill/actions/workflows/release.yml) · [下载发布包](https://github.com/havonz/xxtouch-script-skill/releases)

## 本地打包

在仓库根目录运行以下命令，可将当前提交导出为包含顶层 `xxtouch-script/` 目录的 ZIP。发布方可将命令中的 `HEAD` 替换为指定的提交或标签。

```sh
git archive --format=zip --prefix=xxtouch-script/ -o xxtouch-script.zip HEAD:skills/xxtouch-script
```

随包的 OCR 字典保留了上游的署名和许可条款。[ncnn 字典许可](skills/xxtouch-script/assets/frameworks/licenses/ncnn-dictionary.txt)
