# frozen_string_literal: true

# 为内容库中的文章、选题和素材补充统一的 Obsidian 层级标签。
# 重复运行是安全的：已有标签会保留，新标签只会追加一次。

ROOTS = %w[01选题库 01-选题库 02-稿件库 03素材库 Clippings].freeze
MANAGED_PREFIXES = %w[内容阶段/ 内容载体/ 内容类型/ 主题/ 工具/ 受众/ 概念/ 来源/].freeze

def scope_tags(path)
  return ['来源/外部剪藏'] if path.start_with?('Clippings/')
  return ['内容载体/公众号', '来源/历史发布'] if path.start_with?('03素材库/01-历史文章素材/')

  ['内容载体/公众号']
end

def stage_tags(path)
  return ['内容阶段/选题'] if path.start_with?('01选题库/', '01-选题库/') || path.match?(/选题分析|选题池/)
  return ['内容阶段/访谈'] if path.include?('访谈记录')
  return ['内容阶段/大纲'] if path.include?('文章大纲')
  return ['内容阶段/改稿'] if path.match?(/改稿记录|公众号修改版/)
  return ['内容阶段/定稿'] if path.include?('定稿') && !path.include?('定型验证')
  return ['内容阶段/核验'] if path.match?(/核验|验证报告|资料来源/)
  return ['内容阶段/发布记录'] if path.match?(/同步结果|重同步结果|草稿箱同步结果|发布说明|修正说明|目录说明|路径修正说明/)
  return ['内容阶段/配图素材'] if path.match?(/配图|素材清单|文章配图素材/)
  return ['内容阶段/发布稿'] if path.match?(/公众号发布正文|公众号精排版正文|发布包\.md|长文发布包|图文发布包/)
  return ['内容阶段/初稿'] if path.match?(/初稿|重点标注版/)
  return ['内容阶段/历史文章'] if path.start_with?('03素材库/01-历史文章素材/')
  return ['内容阶段/外部素材'] if path.start_with?('03素材库/', 'Clippings/')

  ['内容阶段/创作中']
end

def topic_tags(path)
  case path
  when /ai入门/i
    ['内容类型/科普', '主题/AI入门', '受众/AI新手']
  when /AI能操作电脑了但你真的知道它在动哪里|AI\+能操作电脑了/
    ['内容类型/科普', '主题/AI安全', '主题/Mac使用', '主题/AI智能体', '受众/AI新手']
  when /Codex宠物/
    ['内容类型/教程', '主题/AI工具', '工具/Codex', '工具/hatch-pet', '受众/运营人']
  when /Codex自动操作浏览器/
    ['内容类型/工作流', '主题/AI自动化', '工具/Codex', '工具/浏览器', '受众/运营人']
  when /Codex调用飞书CLI/
    ['内容类型/工作流', '主题/AI自动化', '主题/内容创作', '工具/Codex', '工具/飞书', '受众/运营人']
  when /Cowart画板/
    ['内容类型/教程', '主题/AI设计', '主题/内容创作', '工具/Cowart', '受众/运营人']
  when /别只会写提示词AI开始自己跑循环/
    ['内容类型/方法论', '主题/AI自动化', '主题/智能体工作流', '概念/Loop-engineering', '受众/运营人']
  when /语音输入软件横评|语音转文字/
    ['内容类型/工具测评', '主题/AI工具', '主题/语音输入', '受众/内容创作者']
  when /运营人为什么用Obsidian搭AI知识库|Obsidian.*Claude code.*AI.*知识库拆解/
    ['内容类型/方法论', '主题/知识管理', '主题/内容创作', '工具/Obsidian', '受众/运营人']
  when /影响力金句|积极向上能力金句/
    ['内容类型/金句', '主题/个人成长', '主题/个人影响力']
  when /请你吃肯德基早餐/
    ['内容类型/活动文案', '主题/社群运营']
  when /快捷键/
    ['内容类型/教程', '主题/效率提升']
  when /AI内容工厂搭建指南/
    ['内容类型/方法论', '主题/内容创作', '主题/AI自动化', '主题/内容工作流', '受众/内容创作者']
  when /Spec Kit/
    ['内容类型/工具解读', '主题/AI编程', '主题/规范驱动开发', '工具/GitHub', '受众/开发者']
  when /运营视频生成工作流/
    ['内容类型/工作流', '主题/AI视频', '主题/内容创作', '受众/运营人']
  when /Claude Code 之父的真实工作流/
    ['内容类型/案例', '主题/AI编程', '主题/智能体工作流', '工具/Claude-Code', '受众/开发者']
  when /电脑白痴也能搞定.*Claude Code/
    ['内容类型/教程', '主题/AI编程', '主题/AI工具', '工具/Claude-Code', '受众/AI新手']
  when /沉静式翻译插件/
    ['内容类型/工具推荐', '主题/AI工具', '主题/翻译', '受众/运营人']
  when /得到get笔记/
    ['内容类型/工具推荐', '主题/知识管理', '主题/灵感管理', '工具/得到笔记', '受众/内容创作者']
  when /腾讯元器/
    ['内容类型/工具推荐', '主题/AI智能体', '主题/内容创作', '工具/腾讯元器', '受众/运营人']
  when /出海seo流量获取/i
    ['内容类型/案例', '主题/出海增长', '主题/SEO', '受众/创业者']
  when /小红书电商\+aiskill搭建分享/i
    ['内容类型/案例', '主题/小红书电商', '主题/AI自动化', '主题/技能搭建', '受众/创业者']
  when /小红书电商，持续爆单心路历程/
    ['内容类型/案例', '主题/小红书电商', '主题/电商运营', '受众/创业者']
  else
    ['主题/AI内容创作']
  end
