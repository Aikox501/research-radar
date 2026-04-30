"""
论文评分与筛选模块
综合考虑：发表时间（越新越高）、引用量（如有）、标题相关性
"""

from datetime import datetime


def compute_freshness_score(published_date_str):
    """
    计算新鲜度得分：2024年之后发表的论文得分更高
    返回 0~1 之间的分数
    """
    try:
        pub_date = datetime.strptime(published_date_str, '%Y-%m-%d')
        now = datetime.now()
        days_old = (now - pub_date).days
        if days_old < 0:
            days_old = 0
        # 越新分数越高，180天内满分，之后衰减
        if days_old <= 180:
            return 1.0
        elif days_old <= 365:
            return 0.7
        elif days_old <= 730:
            return 0.4
        else:
            return 0.2
    except Exception:
        return 0.5


def compute_query_relevance(title, summary, query):
    """
    计算查询相关性（简单关键词匹配）
    返回 0~1 之间的分数
    """
    if not query:
        return 1.0
    text = (title + ' ' + summary).lower()
    query_words = query.lower().split()
    matches = sum(1 for w in query_words if w in text)
    return min(matches / max(len(query_words), 1), 1.0)


def score_paper(paper, query='', weight_freshness=0.6, weight_relevance=0.4):
    """
    综合评分
    :param paper: 论文 dict
    :param query: 搜索关键词
    :return: 综合得分 (0~1)
    """
    freshness = compute_freshness_score(paper.get('published', '2020-01-01'))
    relevance = compute_query_relevance(paper.get('title', ''), paper.get('summary', ''), query)

    # 综合得分
    score = freshness * weight_freshness + relevance * weight_relevance
    return round(score, 4)


def rank_papers(papers, query='', top_n=None):
    """
    对论文进行评分排序
    :param papers: 论文列表
    :param query: 搜索关键词（用于相关性计算）
    :param top_n: 只返回前 N 篇，None 返回全部
    :return: 排序后的论文列表（含 score 字段）
    """
    print("⭐ 正在对论文进行评分排序...")

    for paper in papers:
        paper['score'] = score_paper(paper, query)

    ranked = sorted(papers, key=lambda x: x['score'], reverse=True)

    if top_n:
        ranked = ranked[:top_n]

    print(f"✅ 评分完成，TOP1 得分: {ranked[0]['score'] if ranked else 'N/A'}")
    return ranked


def filter_by_score(papers, min_score=0.3):
    """
    按最低分数过滤论文
    """
    filtered = [p for p in papers if p.get('score', 0) >= min_score]
    print(f"📊 过滤后保留 {len(filtered)}/{len(papers)} 篇 (min_score={min_score})")
    return filtered


if __name__ == '__main__':
    test_papers = [
        {'title': 'LLM Survey', 'summary': 'A survey on large language models.', 'published': '2024-01-15'},
        {'title': 'Old Paper', 'summary': 'Some old work.', 'published': '2020-01-01'},
    ]
    ranked = rank_papers(test_papers, query='LLM')
    for p in ranked:
        print(f"  {p['title']} -> score={p['score']}")
