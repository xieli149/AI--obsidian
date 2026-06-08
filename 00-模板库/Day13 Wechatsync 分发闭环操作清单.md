# Day13 Wechatsync 分发闭环操作清单

## 当前状态

- Wechatsync CLI 已安装。
- CLI 版本：1.0.0
- Day12 发布包已完成：
  - `02-稿件库/01-创作中稿件/AI能操作电脑了但你真的知道它在动哪里吗-20260608/05-发布包/长文发布包`
  - `02-稿件库/01-创作中稿件/AI能操作电脑了但你真的知道它在动哪里吗-20260608/05-发布包/图文发布包`
- 「模板-发布数据分析」已创建。

## 一、你需要在浏览器里完成的操作

### 1. 安装 Chrome 扩展

推荐方式：

打开 Chrome 网上应用店，搜索或访问「文章同步助手 / Wechatsync」，点击添加到 Chrome。

如果商店无法访问：

1. 下载手册里的 ZIP 安装包。
2. 解压到固定文件夹。
3. 打开 `chrome://extensions/`。
4. 打开开发者模式。
5. 点击「加载已解压的扩展程序」。
6. 选择解压后的文件夹。

### 2. 登录目标平台

至少登录 3 个目标平台，建议先选容易登录的平台：

- 知乎：https://www.zhihu.com/
- 掘金：https://juejin.cn/
- CSDN：https://www.csdn.net/

如果你主要发公众号和小红书，也可以登录：

- 微信公众号：https://mp.weixin.qq.com/
- 小红书创作者中心：https://creator.xiaohongshu.com/

### 3. 检查扩展登录状态

点击 Chrome 右上角「文章同步助手」图标。

确认目标平台显示已登录。

## 二、CLI 配置步骤

CLI 需要通过浏览器扩展提供的 Token 通信。

### 1. 在扩展里开启 MCP 连接

1. 点击「文章同步助手」扩展图标。
2. 进入设置。
3. 开启「MCP 连接」。
4. 复制 Token。

### 2. 写入 Mac 环境变量

把下面命令里的 `你的token` 替换成扩展里的 Token：

```bash
echo 'export WECHATSYNC_TOKEN="你的token"' >> ~/.zshrc
source ~/.zshrc
```

### 3. 检查平台登录状态

```bash
wechatsync platforms --auth
```

## 三、同步草稿箱命令示例

注意：发布前先同步到草稿箱，然后你去平台后台人工检查和发布。

### 同步到知乎

```bash
wechatsync sync 长文发布包.md -p zhihu
```

### 同步到多个平台

```bash
wechatsync sync 长文发布包.md -p zhihu,juejin,csdn
```

### 预览模式

```bash
wechatsync sync 长文发布包.md --dry-run
```

## 四、平台 ID 对照

| 平台 | ID |
|-|-|
| 微信公众号 | weixin |
| 知乎 | zhihu |
| 小红书 | xiaohongshu |
| 微博 | weibo |
| 掘金 | juejin |
| CSDN | csdn |
| 头条号 | toutiao |
| B 站专栏 | bilibili |
| 百家号 | baijiahao |
| 简书 | jianshu |
| 抖音图文 | douyin |

## 五、数据反馈循环

发布后不要立刻分析，建议等 7 天数据相对稳定。

### 数据采集节奏

| 时间 | 采集内容 | 用途 |
|-|-|-|
| 发布后 24 小时 | 初始阅读/播放/互动 | 判断初始流量 |
| 发布后 7 天 | 完整阅读、点赞、收藏、评论、转发 | 主要分析节点 |
| 发布后 30 天 | 长尾数据 | 判断长期价值 |

### 安全原则

不要用脚本或第三方工具爬平台数据。

只使用平台官方后台导出或手动记录，避免触发风控。

## 六、Day13 打卡截图

需要准备：

1. Wechatsync 扩展面板，展示至少 3 个平台已登录。
2. 至少 1 个平台草稿箱，展示文章已同步成功。
3. Obsidian 中的「模板-发布数据分析」。

## 七、当前还需要你完成

1. 安装 Chrome 扩展。
2. 登录至少 3 个目标平台。
3. 开启 MCP 连接并提供 Token，或先使用浏览器扩展手动同步。
4. 将至少 1 篇文章同步到至少 2 个平台草稿箱。
