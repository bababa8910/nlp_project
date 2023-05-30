import os
from django.conf import settings
from collections import Counter
from paddlenlp import Taskflow
from pyecharts import options as opts
from pyecharts.charts import WordCloud
from pyecharts.globals import SymbolType
import jieba.analyse
import paddle
paddle.disable_static()


# 加载NER模型
ner = Taskflow("ner", entity_only=True)

# 定义梦境分析函数
def ciyun_analysis(dream):
    # 使用NER获取梦境中的实体
    entities = ner(dream)
    entities_list = [(entity[0], entity[1]) for entity in entities]

    # 使用TextRank获取关键词
    textrank_keywords = jieba.analyse.textrank(dream, topK=30, withWeight=False)

    # 生成词频统计
    word_freq = Counter(jieba.lcut(dream))
    keywords_freq = [(keyword, word_freq[keyword]) for keyword in textrank_keywords]

    # 生成词云
    word_cloud_data = [(keyword, word_freq[keyword]) for keyword in textrank_keywords]
    wordcloud = (
        WordCloud()
        .add("", word_cloud_data, word_size_range=[20, 100], shape=SymbolType.DIAMOND)
        .set_global_opts(title_opts=opts.TitleOpts(title="Dream Keywords WordCloud"))
        .render(os.path.join(settings.BASE_DIR, 'static', 'dream_keywords_wordcloud.html'))  # 指定正确的文件路径
    )

    # 返回分析结果
    return {
        "entities": entities_list,
        "keywords_freq": keywords_freq,
        "wordcloud": 'dream_keywords_wordcloud.html'  # We just need the filename here
    }
print(os.path.join(settings.BASE_DIR, 'static', 'dream_keywords_wordcloud.html'))