end

def normalize_broken_frontmatter(frontmatter)
  # 两篇早期笔记用“:+”代替“: ”，会让 YAML 被当成普通字符串。
  return frontmatter unless frontmatter.lines.any? { |line| line.match?(/^[^:#\n]+:\+/) }

  frontmatter.lines.map do |line|
    match = line.match(/^([^:#\n]+):\+(.*)$/)
    next line unless match

    value = match[2].tr('+', ' ')
    "#{match[1]}: #{value}\n"
  end.join
end

def merge_tags(frontmatter, new_tags)
  lines = frontmatter.lines
  tag_index = lines.index { |line| line.match?(/^tags:\s*$/) }

  unless tag_index
    suffix = frontmatter.end_with?("\n") || frontmatter.empty? ? '' : "\n"
    return frontmatter + suffix + "tags:\n" + new_tags.map { |tag| "  - \"#{tag}\"\n" }.join
  end

  block_end = tag_index + 1
  block_end += 1 while block_end < lines.length && lines[block_end].match?(/^\s+-\s+/)
  parsed = lines[(tag_index + 1)...block_end].map do |line|
    value = line[/^\s+-\s+["']?([^"'\n]+)["']?\s*$/, 1]
    [line, value&.strip]
  end.compact
  kept = parsed.reject do |_line, value|
    value && MANAGED_PREFIXES.any? { |prefix| value.start_with?(prefix) }
  end
  kept_lines = kept.map(&:first)
  existing = kept.map(&:last).compact
  additions = new_tags.reject { |tag| existing.include?(tag) }
  lines[(tag_index + 1)...block_end] = kept_lines + additions.map { |tag| "  - \"#{tag}\"\n" }
  lines.join
end

def update_file(path)
  content = File.read(path)
  tags = (stage_tags(path) + scope_tags(path) + topic_tags(path)).uniq

  if content.start_with?("---\n")
    closing = content.index(/^---\s*$\n?/, 4)
    raise "找不到 frontmatter 结束标记：#{path}" unless closing

    frontmatter = content[4...closing]
    frontmatter = normalize_broken_frontmatter(frontmatter)
    updated = "---\n#{merge_tags(frontmatter, tags)}---\n#{content[(closing + content[closing..].index("\n").to_i + 1)..]}"
  else
    yaml = tags.map { |tag| "  - \"#{tag}\"\n" }.join
    updated = "---\ntags:\n#{yaml}---\n#{content}"
  end

  return false if updated == content

  File.write(path, updated)
  true
end

files = ROOTS.flat_map { |root| Dir.glob("#{root}/**/*.md") }.sort
changed = files.count { |path| update_file(path) }
puts "已扫描 #{files.length} 篇内容，更新 #{changed} 篇。"
