# frozen_string_literal: true

# 构建低噪音的 Obsidian 知识图谱：
# 过程文件 -> 文章项目索引 -> 核心概念页。
# 标签只承担阶段和少量主题分类，具体关系由双向链接表达。

CONTENT_ROOTS = %w[01选题库 01-选题库 02-稿件库 03素材库 Clippings].freeze
CONCEPT_DIR = 'wiki/concepts'
PROJECT_ROOT = '02-稿件库/01-创作中稿件'

CONCEPTS = {
  'AI入门' => ['AI工具', 'AI安全'],
  'AI安全' => ['AI入门', 'AI智能体'],
  'AI自动化' => ['AI智能体', '内容创作'],
  'AI智能体' => ['AI自动化', 'AI安全'],
  '内容创作' => ['AI自动化', '知识管理', 'AI设计'],
  '知识管理' => ['内容创作', 'AI工具'],
  'AI工具' => ['AI入门', '知识管理'],
  'AI编程' => ['AI智能体', 'AI工具'],
  'AI设计' => ['内容创作', 'AI工具'],
  '个人成长' => ['内容创作'],
  '增长运营' => ['内容创作', 'AI自动化']
}.freeze

PROJECTS = [
  {
    title: 'AI 操作电脑与 Mac 安全',
    folder: "#{PROJECT_ROOT}/AI能操作电脑了但你真的知道它在动哪里吗-20260608",
    concepts: %w[AI安全 AI智能体 AI入门],
    audience: 'AI 新手', type: '科普文章'
  },
  {
    title: 'Codex 宠物安装与自定义',
    folder: "#{PROJECT_ROOT}/Codex宠物安装和自定义指南-20260613",
    concepts: %w[AI工具 内容创作],
    audience: '运营人', type: '工具教程'
  },
  {
    title: 'Codex 自动操作浏览器',
    folder: "#{PROJECT_ROOT}/Codex自动操作浏览器-20260618",
    concepts: %w[AI自动化 内容创作],
    audience: '运营人', type: '工作流文章'
  },
  {
    title: 'Codex 调用飞书 CLI',
    folder: "#{PROJECT_ROOT}/Codex调用飞书CLI公众号文章-20260615",
    concepts: %w[AI自动化 内容创作],
    audience: '运营人', type: '工作流文章'
  },
  {
    title: 'Cowart 画板指哪改哪',
    folder: "#{PROJECT_ROOT}/Cowart画板指哪改哪-20260625",
    concepts: %w[AI设计 内容创作],
    audience: '运营人', type: '工具教程'
  },
  {
    title: 'AI 入门',
    folder: "#{PROJECT_ROOT}/ai入门-20260607",
    concepts: %w[AI入门],
    audience: 'AI 新手', type: '科普文章'
  },
  {
    title: '从提示词到 Loop Engineering',
    folder: "#{PROJECT_ROOT}/别只会写提示词AI开始自己跑循环了-20260623",
    concepts: %w[AI自动化 AI智能体],
    audience: '运营人', type: '方法论文章'
  },
  {
    title: 'AI 语音输入工具横评',
    folder: "#{PROJECT_ROOT}/语音输入软件横评-20260613",
    concepts: %w[AI工具 内容创作],
    audience: '内容创作者', type: '工具测评'
  },
  {
    title: '运营人用 Obsidian 搭 AI 知识库',
    folder: "#{PROJECT_ROOT}/运营人为什么用Obsidian搭AI知识库-20260613",
    concepts: %w[知识管理 内容创作],
    audience: '运营人', type: '方法论文章'
  },
  {
    title: '影响力金句分享',
    index: "#{PROJECT_ROOT}/影响力金句分享-项目索引.md",
    pattern: /影响力金句分享-(?!项目索引).*\.md$/,
    concepts: %w[个人成长 内容创作],
    audience: '个人成长读者', type: '金句内容'
  },
  {
    title: '积极向上能力金句',
    index: "#{PROJECT_ROOT}/积极向上能力金句-项目索引.md",
    pattern: /积极向上能力金句(?!-项目索引).*\.md$/,
    concepts: %w[个人成长 内容创作],
    audience: '个人成长读者', type: '金句内容'
  }
].freeze

STAGE_ORDER = %w[选题 访谈 大纲 初稿 改稿 定稿 发布稿 配图素材 核验 发布记录 创作中 历史文章 外部素材].freeze
MAIN_STAGE_ORDER = %w[选题 访谈 大纲 初稿 改稿 定稿 发布稿].freeze

def split_note(content)
  return ['', content] unless content.start_with?("---\n")

  closing = content.index(/^---\s*$\n?/, 4)
  raise '找不到 frontmatter 结束标记' unless closing

  frontmatter = content[4...closing]
  body_start = closing + content[closing..].index("\n").to_i + 1
  [frontmatter, content[body_start..] || '']
end

