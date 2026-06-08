# topic-filter Skill 测试记录

> 测试日期：2026-06-08  
> Skill 路径：`/Users/lizi/.codex/skills/topic-filter/SKILL.md`  
> Skill 名称：`topic-filter`

## 一、测试目标

验证 `topic-filter` 是否能封装 Day7 的选题筛选流程：

`素材/日常灵感 → 账号定位判断 → 高价值选题筛选 → 选题笔记 → 交接给 deep-interview`

## 二、结构校验结果

已执行：

```bash
python3 /Users/lizi/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/lizi/.codex/skills/topic-filter
```

结果：

```text
Skill is valid!
```

## 三、触发语测试清单

以下表达应触发 `topic-filter`：

1. 帮我从素材库筛选选题
2. 看看有什么值得写
3. 把这些素材变成选题
4. 今天写什么
5. 生成选题笔记
6. 从日常素材里找高价值主题
7. 这个素材适合写成什么文章

## 四、预期执行流程

Skill 被触发后，AI 应该按以下顺序执行：

1. 确认账号定位、目标读者和内容平台。
2. 读取或获取素材。
3. 按读者痛点、时效性、作者适配度、具体性、可执行性、差异化筛选。
4. 输出 3-5 个候选选题。
5. 让作者选择或修正角度。
6. 作者确认后创建标准化选题笔记。
7. 提醒下一步进入 `deep-interview`。

## 五、关键安全规则

Skill 中已经写入以下规则：

- 不在选题筛选阶段直接写完整文章。
- 不把每个素材都当成选题。
- 不强行贴合不相关的账号定位。
- 没有账号定位时先提问确认。
- 无法读取 Obsidian 文件时，让用户粘贴素材。
- 通过 Obsidian URI 写入时必须使用 `encodeURIComponent`，避免空格变成 `+`。

## 六、边界情况检查

### 情况 1：用户只给一个素材

预期行为：

AI 应围绕该素材判断是否值得写，并给出可能角度，而不是假装扫描了整个素材库。

### 情况 2：用户没有账号定位

预期行为：

AI 应先问目标读者、平台、内容方向，再筛选。

### 情况 3：出现多个候选选题

预期行为：

AI 应推荐最强一个，但让作者最终确认。

### 情况 4：作者确认选题

预期行为：

AI 应创建选题笔记，并建议进入 `deep-interview`。

## 七、当前测试结论

`topic-filter` 已通过本地结构校验，流程设计符合 Day7 选题筛选要求。

由于当前会话已经加载过技能列表，新 Skill 的自动触发效果需要在新对话或重启 Codex 后验证。

## 八、下一步验证方法

打开一个新的 Codex/Claudian 对话，输入：

```text
帮我从素材库里筛选几个值得写的选题。
```

预期结果：

AI 应自动使用 `topic-filter`，先确认账号定位和目标读者，再读取或请求素材，不应直接写文章。

## 九、当前 Skill 组合

现在已有四个 Skill：

1. `topic-filter`：素材筛选成选题
2. `deep-interview`：选题深度访谈
3. `style-write`：基于访谈记录写稿并做 5 轮优化
4. `style-report-updater`：作者修订后更新风格报告

这四个 Skill 已经覆盖：

`素材 → 选题 → 访谈 → 初稿 → 5轮优化 → 作者修订 → 风格报告更新`

## 十、后续建议

下一步可以进入 Day12：多平台适配模板与自动化导出流程。
