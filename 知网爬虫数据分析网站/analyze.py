import json
import os.path
import tempfile
import atexit
import matplotlib.pyplot as plt
import jieba
temp_file=None

def bar_graph(articles):
    global temp_file
    plt.rcParams['font.sans-serif'] = ['SimHei']

    articles = articles.decode('utf8').replace("'", '"').replace("摘要", '').replace("【】", "")

    articles = json.loads((articles))
    keywords = {}
    for article in articles:
        text = article['title'] + article['content']
        words = jieba.cut(text)
        for word in words:
            if len(word) > 1:
                if word in keywords:
                    keywords[word] += 1
                else:
                    keywords[word] = 1
    sorted_kwd = sorted(keywords.items(), key=lambda x: x[1], reverse=True)
    words = []
    counts = []
    for keyword, count in sorted_kwd[0:30]:
        words.append(keyword)
        counts.append(count)
    plt.barh(words, counts)
    plt.xlabel('数量')
    plt.ylabel('关键词')
    plt.title('关键词数量关系图')
    for i, v in enumerate(counts):
        plt.text(v, i, str(v), va='bottom')
    temp_file = tempfile.NamedTemporaryFile(suffix='.svg', delete=False)

    plt.savefig(temp_file.name)
    plt.close()
    return temp_file.name