def property_range(lines, key)
  index = lines.index { |line| line.match?(/^#{Regexp.escape(key)}:\s*/) }
  return nil unless index

  finish = index + 1
  finish += 1 while finish < lines.length && lines[finish].match?(/^\s+-\s+/)
  index...finish
end

def set_property(frontmatter, key, value_lines)
  lines = frontmatter.lines
  range = property_range(lines, key)
  replacement = Array(value_lines)
  range ? lines[range] = replacement : lines.concat(replacement)
  lines.join
end

def delete_property(frontmatter, key)
  lines = frontmatter.lines
  range = property_range(lines, key)
  lines[range] = [] if range
  lines.join
end

def existing_plain_tags(frontmatter)
  lines = frontmatter.lines
  range = property_range(lines, 'tags')
  return [] unless range

  lines[range].map do |line|
    line[/^\s+-\s+["']?([^"'\n]+)["']?\s*$/, 1]&.strip
  end.compact.select { |tag| tag == 'clippings' }
end

def set_tags(frontmatter, tags)
  tags = (existing_plain_tags(frontmatter) + tags).uniq
  set_property(frontmatter, 'tags', ["tags:\n"] + tags.map { |tag| "  - \"#{tag}\"\n" })
end

def set_scalar(frontmatter, key, value)
  set_property(frontmatter, key, ["#{key}: \"#{value}\"\n"])
end

def set_links(frontmatter, key, links)
  values = links.map { |link| "  - \"[[#{link}]]\"\n" }
  set_property(frontmatter, key, ["#{key}:\n"] + values)
end

def write_note(path, frontmatter, body)
  updated = "---\n#{frontmatter}---\n#{body}"
  return false if File.exist?(path) && File.read(path) == updated

  FileUtils.mkdir_p(File.dirname(path))
  File.write(path, updated)
  true
end

def stage_for(path)
  return '选题' if path.start_with?('01选题库/', '01-选题库/') || path.include?('选题分析')
  return '访谈' if path.include?('访谈记录')
  return '大纲' if path.include?('文章大纲')
  return '改稿' if path.match?(/改稿记录|公众号修改版/)
  return '定稿' if path.include?('定稿') && !path.include?('定型验证')
  return '核验' if path.match?(/核验|验证报告|资料来源/)
  return '发布记录' if path.match?(/同步结果|重同步结果|草稿箱同步结果|发布说明|修正说明|目录说明|路径修正说明/)
  return '配图素材' if path.match?(/配图|素材清单|文章配图素材/)
  return '发布稿' if path.match?(/公众号发布正文|公众号精排版正文|发布包\.md|长文发布包|图文发布包/)
  return '初稿' if path.match?(/初稿|重点标注版/)
  return '历史文章' if path.start_with?('03素材库/01-历史文章素材/')
  return '外部素材' if path.start_with?('03素材库/', 'Clippings/')

  '创作中'
end

def concept_names(path)
  case path
  when /ai入门/i then %w[AI入门]
  when /AI能操作电脑了|AI\+能操作电脑了/ then %w[AI安全 AI智能体]
  when /Codex宠物|沉静式翻译插件|快捷键/ then %w[AI工具]
  when /Codex自动操作浏览器|Codex调用飞书CLI|AI内容工厂/ then %w[AI自动化 内容创作]
  when /Cowart|运营视频生成/ then %w[AI设计 内容创作]
  when /别只会写提示词AI开始自己跑循环/ then %w[AI自动化 AI智能体]
  when /语音输入|语音转文字/ then %w[AI工具 内容创作]
  when /Obsidian|得到get笔记/ then %w[知识管理 内容创作]
  when /影响力金句|积极向上能力金句/ then %w[个人成长 内容创作]
  when /Spec Kit|Claude Code 之父|电脑白痴也能搞定.*Claude Code/ then %w[AI编程 AI工具]
  when /腾讯元器/ then %w[AI智能体 内容创作]
  when /出海seo|小红书电商|肯德基早餐/ then %w[增长运营]
  else %w[内容创作]
  end
end

def source_tag(path)
  return '来源/外部剪藏' if path.start_with?('Clippings/')
  return '来源/历史发布' if path.start_with?('03素材库/01-历史文章素材/')

  nil
end

def index_path(project)
  project[:index] || "#{project[:folder]}/00-项目索引.md"
end

def project_files(project)
  files = if project[:folder]
            Dir.glob("#{project[:folder]}/**/*.md")
          else
            Dir.glob("#{PROJECT_ROOT}/*.md").select { |path| path.match?(project[:pattern]) }
          end
  files.reject { |path| path == index_path(project) }.sort
end

def wiki_target(path)
  path.sub(/\.md$/, '')
end

def link_for(path, alias_text = nil)
  target = wiki_target(path)
  alias_text ? "[[#{target}|#{alias_text}]]" : "[[#{target}]]"
end

def main_chain_for(files)
  grouped = files.group_by { |path| stage_for(path) }
  MAIN_STAGE_ORDER.map { |stage| grouped[stage]&.min_by { |path| File.basename(path).length } }.compact
end

def build_project_index(project, files)
  grouped = files.group_by { |path| stage_for(path) }
  main_chain = main_chain_for(files)

  frontmatter = ''
  frontmatter = set_tags(frontmatter, ['索引/文章项目'] + project[:concepts].first(2).map { |name| "主题/#{name}" })
  frontmatter = set_scalar(frontmatter, '项目名称', project[:title])
  frontmatter = set_scalar(frontmatter, '内容类型', project[:type])
  frontmatter = set_scalar(frontmatter, '目标受众', project[:audience])
  frontmatter = set_links(frontmatter, '相关概念', project[:concepts].map { |name| "#{CONCEPT_DIR}/#{name}|#{name}" })

  body = +"# #{project[:title]}\n\n"
  body << "## 核心概念\n\n"
  body << project[:concepts].map { |name| "- #{link_for("#{CONCEPT_DIR}/#{name}.md", name)}" }.join("\n") << "\n\n"
  unless main_chain.empty?
    body << "## 创作主链\n\n"
    body << main_chain.map { |path| link_for(path, File.basename(path, '.md')) }.join(' → ') << "\n\n"
  end
  body << "## 全部过程材料\n\n"
  STAGE_ORDER.each do |stage|
    next unless grouped[stage]

    body << "### #{stage}\n\n"
    body << grouped[stage].map { |path| "- #{link_for(path, File.basename(path, '.md'))}" }.join("\n") << "\n\n"
  end
  [frontmatter, body]
end

require 'fileutils'

changed = 0
project_members = {}
chain_navigation = {}

PROJECTS.each do |project|
  files = project_files(project)
  project_link = "#{wiki_target(index_path(project))}|#{project[:title]}"
  files.each { |path| project_members[path] = [project, project_link] }
  chain = main_chain_for(files)
  chain.each_with_index do |path, index|
    previous = index.positive? ? chain[index - 1] : nil
    chain_navigation[path] = [previous, chain[index + 1]]
  end
  frontmatter, body = build_project_index(project, files)
  changed += 1 if write_note(index_path(project), frontmatter, body)
end

content_files = CONTENT_ROOTS.flat_map { |root| Dir.glob("#{root}/**/*.md") }.sort
content_files.reject! { |path| PROJECTS.any? { |project| path == index_path(project) } }

content_files.each do |path|
  frontmatter, body = split_note(File.read(path))
  stage = stage_for(path)
  if project_members[path]
    _project, project_link = project_members[path]
    tags = ["内容阶段/#{stage}"]
    frontmatter = set_scalar(frontmatter, '所属项目', "[[#{project_link}]]")
    previous, following = chain_navigation[path]
    if previous
      frontmatter = set_scalar(frontmatter, '上一步', "[[#{wiki_target(previous)}|#{File.basename(previous, '.md')}]]")
    else
      frontmatter = delete_property(frontmatter, '上一步')
    end
    if following
      frontmatter = set_scalar(frontmatter, '下一步', "[[#{wiki_target(following)}|#{File.basename(following, '.md')}]]")
    else
      frontmatter = delete_property(frontmatter, '下一步')
    end
    range = property_range(frontmatter.lines, '相关概念')
    if range
      lines = frontmatter.lines
      lines[range] = []
      frontmatter = lines.join
    end
  else
    concepts = concept_names(path)
    tags = ["内容阶段/#{stage}", source_tag(path), *concepts.first(2).map { |name| "主题/#{name}" }].compact
    frontmatter = set_links(frontmatter, '相关概念', concepts.map { |name| "#{CONCEPT_DIR}/#{name}|#{name}" })
  end
  frontmatter = set_tags(frontmatter, tags)
  changed += 1 if write_note(path, frontmatter, body)
end

CONCEPTS.each do |name, related|
  path = "#{CONCEPT_DIR}/#{name}.md"
  frontmatter = ''
  frontmatter = set_tags(frontmatter, ['索引/核心概念'])
  frontmatter = set_links(frontmatter, '相关概念', related.map { |item| "#{CONCEPT_DIR}/#{item}|#{item}" })
  body = +"# #{name}\n\n"
  body << "这是内容库中的核心概念节点，用于连接相关选题、文章项目和外部素材。\n\n"
  body << "## 相邻概念\n\n"
  body << related.map { |item| "- #{link_for("#{CONCEPT_DIR}/#{item}.md", item)}" }.join("\n") << "\n\n"
  body << "## 相关内容\n\n"
  body << "```dataview\nTABLE WITHOUT ID file.link AS \"内容\", file.tags AS \"阶段或主题\"\nWHERE contains(相关概念, this.file.link)\nSORT file.mtime DESC\n```\n"
  changed += 1 if write_note(path, frontmatter, body)
end

puts "知识图谱构建完成：#{PROJECTS.length} 个文章项目，#{CONCEPTS.length} 个核心概念，本次更新 #{changed} 个文件。"
