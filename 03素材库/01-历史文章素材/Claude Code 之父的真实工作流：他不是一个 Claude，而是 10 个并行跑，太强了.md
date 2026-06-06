---
title: "Claude Code 之父的真实工作流：他不是一个 Claude，而是 10 个并行跑，太强了"
source: "https://mp.weixin.qq.com/s/PvXywnkXDabmxl2YYLmvvQ"
author:
  - "[[黎子ai]]"
published:
created: 2026-06-06
description: "内容主要是在分享“Claude Code 之父”自己是怎么高效用 Claude Code 写代码的"
tags:
  - "clippings"
---
黎子ai *2026年1月4日 17:08*

内容主要是在分享“Claude Code 之父”自己是怎么高效用 Claude Code 写代码的，可以理解成一套「多 Agent 并行 + 团队知识库」的工作流示范。

## 核心内容

- 他强调：Claude Code 开箱即用，默认配置就很好，不需要折腾复杂定制，每个人可以按自己的习惯来用，没有唯一正确姿势。
- 他自己是「重度用户」，会同时开很多个 Claude 会话（本地终端 + 网页版），让它们并行干活，提高开发效率。
- 他认为最新的 Opus 4.5「带思考模式」是目前写代码最好用的模型，虽然单次响应慢一些，但因为更聪明、需要你操心更少，整体速度反而更快。
- 团队层面，他们用一个共享的 CLAUDE.md 文档来教 Claude：哪些做法是错的、项目有哪些约定，把这些经验沉淀起来，让 Claude 越用越懂你的代码库。
- 在代码评审（Code Review）时，他们会让 Claude 自动参与，并顺手更新 CLAUDE.md，相当于让 AI 帮团队持续「打磨」自己的工程实践。

## 他用 Claude Code 的具体步骤（简化版）

下面是把他那一长串推文，拆成小白也能照着理解/模仿的流程（不要求你一步不差照做，更多是思路）：

## 1\. 在终端里并行开 5 个 Claude

