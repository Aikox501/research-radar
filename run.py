#!/usr/bin/env python3
"""
ResearchRadar - AI 学术前沿追踪平台
主入口脚本

用法:
    python run.py --query "large language model" --max 50
    python run.py --category cs.AI --max 50
    python run.py --query "diffusion model" --max 30 --min-score 0.4
"""

import argparse
import sys
import os

# 添加 src 到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from fetcher import fetch_papers, fetch_by_category
from translator import translate_papers
from analyzer import analyze_hot_topics, cluster_by_keyword
from scorer import rank_papers, filter_by_score
from reporter import generate_html_report


def main():
    parser = argparse.ArgumentParser(description='ResearchRadar - AI 学术前沿追踪')
    parser.add_argument('--query', type=str, default='', help='搜索关键词，如 "large language model"')
    parser.add_argument('--category', type=str, default='', help='arXiv 分类，如 cs.AI, cs.CL, cs.CV')
    parser.add_argument('--max', type=int, default=50, help='最多抓取论文数 (默认 50)')
    parser.add_argument('--min-score', type=float, default=0.0, help='最低评分过滤 (默认 0.0，不过滤)')
    parser.add_argument('--no-translate', action='store_true', help='跳过中文翻译（加快速度）')
    parser.add_argument('--output', type=str, default='output/report.html', help='输出 HTML 路径')
    args = parser.parse_args()

    print("=" * 50)
    print("🔭 ResearchRadar - AI 学术前沿追踪平台")
    print("=" * 50)

    # 1. 抓取论文
    if args.category:
        papers = fetch_by_category(args.category, max_results=args.max)
        query = args.category
    elif args.query:
        papers = fetch_papers(args.query, max_results=args.max)
        query = args.query
    else:
        print("❌ 请指定 --query 或 --category")
        sys.exit(1)

    if not papers:
        print("❌ 未抓取到任何论文，请检查关键词或网络")
        sys.exit(1)

    # 2. 评分排序
    papers = rank_papers(papers, query=query)

    # 3. 过滤
    if args.min_score > 0:
        papers = filter_by_score(papers, min_score=args.min_score)

    # 4. 翻译摘要（可选）
    if not args.no_translate:
        papers = translate_papers(papers)
    else:
        for p in papers:
            p['summary_zh'] = ''

    # 5. 热点分析
    hot_topics = analyze_hot_topics(papers, top_n=30)

    # 6. 聚类
    clusters = cluster_by_keyword(papers, top_keywords=10)

    # 7. 生成 HTML 报告
    os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)
    generate_html_report(papers, hot_topics, clusters, query, args.output)

    print("=" * 50)
    print(f"🎉 完成！报告已保存至: {args.output}")
    print(f"   用浏览器打开即可查看")
    print("=" * 50)


if __name__ == '__main__':
    # 直接指定参数，不用命令行
    test_args = ['run.py', '--query', 'LLM', '--max', '10', '--no-translate']
    import sys
    sys.argv = test_args
    main()

