"""
arXiv 论文抓取模块
使用 arXiv API（无需 Key，完全免费）
"""
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import time


ARXIV_API = "http://export.arxiv.org/api/query"
NS = {'atom': 'http://www.w3.org/2005/Atom'}


def fetch_papers(query, max_results=50, sort_by='submittedDate', ascending=False):
    """
    抓取 arXiv 论文
    :param query: 搜索关键词，如 "large language model"
    :param max_results: 最多返回论文数
    :return: list[dict] 论文列表
    """
    params = {
        'search_query': f'all:{query}',
        'start': 0,
        'max_results': max_results,
        'sortBy': sort_by,
        'sortOrder': 'ascending' if ascending else 'descending'
    }
    url = ARXIV_API + '?' + urllib.parse.urlencode(params)

    print(f"🔍 正在抓取 arXiv 论文: {query} (最多 {max_results} 篇)...")

    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            xml_data = resp.read()
    except Exception as e:
        print(f"❌ 抓取失败: {e}")
        return []

    root = ET.fromstring(xml_data)
    entries = root.findall('atom:entry', NS)

    papers = []
    for entry in entries:
        try:
            paper = {
                'id': entry.find('atom:id', NS).text.strip(),
                'title': entry.find('atom:title', NS).text.strip().replace('\n', ' '),
                'summary': entry.find('atom:summary', NS).text.strip().replace('\n', ' '),
                'published': entry.find('atom:published', NS).text[:10],
                'updated': entry.find('atom:updated', NS).text[:10],
                'authors': [a.find('atom:name', NS).text for a in entry.findall('atom:author', NS)],
                'pdf_url': '',
            }
            # 提取 PDF 链接
            for link in entry.findall('atom:link', NS):
                if link.get('title') == 'pdf':
                    paper['pdf_url'] = link.get('href')
                    break
            papers.append(paper)
        except Exception as e:
            print(f"⚠️  跳过一篇解析失败的论文: {e}")
            continue

    print(f"✅ 成功抓取 {len(papers)} 篇论文")
    return papers


def fetch_by_category(category, max_results=50):
    """
    按 arXiv 分类抓取，如 cs.AI, cs.CL, cs.CV 等
    """
    params = {
        'search_query': f'cat:{category}',
        'start': 0,
        'max_results': max_results,
        'sortBy': 'submittedDate',
        'sortOrder': 'descending'
    }
    url = ARXIV_API + '?' + urllib.parse.urlencode(params)
    print(f"🔍 正在抓取分类 {category} 的最新论文...")

    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            xml_data = resp.read()
    except Exception as e:
        print(f"❌ 抓取失败: {e}")
        return []

    root = ET.fromstring(xml_data)
    entries = root.findall('atom:entry', NS)

    papers = []
    for entry in entries:
        try:
            paper = {
                'id': entry.find('atom:id', NS).text.strip(),
                'title': entry.find('atom:title', NS).text.strip().replace('\n', ' '),
                'summary': entry.find('atom:summary', NS).text.strip().replace('\n', ' '),
                'published': entry.find('atom:published', NS).text[:10],
                'updated': entry.find('atom:updated', NS).text[:10],
                'authors': [a.find('atom:name', NS).text for a in entry.findall('atom:author', NS)],
                'pdf_url': '',
            }
            for link in entry.findall('atom:link', NS):
                if link.get('title') == 'pdf':
                    paper['pdf_url'] = link.get('href')
                    break
            papers.append(paper)
        except Exception:
            continue

    print(f"✅ 成功抓取 {len(papers)} 篇论文")
    return papers


if __name__ == '__main__':
    papers = fetch_papers("large language model", max_results=5)
    for p in papers[:3]:
        print(f"- {p['title'][:60]}...")
