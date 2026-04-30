"""
摘要中文翻译模块
使用 MyMemory 免费翻译 API（无需 Key，每天 5000字符）
"""
import urllib.request
import urllib.parse
import json
import time


MYMEMORY_API = "https://api.mymemory.translated.net/get"


def translate_to_zh(text, retries=2):
    """
    将英文文本翻译成中文
    :param text: 英文文本
    :param retries: 重试次数
    :return: 中文文本，失败返回原文
    """
    # MyMemory 单次最多 500 字符，截断处理
    if len(text) > 450:
        text = text[:450] + "..."

    params = urllib.parse.urlencode({
        'q': text,
        'langpair': 'en|zh-CN'
    })
    url = MYMEMORY_API + '?' + params

    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'ResearchRadar/1.0'})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                result = data.get('responseData', {}).get('translatedText', '')
                if result and result != text:
                    return result
                else:
                    # 可能超过免费额度，返回空
                    return text
        except Exception as e:
            if attempt == retries - 1:
                return text  # 失败返回原文
            time.sleep(1)

    return text


def translate_papers(papers, max_workers=5):
    """
    批量翻译论文摘要
    为节省 API 调用，只翻译前 N 篇重点论文
    """
    print(f"🌏 正在翻译摘要 (MyMemory 免费API)...")
    translated = 0
    for paper in papers:
        cn = translate_to_zh(paper['summary'])
        paper['summary_zh'] = cn
        translated += 1
        if translated % 10 == 0:
            print(f"   已翻译 {translated}/{len(papers)}...")
        time.sleep(0.5)  # 避免频率限制
    print(f"✅ 翻译完成 ({translated} 篇)")
    return papers


if __name__ == '__main__':
    test = "We propose a novel method for large language model training."
    print(translate_to_zh(test))
