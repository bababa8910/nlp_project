# 梦境解析：分析梦境元素的潜在心理含义
# NLP技术：文本分词、情感分析

from paddlenlp import Taskflow
import jieba

# 定义一个字典，包含梦境元素和它们的潜在心理含义
dream_dictionary = {
    "飞翔": "自由，逃避",
    "追赶": "压力，逃避",
    "死亡": "结束，新的开始",
    "考试": "压力，对能力的怀疑",
    "坠落": "不稳定，恐惧",
    "水": "意识的流动，情感的变化",
    "火": "愤怒，热情，毁灭",
    "树": "生命力，成长",
    "车辆": "生活的进程，自我控制",
    "房屋": "自我，身体",
    "赤裸": "真实，脆弱",
    "蛇": "恐惧，智慧，性欲",
    "婴儿": "新的开始，无邪",
    "武器": "攻击性，防御性",
    "金钱": "自尊，能力，价值",
    "花": "爱，美，生命力"
}

# 使用PaddleNLP进行情感分析
senta = Taskflow("sentiment_analysis")


def analyze_dream(dream_description):
    # 使用jieba分词
    words = jieba.cut(dream_description)

    # 情感分析
    sentiment = senta(dream_description)
    sentiment_result = sentiment[0]
    sentiment_dict = {"text": sentiment_result['text'], "label": sentiment_result['label'], "score": sentiment_result['score']}

    # 梦境元素的潜在心理含义
    elements = []
    for word in words:
        if word in dream_dictionary:
            elements.append((word, dream_dictionary[word]))

    # 返回情感分析结果和梦境元素
    return sentiment_dict, elements
