"""
热点聚类分析模块
对论文摘要提取关键词，统计热点话题
"""
import re
from collections import Counter


# 停用词（英文常见无意义词）
STOP_WORDS = {
    'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'as', 'is', 'are', 'was', 'were', 'be',
    'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
    'would', 'should', 'could', 'may', 'might', 'can', 'this', 'that',
    'these', 'those', 'we', 'our', 'us', 'you', 'your', 'they', 'their',
    'it', 'its', 'i', 'me', 'my', 'mine', 'also', 'however', 'more',
    'most', 'many', 'much', 'such', 'no', 'not', 'only', 'very', 'even',
    'still', 'already', 'yet', 'both', 'each', 'few', 'several', 'new',
    'one', 'two', 'first', 'second', 'than', 'then', 'now', 'into', 'out',
    'up', 'down', 'over', 'under', 'again', 'further', 'once', 'here',
    'there', 'all', 'between', 'through', 'during', 'before', 'after',
    'above', 'below', 'since', 'while', 'about', 'between', 'through',
    'during', 'before', 'after', 'above', 'below', 'since', 'while',
    'propose', 'proposed', 'using', 'used', 'use', 'show', 'shown', 'result',
    'results', 'paper', 'approach', 'method', 'methods', 'model', 'models',
    'based', 'present', 'presented', 'study', 'studies', 'experimental',
    'experiment', 'experiments', 'evaluation', 'evaluate', 'analysis', 'analyze',
    'learning', 'network', 'networks', 'data', 'set', 'sets', 'state',
    'different', 'various', 'including', 'compared', 'comparison', 'performance',
    'improve', 'improved', 'improvement', 'achieve', 'achieved', 'achieving',
    'high', 'higher', 'highest', 'low', 'lower', 'lowest', 'better', 'best',
    'good', 'great', 'large', 'small', 'well', 'widely', 'recent', 'recently',
}


def extract_keywords(text, min_len=3, max_words=50):
    """
    从文本中提取关键词（简单词频统计）
    """
    # 转小写，只保留字母
    words = re.findall(r'\b[a-z]{' + str(min_len) + r',}\b', text.lower())
    # 过滤停用词
    words = [w for w in words if w not in STOP_WORDS]
    return words


def analyze_hot_topics(papers, top_n=20):
    """
    分析热点话题
    :param papers: 论文列表
    :param top_n: 返回前 N 个热点词
    :return: [{'word': 'llm', 'count': 42}, ...]
    """
    print("🔥 正在分析热点话题...")

    all_words = []
    for paper in papers:
        text = (paper.get('title', '') + ' ' + paper.get('summary', ''))
        words = extract_keywords(text)
        all_words.extend(words)

    counter = Counter(all_words)
    hot_topics = [{'word': w, 'count': c} for w, c in counter.most_common(top_n)]

    print(f"✅ 热点分析完成，发现 {len(hot_topics)} 个高频关键词")
    return hot_topics


def cluster_by_keyword(papers, top_keywords=10):
    """
    按高频关键词对论文进行聚类分组
    返回：{keyword: [paper, ...], ...}
    """
    hot_topics = analyze_hot_topics(papers, top_n=top_keywords)
    top_words = [item['word'] for item in hot_topics]

    clusters = {w: [] for w in top_words}

    for paper in papers:
        text = (paper.get('title', '') + ' ' + paper.get('summary', '')).lower()
        for word in top_words:
            if word in text and len(clusters[word]) < 10:  # 每个话题最多10篇
                clusters[word].append(paper)
                break  # 一篇论文归到第一个匹配的话题

    # 过滤空分组
    clusters = {k: v for k, v in clusters.items() if v}

    print(f"✅ 聚类完成，形成 {len(clusters)} 个话题分组")
    return clusters


if __name__ == '__main__':
    # 测试
    test_papers = [
        {'title': 'Large Language Models are Awesome', 'summary': 'We study large language models and diffusion models.'},
        {'title': 'Diffusion Models for Image Generation', 'summary': 'Diffusion models achieve state-of-the-art results.'},
    ]
    topics = analyze_hot_topics(test_papers, top_n=5)
    for t in topics:
        print(f"  {t['word']}: {t['count']}")
