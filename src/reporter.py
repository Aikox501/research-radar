"""
HTML 报告生成模块
生成自包含的 HTML 文件，内嵌数据和交互功能
"""
import json
import html


def _make_html(papers_json, topics_json, cluster_json, query):
    """构建 HTML 内容（不用 f-string，避免花括号冲突）"""

    # 分页数据：只取前100篇
    papers_slice = papers_json[:100]

    # 用字符串替换的方式注入数据，避免 f-string 与 JS 花括号冲突
    HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ResearchRadar - 学术前沿追踪报告</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f5f7fa; color: #333; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px 40px; }
        .header h1 { font-size: 28px; margin-bottom: 8px; }
        .header p { opacity: 0.9; font-size: 14px; }
        .query-badge { display: inline-block; background: rgba(255,255,255,0.2); padding: 4px 12px; border-radius: 20px; font-size: 13px; margin-top: 8px; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .stats { display: flex; gap: 15px; margin-bottom: 20px; flex-wrap: wrap; }
        .stat-card { background: white; border-radius: 10px; padding: 20px; flex: 1; min-width: 150px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
        .stat-card .num { font-size: 32px; font-weight: bold; color: #667eea; }
        .stat-card .label { font-size: 13px; color: #888; margin-top: 4px; }
        .tabs { display: flex; gap: 5px; margin-bottom: 20px; border-bottom: 2px solid #e0e0e0; }
        .tab { padding: 10px 20px; cursor: pointer; border: none; background: none; font-size: 15px; color: #888; border-bottom: 2px solid transparent; margin-bottom: -2px; }
        .tab.active { color: #667eea; border-bottom-color: #667eea; font-weight: 600; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        .paper-card { background: white; border-radius: 10px; padding: 20px; margin-bottom: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); transition: transform 0.2s; }
        .paper-card:hover { transform: translateY(-2px); box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        .paper-title { font-size: 17px; font-weight: 600; color: #222; margin-bottom: 8px; line-height: 1.4; }
        .paper-title a { color: inherit; text-decoration: none; }
        .paper-title a:hover { color: #667eea; }
        .paper-summary { font-size: 14px; color: #555; line-height: 1.6; margin-bottom: 8px; }
        .paper-summary-zh { font-size: 13px; color: #444; line-height: 1.6; margin-bottom: 8px; padding: 10px; background: #f0f4ff; border-radius: 6px; }
        .paper-meta { display: flex; gap: 15px; font-size: 12px; color: #999; flex-wrap: wrap; align-items: center; }
        .paper-meta .tag { background: #f0f4ff; color: #667eea; padding: 2px 8px; border-radius: 10px; font-size: 11px; }
        .paper-meta .score { color: #f59e0b; font-weight: 600; }
        .hot-topics { display: flex; flex-wrap: wrap; gap: 8px; }
        .topic-tag { background: white; border: 1px solid #e0e0e0; padding: 6px 14px; border-radius: 20px; font-size: 13px; display: flex; align-items: center; gap: 6px; }
        .topic-tag .count { background: #667eea; color: white; border-radius: 10px; padding: 1px 7px; font-size: 11px; }
        .cluster-section { margin-bottom: 25px; }
        .cluster-header { font-size: 18px; font-weight: 600; color: #667eea; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 2px solid #f0f0f0; }
        .search-box { width: 100%%; padding: 12px 15px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px; margin-bottom: 15px; }
        .no-data { text-align: center; padding: 60px 20px; color: #aaa; font-size: 15px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔭 ResearchRadar</h1>
        <p>AI 领域学术前沿追踪报告</p>
        <span class="query-badge">查询: __QUERY__</span>
    </div>
    <div class="container">
        <div class="stats">
            <div class="stat-card"><div class="num" id="stat-total">0</div><div class="label">论文总数</div></div>
            <div class="stat-card"><div class="num" id="stat-avg-score">0</div><div class="label">平均评分</div></div>
            <div class="stat-card"><div class="num" id="stat-top-keyword">-</div><div class="label">最热关键词</div></div>
            <div class="stat-card"><div class="num" id="stat-date">-</div><div class="label">最新发表</div></div>
        </div>
        <div class="tabs">
            <button class="tab active" onclick="switchTab('papers')">📄 论文列表</button>
            <button class="tab" onclick="switchTab('topics')">🔥 热点话题</button>
            <button class="tab" onclick="switchTab('clusters')">🗂️ 话题聚类</button>
        </div>
        <div id="tab-papers" class="tab-content active">
            <input type="text" class="search-box" id="search-box" placeholder="🔍 搜索论文标题或摘要..." oninput="filterPapers()">
            <div id="papers-list"></div>
        </div>
        <div id="tab-topics" class="tab-content">
            <div class="hot-topics" id="topics-list"></div>
        </div>
        <div id="tab-clusters" class="tab-content">
            <div id="clusters-list"></div>
        </div>
    </div>
    <script>
        var PAPERS = __PAPERS__;
        var TOPICS = __TOPICS__;
        var CLUSTERS = __CLUSTERS__;

        // 初始化统计
        document.getElementById('stat-total').textContent = PAPERS.length;
        if (PAPERS.length > 0) {
            var avg = (PAPERS.reduce(function(s, p) { return s + p.score; }, 0) / PAPERS.length).toFixed(2);
            document.getElementById('stat-avg-score').textContent = avg;
            document.getElementById('stat-date').textContent = PAPERS[0].published;
        }
        if (TOPICS.length > 0) {
            document.getElementById('stat-top-keyword').textContent = TOPICS[0].word;
        }

        // Tab 切换
        function switchTab(name) {
            document.querySelectorAll('.tab').forEach(function(t) { t.classList.remove('active'); });
            document.querySelectorAll('.tab-content').forEach(function(c) { c.classList.remove('active'); });
            event.target.classList.add('active');
            document.getElementById('tab-' + name).classList.add('active');
        }

        // 渲染论文列表
        function renderPapers(list) {
            var container = document.getElementById('papers-list');
            if (!list || list.length === 0) {
                container.innerHTML = '<div class="no-data">暂无数据</div>';
                return;
            }
            container.innerHTML = list.map(function(p) {
                var authors = p.authors.slice(0, 3).join(', ') + (p.authors.length > 3 ? ' 等' : '');
                var zhHtml = p.summary_zh ? '<div class="paper-summary-zh">🇨🇳 ' + escapeHtml(p.summary_zh) + '</div>' : '';
                return '<div class="paper-card">' +
                    '<div class="paper-title"><a href="' + p.pdf_url + '" target="_blank">' + escapeHtml(p.title) + '</a></div>' +
                    '<div class="paper-summary">' + escapeHtml(p.summary.substring(0, 300)) + (p.summary.length > 300 ? '...' : '') + '</div>' +
                    zhHtml +
                    '<div class="paper-meta">' +
                    '<span>📅 ' + p.published + '</span>' +
                    '<span>👤 ' + escapeHtml(authors) + '</span>' +
                    '<span class="score">⭐ ' + p.score + '</span>' +
                    '</div></div>';
            }).join('');
        }

        function escapeHtml(str) {
            var div = document.createElement('div');
            div.textContent = str;
            return div.innerHTML;
        }

        // 搜索过滤
        function filterPapers() {
            var kw = document.getElementById('search-box').value.toLowerCase();
            var filtered = PAPERS.filter(function(p) {
                return p.title.toLowerCase().indexOf(kw) !== -1 || p.summary.toLowerCase().indexOf(kw) !== -1;
            });
            renderPapers(filtered);
        }

        // 渲染热点话题
        function renderTopics() {
            var container = document.getElementById('topics-list');
            container.innerHTML = TOPICS.map(function(t) {
                return '<div class="topic-tag">' + t.word + ' <span class="count">' + t.count + '</span></div>';
            }).join('');
        }

        // 渲染聚类
        function renderClusters() {
            var container = document.getElementById('clusters-list');
            var keys = Object.keys(CLUSTERS);
            if (keys.length === 0) {
                container.innerHTML = '<div class="no-data">暂无聚类数据</div>';
                return;
            }
            container.innerHTML = keys.map(function(kw) {
                var papers = CLUSTERS[kw];
                var items = papers.map(function(p) {
                    return '<div style="padding:6px 0; border-bottom:1px solid #f0f0f0;">' +
                        '<a href="' + p.pdf_url + '" target="_blank" style="color:#333; text-decoration:none;">' + escapeHtml(p.title.substring(0, 80)) + '</a>' +
                        '<span style="color:#f59e0b; font-size:12px; margin-left:8px;">⭐' + p.score + '</span></div>';
                }).join('');
                return '<div class="cluster-section"><div class="cluster-header">🏷️ ' + kw + ' (' + papers.length + ' 篇)</div>' + items + '</div>';
            }).join('');
        }

        // 初始化
        renderPapers(PAPERS);
        renderTopics();
        renderClusters();
    </script>
</body>
</html>'''

    # 替换占位符（用 __XXX__ 避免与 JS 花括号冲突）
    html_out = HTML_TEMPLATE
    html_out = html_out.replace('__QUERY__', html.escape(query or '全部'))
    html_out = html_out.replace('__PAPERS__', papers_json)
    html_out = html_out.replace('__TOPICS__', topics_json)
    html_out = html_out.replace('__CLUSTERS__', cluster_json)
    # 修复 CSS 中的 %% (由 .replace('%%', '%') 处理)
    html_out = html_out.replace('%%', '%')

    return html_out


def generate_html_report(papers, hot_topics, clusters, query, output_path):
    """
    生成自包含的 HTML 报告
    """
    print("📝 正在生成 HTML 报告...")

    import os
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)

    # 准备数据
    papers_json_list = []
    for p in papers[:100]:
        papers_json_list.append({
            'id': p.get('id', ''),
            'title': p.get('title', ''),
            'summary': p.get('summary', '')[:500],
            'summary_zh': p.get('summary_zh', '')[:500],
            'published': p.get('published', ''),
            'authors': p.get('authors', [])[:5],
            'pdf_url': p.get('pdf_url', ''),
            'score': round(p.get('score', 0), 3),
        })

    papers_data = json.dumps(papers_json_list, ensure_ascii=False)

    topics_data = json.dumps(hot_topics[:20], ensure_ascii=False)

    cluster_data = {}
    for kw, plist in list(clusters.items())[:10]:
        cluster_data[kw] = [{'title': p.get('title', ''), 'score': round(p.get('score', 0), 3), 'pdf_url': p.get('pdf_url', '')} for p in plist[:8]]
    cluster_json = json.dumps(cluster_data, ensure_ascii=False)

    html_content = _make_html(papers_data, topics_data, cluster_json, query)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("✅ HTML 报告已生成: " + output_path)
    return output_path


if __name__ == '__main__':
    test_papers = [{'title': 'Test Paper', 'summary': 'This is a test.', 'summary_zh': '这是测试。',
                    'published': '2024-01-01', 'authors': ['A', 'B'], 'pdf_url': '', 'score': 0.9, 'id': 'test'}]
    test_topics = [{'word': 'llm', 'count': 10}]
    test_clusters = {'llm': [{'title': 'Test', 'score': 0.9, 'pdf_url': ''}]}
    generate_html_report(test_papers, test_topics, test_clusters, 'llm', 'test_output.html')
    print("测试报告已生成: test_output.html")
