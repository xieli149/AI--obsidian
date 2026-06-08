# wechat-publish-polish Skill 测试记录

> 测试日期：2026-06-08  
> Skill 路径：`/Users/lizi/.codex/skills/wechat-publish-polish/SKILL.md`  
> Skill 名称：`wechat-publish-polish`

## 一、用途

用于公众号发布前的固定处理流程：

- 公众号精排版
- 生成或整理配图
- 删除水平分割线
- 生成 Obsidian 预览用 Markdown
- 生成 Wechatsync 同步用 Markdown
- 检查图片路径
- 同步公众号草稿箱前检查

## 二、结构校验

已通过：

```text
Skill is valid!
```

## 三、触发语

以下表达应触发：

1. 帮我做公众号发布稿
2. 把这篇文章做成公众号精排版
3. 同步公众号前检查图片路径
4. 图片不显示，帮我修路径
5. 删除文章里的水平分割线
6. 生成公众号配图
7. 导入公众号草稿箱前帮我检查

## 四、关键规则

- 不直接同步发布包说明文件。
- 同步正文第一行必须是正式标题。
- 删除所有水平分割线。
- 生图尽量不要让模型直接生成中文。
- Obsidian 预览用 `file://`。
- Wechatsync 同步用相对路径。
- API Key 不写进 Skill、脚本或笔记。

## 五、验证方法

新开对话后输入：

```text
帮我把这篇文章做成公众号精排版发布稿，处理配图、图片路径和同步前检查。
```

预期：AI 应自动使用 `wechat-publish-polish`。
