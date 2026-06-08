# deep-interview Skill 测试记录

> 测试日期：2026-06-08  
> Skill 路径：`/Users/lizi/.codex/skills/deep-interview/SKILL.md`  
> Skill 名称：`deep-interview`

## 一、测试目标

验证 `deep-interview` 是否能封装 Day8 的深度访谈流程：

`粗选题 → 确认文章边界 → 逐轮访谈 → 提炼核心观点 → 保存访谈记录 → 交接给 style-write`

## 二、结构校验结果

已执行：

```bash
python3 /Users/lizi/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/lizi/.codex/skills/deep-interview
```

结果：

```text
Skill is valid!
```

说明：

- YAML frontmatter 合法
- Skill 命名符合规范
- agents/openai.yaml 已生成
- Skill 文件结构通过基础校验

## 三、触发语测试清单

以下表达应触发 `deep-interview`：

1. 我要开始写一篇新文章
2. 围绕这个选题采访我
3. 帮我做深度访谈
4. 先问我问题再写
5. 整理访谈记录
6. 把这个选题变成文章素材
7. 我想写这个选题，你先问我问题

## 四、预期执行流程

Skill 被触发后，AI 应该按以下顺序执行：

1. 确认选题、目标读者、平台、标题和文章边界。
2. 先总结当前理解，让作者纠偏。
3. 分轮提出高价值访谈问题。
4. 保留作者原始回答，不替换作者意思。
5. 根据回答提炼核心观点、必讲内容、不要写成什么。
6. 生成结构化访谈记录。
7. 保存到当前稿件文件夹的 `01-访谈记录`。
8. 提醒下一步进入 `style-write`，而不是直接擅自写稿。

## 五、关键安全规则

Skill 中已经写入以下规则：

- 不允许没访谈就直接写稿。
- 用户纠正文章方向时，以用户纠正为准。
- 不强行关联无关工具或主题。
- 作者回答混乱时，保留原始回答，把清洗后的内容放到提炼区。
- 通过 Obsidian URI 写入时必须使用 `encodeURIComponent`，避免空格变成 `+`。
- 未经确认，不覆盖用户已经编辑过的笔记。

## 六、边界情况检查

### 情况 1：用户只给了一个模糊选题

预期行为：

AI 应先问目标读者、写作目的、核心场景和不要写成什么。

### 情况 2：用户已经回答了一组访谈问题

预期行为：

AI 应整理和提炼现有回答，不重复完整访谈。

### 情况 3：AI 的理解被用户纠正

预期行为：

AI 必须更新文章边界，并在后续访谈和记录中遵守新边界。

### 情况 4：访谈记录完成

预期行为：

AI 应建议进入 `style-write`，生成大纲、初稿和 5 轮优化。

## 七、当前测试结论

`deep-interview` 已通过本地结构校验，流程设计符合 Day8 深度访谈要求。

由于当前会话已经加载过技能列表，新 Skill 的自动触发效果需要在新对话或重启 Codex 后验证。

## 八、下一步验证方法

打开一个新的 Codex/Claudian 对话，输入：

```text
我要开始写一篇新文章，选题是：普通人如何安全地让 AI 操作电脑。你先围绕这个选题采访我。
```

预期结果：

AI 应自动使用 `deep-interview`，先确认目标读者和文章边界，再开始逐轮访谈，而不是直接写文章。

## 九、当前 Skill 组合

现在已有三个 Skill：

1. `deep-interview`：选题深度访谈
2. `style-write`：基于访谈记录写稿并做 5 轮优化
3. `style-report-updater`：作者修订后更新风格报告

这三个 Skill 已经能覆盖：

`选题访谈 → 初稿生成 → 5轮优化 → 作者修订 → 风格报告更新`

## 十、后续建议

如果继续开发，下一个可选 Skill 是 `topic-filter`，用于从日常素材库筛选高价值选题。
