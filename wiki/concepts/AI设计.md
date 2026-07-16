---
tags:
  - "索引/核心概念"
相关概念:
  - "[[wiki/concepts/内容创作|内容创作]]"
  - "[[wiki/concepts/AI工具|AI工具]]"
---
# AI设计

这是内容库中的核心概念节点，用于连接相关选题、文章项目和外部素材。

## 相邻概念

- [[wiki/concepts/内容创作|内容创作]]
- [[wiki/concepts/AI工具|AI工具]]

## 相关内容

```dataview
TABLE WITHOUT ID file.link AS "内容", file.tags AS "阶段或主题"
WHERE contains(相关概念, this.file.link)
SORT file.mtime DESC
```