- 他在本地终端里跑了 5 个 Claude 会话，把标签页编号为 1～5，比如一个负责写代码、一个负责写测试、一个负责重构等。
- 他开启系统通知：当某个 Claude 等他输入时，会弹通知提醒，这样他不用盯着一个窗口，而是来回切换，把时间填满。
- ![Image](https://mmbiz.qpic.cn/mmbiz_png/hrGeVYXiaibBPItRWkTwZxZhLZbo8ibFg7icxFv2O4VTNNrH73blEq9YqtOQ5BhC8y5wsHK9jynY7Pu86p3VQ83v8w/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=0)

> 对小白理解：  
> 就像你同时和 5 个「远程实习生」聊天，让他们并行干不同的任务，你只在他们找你时回复一下。

## 2\. 同时再开 5–10 个网页版 Claude Code

- 除了本地 5 个，他还会在 claude.ai/code 上再开 5–10 个 Claude 会话，让「本地 + 网页」一共十来个任务一起跑。
- 当终端里的某个任务跑到一半，他会把上下文「丢给」网页端继续（用&），或者在 Chrome 手动启动会话，有时还会——来回传送。每天早上和白天都会用手机（通过 Claude iOS 应用）启动几次会话，之后再查看。
	![Image](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

> 对小白理解：  
> 本地终端 = 你眼前在干的事，网页 Claude = 你让它在后台「慢慢想、慢慢跑」的大任务，互相可以接力。

## 3\. 模型选择：统一用 Opus 4.5 + 思考模式

- 他所有编码相关任务都用 Opus 4.5 的思考模式
- 原因：Opus 虽然比 Sonnet 慢，但因为：
- 更懂复杂代码和工具调用
	- 需要你少做「提示工程」和反复纠正  
	所以从「总用时」来看，反而更快。

> 对小白理解：  
> 有点像：请一个贵但靠谱的高级工程师，一次就写对，而不是请一个便宜但需要你不停返工的人。

## 4\. 用 CLAUDE.md 把「踩过的坑」喂回去

- 他们在代码仓库里有一个 CLAUDE.md 文件，放在 git 里，全团队一起维护。
- 每当 Claude 做错事（比如用错内部函数、写错风格、忘了某个业务规则），他们就把「这个错误」和「正确写法」写进 CLAUDE.md。
- 下次 Claude 再看同一个仓库时，就能从 CLAUDE.md 里学到这些规则，少犯同样的错误。
- ![Image](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

> 对小白理解：  
> 每次 AI 搞砸，你别只骂它，顺手记一条「注意事项」到 CLAUDE.md，等于给它写「小抄」，越记越聪明。

## 5\. 在代码评审中让 Claude 自动参与

- 他做 Code Review 时，会在同事的 PR 里 @.claude，让 Claude 来：
- 帮忙审查代码
	- 发现问题后自动更新 CLAUDE.md（通过 用 Claude Code 的 GitHub 动作（/install-github-action）来实现这个功能）形成复利工程
- 这就把「日常评审」变成「顺手教 Claude 变聪明」的过程，类似 Dan Shipper 说的「复利工程」：每次小改动，都在给系统加经验值。
- ![Image](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

> 对小白理解：  
> 每次评审，不只是改这一次代码，还顺手教 AI：以后遇到类似情况应该怎么做，这样团队效率「越用越高」。

6\. 用「计划模式」先把方案想明白

大多数会话以计划模式开始（Shift+Tab 两次）。如果目标是写一个拉取请求，他会先用计划模式，让 Claude 把要改哪些文件、分几步做都写成一个详细计划，来回调整到满意，再切到自动接受编辑模式，让 Claude 一次性完成修改，一个好计划非常关键。

![Image](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

> 对小白理解：  
> 先让 Claude 把「这次要干什么、怎么一步步做」写成待办清单，再让它动手写代码，比一上来就乱改，成功率高太多。

## 7\. 高频小流程全部做成斜杠指令

他把自己一天内会重复好多次的「内循环工作流」，全部做成了斜杠指令（/命令）。这样既不用每次重新打一长串提示词，也能让 Claude 主动调用这些流程；这些命令都放在仓库的.claude/commands/ 目录里，跟代码一起进 git。

![Image](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

> 对小白理解：  
> 凡是你一天里要对 Claude 说三遍以上的重复话，都值得抽成一个「/命令」，以后一句指令就能触发整套流程。

---

8\. 用子代理自动化常见复杂流程

他经常使用几个固定的子代理（subagents）：比如 code-simplifier 用来在 Claude 写完代码后自动简化实现，verify-app 里写着非常详细的端到端测试步骤，专门用来测 Claude Code 是否工作正常。子代理本质上就是把高频、复杂的工作流封成一个个专门的「AI 小角色」来自动执行。

![Image](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

> 对小白理解：  
> 可以把子代理想成几个专科医生：一个只管帮你把代码改得更简洁，一个只管帮你按 checklist 把应用从头到尾验收一遍。

---

## 9\. 用 PostToolUse 钩子兜底代码格式

他们为 Claude 的工具调用加了一个 PostToolUse 钩子，专门负责在 Claude 完成修改后再次格式化代码。Claude 本身生成的代码格式已经不错，这个钩子主要是帮你兜底最后 10% 的小问题，避免 CI 里因为格式不规范而报错。

![Image](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

> 对小白理解：  
> 别指望 AI 每次都 100% 按你项目的格式规范来写，最后再加一层「自动格式化」，相当于有个机器人帮你统一美化代码。

---

## 10\. 不裸奔跳过权限，用 /permissions 预授权白名单

他不会使用 `--dangerously-skip-permissions` 这种一刀切跳过所有权限确认的方式，而是用 /permissions 预先允许一批在当前环境中确认安全、又经常会用到的 bash 命令。这些白名单配置写在.claude/settings.json 里，跟团队共享，既减少了频繁的权限弹窗，又保证了不安全操作仍需要显式确认。

![Image](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

> 对小白理解：  
> 不要一键把所有命令都放行，先列一份「安全命令清单」给 Claude，常用操作不打扰你，危险操作还是要你点头。

---

11\. Claude Code 帮我用所有工具  
Claude Code 会自动替他调用很多外部工具：经常通过 MCP 服务器在 Slack 里搜索和发消息，用 bq 命令行跑 BigQuery 查询来回答分析问题，也会从 Sentry 抓错误日志。这些工具的配置（比如 Slack 的 MCP 配置）写在.mcp.json 里，和代码一起提交、在团队内共享。

![Image](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

对小白理解：  
　　不用你自己去点开 Slack、数据平台和日志系统查来查去，只要事先把「这些工具的账号和用法」写进配置文件，Claude 就能帮你去各个系统里跑来跑去，你只负责提问题和看结果。

---

12\. 长任务用后台代理 / Stop Hook / 插件做二次复核  
对于非常长时间运行的任务，会选择（a）在完成后提示 Claude 通过后台代理验证其工作，（b）使用代理 Stop Hook 更确定地验证，或者（c）使用 ralph-wiggum 插件（最初由 @GeoffreyHuntley设计）。还会在沙盒中使用 --permission-mode=dontAsk 或 --dangerously-skip-permissions 来避免会话的权限提示，这样 Claude 就能在不被拉黑的情况下做 cook。

![Image](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

对小白理解：  
　　遇到要跑很久的大活，他不会「跑完就算结束」，而是再安排一个「第二双眼睛」（后台代理、钩子或插件）帮 Claude 复查一遍，这样更放心，不怕 AI 偷懒或犯低级错误。

---

13\. 最重要的是让 Claude 能验证自己的工作  
他最后总结：想从 Claude Code 拿到足够好的结果，最重要的一点是——给 Claude 一种验证自己工作的方式。如果有这样一个反馈闭环，最终结果的质量能提升 2–3 倍；在他的工作流里，Claude 会测试它落地的每一次代码改动，而不是改完就合并。

Claude 会用 Claude Chrome 扩展测试 http:// 的每一个更改 claude.ai/code。它会打开浏览器，测试界面，然后不断迭代，直到代码正常运行，用户体验也让它满意为止。每个域名的验证内容都不同。可能只是运行一个 bash 命令，运行测试套件，或者在浏览器或手机模拟器中测试应用。一定要投资让它坚固如磐石。 code.claude.com/docs/en/chrome

![Image](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

对小白理解：  
　　真正拉开差距的，不是「Claude 写了多少行代码」，而是「Claude 有没有习惯写完就自测」。让 AI 像好工程师一样：每次修改后先自己跑一轮检查，确认通过，再交给你。

继续滑动看下一个

运营人黎子的AI学习日记

向上滑动看下一个