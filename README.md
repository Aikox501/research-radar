# 🔭 ResearchRadar

AI 领域学术前沿追踪平台 —— 自动抓取 arXiv 最新论文，智能评分筛选，热点话题聚类，一键生成可视化报告。

## ✨ 功能特性

- 🔍 **智能抓取** — 按关键词或 arXiv 分类自动抓取最新论文
- 🌏 **中文翻译** — 摘要自动翻译为中文（MyMemory 免费 API）
- 🔥 **热点分析** — 关键词词频统计，发现最热研究方向
- 🗂️ **话题聚类** — 自动按热点关键词对论文聚类分组
- ⭐ **智能评分** — 综合考虑发表时间和相关性进行评分排序
- 🌐 **可视化报告** — 生成自包含 HTML 报告，浏览器直接打开

## 🚀 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 基本用法

```bash
# 按关键词搜索（默认 50 篇）
python run.py --query "large language model"

# 按 arXiv 分类搜索
python run.py --category cs.AI

# 自定义数量 + 最低评分过滤
python run.py --query "diffusion model" --max 80 --min-score 0.4

# 跳过翻译（加快速度）
python run.py --query "LLM" --no-translate
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--query` | 搜索关键词 | 无 |
| `--category` | arXiv 分类（cs.AI/cs.CL/cs.CV等） | 无 |
| `--max` | 最多抓取论文数 | 50 |
| `--min-score` | 最低评分，低于此分过滤掉 | 0.0 |
| `--no-translate` | 跳过中文翻译 | False |
| `--output` | 输出 HTML 路径 | output/report.html |

### 常用 arXiv 分类

| 分类代码 | 领域 |
|---------|------|
| `cs.AI` | 人工智能 |
| `cs.CL` | 计算语言学（NLP） |
| `cs.CV` | 计算机视觉 |
| `cs.LG` | 机器学习 |
| `cs.RO` | 机器人 |
| `stat.ML` | 统计机器学习 |

## 📊 报告预览

运行后生成 `output/report.html`，包含三个视图：

- **📄 论文列表** — 按评分排序，支持搜索过滤，附中文摘要
- **🔥 热点话题** — 高频关键词可视化展示
- **🗂️ 话题聚类** — 按热点词分组的论文列表

## 📁 项目结构

```
research-radar/
├── run.py              # 主入口
├── src/
│   ├── fetcher.py     # arXiv 论文抓取
│   ├── translator.py  # 摘要中文翻译
│   ├── analyzer.py    # 热点话题分析
│   ├── scorer.py      # 论文评分排序
│   └── reporter.py    # HTML 报告生成
├── output/            # 生成的报告输出目录
└── requirements.txt   # 依赖列表
```

## 📝 说明

- 翻译使用 [MyMemory API](https://mymemory.translated.net/) 免费接口，每天限 5000 字符
- arXiv API 无需 Key，完全免费
- 生成报告为自包含 HTML，无需服务器，直接浏览器打开

## 📄 License

MIT License
