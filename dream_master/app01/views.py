import csv
from urllib.parse import quote, unquote
import pandas as pd

from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def dream_interpreter_view(request):
#     if request.method == 'POST':
#         dream = request.POST['dream']
#         interpretation = dream_interpreter(dream)
#         return JsonResponse({'interpretation': interpretation})
#     else:
#         return JsonResponse({'error': 'Invalid request'}, status=400)


def index_view(request):
    search_query = request.GET.get('search', '')  # 获取搜索查询，如果没有则设为空字符串

    category = "default_category"

    items = []
    with open('data/data0.csv', 'r', encoding='GBK') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['category'] == category:
                if match_search_query(row, search_query):
                    items.append({'dream': row['dream'], 'decode': row['decode']})

    categories = ["人物", "动物", "植物", "物品", "活动", "情感", "生活", "鬼神", "自然", "建筑", "其他"]

    context = {'items': items, 'categories': categories}
    return render(request, 'index.html', context)

def category_view(request, category):
    search_query = request.GET.get('search', '')  # 获取搜索查询，如果没有则设为空字符串

    category = unquote(category)

    items = []  # 定义一个空列表
    if category == "人物":
        data = [
            {"dream": "梦见教练在训练的情景", "decode": " 这都提示着梦者自己的投资不会获得直接利润。"},
            {"dream": "梦到体育教练", "decode": "暗示你的投资不会有利润。"},
            {"dream": "梦见体育教练", "decode": "表示最近自己的事业不会盈利，但是对社会有很大的贡献。"},
            {"dream": "梦见受著名的体育选手指导", "decode": "健康方面将有不韦。"},
            {"dream": "梦见贵人的梦不多", "decode": "能够梦见贵人表示你能够出人头地的机会很大，未来有一番作为。"},
            {"dream": "梦见领袖", "decode": "则表示心灵上得到安详;如果梦见领袖在行事，则会受到赏识。"},
            {"dream": "梦见自己在贵人面前", "decode": "表示将会出人头地;但若梦中与贵人为对等地位，则有忧事将至。"},
            {"dream": "梦见与贵族说话",
             "decode": "若平静的说话，表示会发生烦恼的事;若是对方骂你，表示幸运即将来临;相反的，若你骂对方，则为凶兆，一定会遭遇灾难。"},
            {"dream": "梦见贵族人士骂你", "decode": "表示你的幸运即将来临。"},
            {"dream": "梦见贵族",
             "decode": "此梦是在暗喻着，梦者也将会在近期获得较高的社会地位或丰厚的财富等，梦者的日常生活也将会因此而越来越美好。"},
            {"dream": "梦见某个家庭成员或朋友不见了", "decode": "缺席者要遭厄运。"},
            {"dream": "梦见自己不在办公室",
             "decode": "却在公园等处散步，或在电影院看电影等，预示着心术不正的朋友给自己造成难以忍受的损失。"},
            {"dream": "梦见久未见面的人时", "decode": "此人将会很快归来。"},
            {"dream": "梦见有人缺席", "decode": "说明这个人就是你需要特别留意的人，可能他你就是你的心上人。"},
            {"dream": "梦见母亲缺席了", "decode": "意味着丧失生命等，这可能是一种精神创伤型的经验。"},
            {"dream": "梦到自己处于一种熟悉的环境",
             "decode": "可是偏偏短缺某一心爱之物或熟人，意味着某种不稳定或者反复无常的情绪。"},
            {"dream": "梦见强盗抢劫", "decode": "预示你将遇到波折，但很快局面会开始好转。"},
            {"dream": "梦见和强盗打斗", "decode": "预示你会结交忠实可靠的新朋友。"},
            {"dream": "梦见自己和强盗交朋友", "decode": "表示你在危难时刻，会得到朋友的同情和帮助。"},
            {"dream": "梦见海盗", "decode": "大海不仅仅有风浪的威胁，更有着最危险的组织海盗的威胁。"},
            {"dream": "梦见强盗抢了自己的东西", "decode": "表示会突然破财。"},
            {"dream": "梦见强盗", "decode": "表明在你心中存在着恐惧心理。"},
            {"dream": "梦见遭到强盗的抢劫", "decode": "表明在你的身边存在着势利小人。"},
            {"dream": "梦见自己成为强盗", "decode": "表明你想发泄一下自己的不满情绪。"},
            {"dream": "梦见土匪", "decode": "代表的是健康与行为。"},
            {"dream": "梦见抢劫", "decode": "意味着收获、开支或朋友。"},
            {"dream": "梦见自己的导师", "decode": "一切都会顺心如意。"},
            {"dream": "梦见新的导师", "decode": "会遭受损失。"},
            {"dream": "梦见与自己的导师交谈", "decode": "不久要与世长辞。"},
            {"dream": "梦见和自己的导师谈话", "decode": "吸收新的合股人，能发大财。"},
            {"dream": "梦见与导师吵架", "decode": "会家破人亡。"},
            {"dream": "梦见和导师交谈", "decode": "会因生活困难，中途辍学。"},
            {"dream": "梦见跟老师打招呼", "decode": "做梦者会得到一位好朋友或很快升职加薪。"},
            {"dream": "梦见女演员是成功的预兆", "decode": "可能是做梦人心中希望在公众面前展示的形象。"},
            {"dream": "梦见一个穷困中的女演员",
             "decode": "预示着你将欣然用自己的方法和影响帮助朋友从债务和不幸中解脱出来。"},
        ]

        df = pd.DataFrame(data)  # 创建DataFrame对象

        for item in df.itertuples():
            item_dict = {'dream': item.dream, 'decode': item.decode}
            if match_search_query(item_dict, search_query):
                items.append(item_dict)

        categories = ["人物", "动物", "植物", "物品", "活动", "情感", "生活", "鬼神", "自然", "建筑", "其他"]

        context = {'items': items, 'categories': categories, 'data_items': df.iterrows()}

        return render(request, 'index.html', context)
    elif category == "动物":
        data = [
            {"dream": "梦见夜莺", "decode": "还表示你将与亲人团聚，或夫妻重逢。"},
            {"dream": "梦见不唱歌的夜莺", "decode": "表示朋友之间将有误会。"},
            {"dream": "梦见白鹤飞向北方", "decode": "意味着在商业上会不景气;对于女性而言，表示不如意。"},
            {"dream": "梦见白鹤往南飞", "decode": "则预示很久不见的朋友会重逢，你的异性朋友也会忠贞不贰。"},
            {"dream": "梦见白鹤从空中降落", "decode": "预示不寻常的事情就要发生在你眼前。"},
            {"dream": "梦见白鹤", "decode": "则意味着虽然获利较慢，但生意做得长远，并且受到大家的敬重。"},
            {"dream": "梦见只有一只白鹤", "decode": "暗示你内心是孤单寂寞的。"},
            {"dream": "梦见活的鹤鹑", "decode": "是非常吉利的预兆。"},
            {"dream": "梦见死的鹤鹑", "decode": "预示你的运气很不好，将有不好的事情要降临到自己上。"},
            {"dream": "梦见吃鹤鹑", "decode": "预示你生活奢侈。"},
            {"dream": "梦见鹤鹑", "decode": "意味着你会经常，并且交流的氛围很好。"},
            {"dream": "梦见鹤鹑歌唱", "decode": "暗示你可能会发财。"},
            {"dream": "梦见鹤鹑一声不叫", "decode": "暗示你即使目前生意会萧条，事业进展慢，但最终只要坚持下来，肯定取得成功。"},
            {"dream": "梦见鹤鹑若是丈夫或自己出差在外", "decode": "则意味着不久将要与丈夫相会，也体现的是一种思念之情。"},
            {"dream": "梦见鹤鹑从树上飞走", "decode": "暗示你有时候往往机会只有一次，如果不能及时把握住，那再想抓住，恐怕已经来不及了。"},
            {"dream": "梦见丹顶鹤鸣叫", "decode": "预示梦者将会得到升迁。"},
            {"dream": "梦见丹顶鹤上天", "decode": "预示将会面临灾难，有可能家里有亲人要驾鹤仙游。"},
            {"dream": "梦见丹顶鹤", "decode": "会为死去的丈夫守节一辈子，会被树立贞节牌坊。"},
            {"dream": "梦见只有一只丹顶鹤", "decode": "预示会和亲爱的人分离。"},
            {"dream": "梦见丹顶鹤入怀中", "decode": "会怀孕，并生一个男孩。"},
            {"dream": "梦见鹤", "decode": "是好事，象征健康长寿或取得功名;也表示眼前的烦恼即将结束，因祸得福，化险为夷。"},
            {"dream": "梦见鹤群", "decode": "预示你吉祥如意，事事顺心。"},
            {"dream": "梦见形单影只的鹤", "decode": "则不吉利，预示做梦人有可能会失去配偶。"},
            {"dream": "梦见仙鹤飞进自己怀里", "decode": "预示会喜得贵子。"},
            {"dream": "梦见仙鹤", "decode": "预示将通过稳扎稳打，逐渐积累，获得丰厚的利润。"},
            {"dream": "梦见白鹤在空中飞翔", "decode": "表示你财运好转，也许还会收到亲人或长辈的赠送。"},
            {"dream": "梦见自己坐在鹤身上飞翔", "decode": "预示你将获得意外的的晋升。"},
            {"dream": "梦见鹤飞走", "decode": "远去消失，预示可能会有儿女意外去世。"},
            {"dream": "梦见仙鹤飞入怀中", "decode": "暗示着你将喜得贵子。"},
            {"dream": "梦见鹤驾车", "decode": "这暗指现实中的你正处于一场纠纷中，你想通过武力来解决事情。"},
            {"dream": "梦见放飞仙鹤", "decode": "预示着会有财运来临，这是大吉大利的好梦。"},
            {"dream": "梦见鹦鹉死了", "decode": "要提防小人，以防上当受骗。"},
            {"dream": "梦见死去的鹦鹉", "decode": "那你就要提防自己交上心眼不好的朋友了，恐怕自己会受他欺骗上当。"},
            {"dream": "梦见用枪打鹦鹉", "decode": "预示你可以降服你的竞争对手，赢取最后的胜利。"},
            {"dream": "梦见抓了好多鹦鹉掐死了", "decode": "意味着自己一副悠闲的样子，却没观察到已经影响到别人的地方。"},
            {"dream": "梦见养鹦鹉", "decode": "事实证明朋友靠招遥撞骗为生，提醒梦者交友要慎重。"},
            {"dream": "梦见成群的鹦鹉", "decode": "提醒你当心，可能财产会遇到严重威胁，提醒你投资要谨慎。"},
            {"dream": "梦见鹦鹉在飞", "decode": "好事，预示你现在的烦恼或忧愁将成为过去，有人会令你展颜启齿。"},
            {"dream": "梦见会说话的鹦鹉", "decode": "代表梦者的内心很寂寞，缺少与人的沟通。"},
            {"dream": "梦见关在笼子里的鹦鹉", "decode": "预示梦者会困难重重。"},
            {"dream": "梦见用打鹦鹉", "decode": "预示梦者能降服对。"},
            {"dream": "梦见买鹦鹉", "decode": "预示你要承担无端的经济压力，可能家人或父辈欠的债需要你来偿还。"},
        ]

        df = pd.DataFrame(data)  # 创建DataFrame对象

        for item in df.itertuples():
            item_dict = {'dream': item.dream, 'decode': item.decode}
            if match_search_query(item_dict, search_query):
                items.append(item_dict)

        categories = ["人物", "动物", "植物", "物品", "活动", "情感", "生活", "鬼神", "自然", "建筑", "其他"]

        context = {'items': items, 'categories': categories, 'data_items': df.iterrows()}
        return render(request, 'index.html', context)
    elif category == "植物":
        data = [
            {"dream": "梦见喝柠檬汁", "decode": "表示你深受欢迎，人际关系良好。"},
            {"dream": "梦见成堆的柠檬", "decode": "是祥兆，意味着能找到如意的对象。"},
            {"dream": "梦见咬柠檬","decode": "预示钱财方面可能会同时有大进项和支出，如你先有巨大收入，不要高兴过早，可能很快会有意料外的支出。"},
            {"dream": "梦见吃生柠檬", "decode": "提醒你要注意身体健康，这是生病的预兆，你体内可能有些阴阳不调。"},
            {"dream": "梦到干缩的柠檬", "decode": "意味着离婚与分别。"},
            {"dream": "梦到正在吃柠檬", "decode": "暗示会有使你生气的事情发生。"},
            {"dream": "梦到绿色的柠檬", "decode": "是疾病和传染病的象征，你要留意自己的健康状况。"},
            {"dream": "梦见柠檬树上结了许多柠檬","decode": "意味着你忌妒某个受大家欢迎的人，但因对方光明磊落，使你感到惭愧。"},
            {"dream": "梦见成熟的荔枝果实累累", "decode": "表示婚姻美满，家庭和谐。"},
            {"dream": "梦见荔枝", "decode": "预示婚后生活不快乐，可能会顺从父母意愿嫁给一个无能的丈夫。"},
            {"dream": "梦见吃新鲜荔枝", "decode": "预示财源广进，机会增多。"},
            {"dream": "梦见吃荔枝","decode": "预示着近期你有流产等重大危险，建议你要注意安全健康，特别要暗示去医院做检查。"},
            {"dream": "梦见偷荔枝", "decode": "预示梦者近段时间经常怀念过去，容易感伤。"},
            {"dream": "梦见摘荔枝", "decode": "预示着你近期会生一个活泼健康的儿子，是吉兆。"},
            {"dream": "梦见吃烂荔枝", "decode": "暗示梦者近期精力充沛，做事(梦见荔枝)非常有动力。"},
            {"dream": "梦见草莓", "decode": "如果你还没结婚，可能表示你现在的恋人并不很喜欢你，会移情别恋，爱上另一个女人;如果你已经结婚，预示丈夫也许要出轨，有情妇。"},
            {"dream": "梦见买草莓", "decode": "预示你家里可能有人要结婚，办喜事。"},
            {"dream": "梦见卖草莓", "decode": "预示梦者可能将有一段艰苦的日子到来。"},
            {"dream": "梦见和恋人一起吃草莓", "decode": "预示感情美满，爱情终会开花结果。"},
            {"dream": "梦见吃腐烂的草莓", "decode": "凶兆，预示梦者会面临厄运(梦见草莓)或生病，要注意身体健康。"},
            {"dream": "梦见送别人草莓", "decode": "表示梦者将结识新的朋友。"},
            {"dream": "梦见吃草莓", "decode": "预示生个漂亮的女儿且生活会幸福美满。"},
            {"dream": "梦见红润饱满的橘子", "decode": "预示你会交好运，走红运。"},
            {"dream": "梦见熟透了的橘子", "decode": "暗示着要交好运，会有意外的惊喜。"},
            {"dream": "梦见熟橘子", "decode": "预示会有很好的名声。"},
            {"dream": "梦见生橘子", "decode": "代表了做梦的人身体有不舒服的地方需要多注意了。"},
            {"dream": "梦见买橘子", "decode": "意味着妻子去世后，很快能娶到年轻貌美的姑娘。"},
            {"dream": "梦见送别人橘子", "decode": "预示你会受到别人的喜爱和赞扬。"},
            {"dream": "梦见剥橘子皮或挤橘子汁", "decode": "预示会有大生意，利润丰厚。"},
            {"dream": "梦见多棵繁茂的橘子树挂满成熟的橘子", "decode": "预示健康和成功的情形。"},
            {"dream": "梦见吃橘子","decode": "是不吉利的梦，你主要是因朋友或亲戚的疾病而烦恼，事业上相互不满的气氛也将蔓延。"},
            {"dream": "梦见成色很好的橘子挂在高高的枝头", "decode": "预示她将谨慎地在众多追求者中选择一个做丈夫。"},
            {"dream": "梦见踩上橘子皮滑倒", "decode": "预示亲戚的死亡。"},
            {"dream": "梦见妻子要你买橘子", "decode": "然后把橘子吃了，预示讨厌的复杂因素将转化为有利条件。"},
            {"dream": "梦见有人在破坏橘子果园", "decode": "意味着有好几个仇人，他们会从多方面对自己不利。"},
            {"dream": "梦见成熟的西瓜", "decode": "吉利如意，预示发财。"},
            {"dream": "梦见没熟的西瓜", "decode": "是凶险的征兆，你可能会遇到不好的事。"},
            {"dream": "梦见长在藤上的西瓜", "decode": "还提醒你交友要谨慎，以免日后带来麻烦。"},
            {"dream": "梦见吃西瓜", "decode": "预示着自己和孩子身体都很健康，是祥兆。"},
            {"dream": "梦见有人抢自己的西瓜", "decode": "预示会有官司之争，打输的可能性很大，会令你损失巨大。"},
            {"dream": "梦见庄稼被毁", "decode": "这是不祥之兆，预示着成功得而复失。"},
        ]

        df = pd.DataFrame(data)  # 创建DataFrame对象

        for item in df.itertuples():
            item_dict = {'dream': item.dream, 'decode': item.decode}
            if match_search_query(item_dict, search_query):
                items.append(item_dict)

        categories = ["人物", "动物", "植物", "物品", "活动", "情感", "生活", "鬼神", "自然", "建筑", "其他"]

        context = {'items': items, 'categories': categories, 'data_items': df.iterrows()}
        return render(request, 'index.html', context)
    elif category == "物品":
        data = [
            {"dream": "梦见滑轮", "decode": "公司的活动可以为你带来表现的机会，无论获得的奖品如何，关键的是你有机会展现自己的机智和口才。"},
        {"dream": "梦见脚踩滑轮","decode": "大概会有许多人会注意着你的一举一动，你的每件事情，他们都看在眼里，希望你能够与他们主动的联系沟通，也许他们还有帮忙的意思。"},
        {"dream": "梦见滑滑轮旱冰", "decode": "预示着自己将会有意外之财，但是后续财运会变差。"},
        {"dream": "梦见脚踩滑轮车前行", "decode": "最近做事会发生连锁反应。"},
        {"dream": "梦见道路被堵","decode": "预示着近期你的运势不好，自己心情不好的时候，就会胡乱的花钱购物，建议需要学会节制。"},
        {"dream": "梦见路上堵车","decode": "预示着自己最近的运势一般，虽然看起来一副悠闲的的样子，却没有注意到自己已经影响到别人，需要调整好自己，避免给他人人带来困扰和焦虑。"},
        {"dream": "梦见奔波途中遇到交通堵塞", "decode": "预示奋斗过程中将遭遇挫折，或是生活令你感到压抑。"},
        {"dream": "梦见自己被奢侈品包围","decode": "暗示巨大的财富，但是你的自负和挥霍无度将使自己所得逐渐变少。"},
        {"dream": "梦见享用奢侈品", "decode": "表示她的处境不久就会改变。"},
        {"dream": "梦见你的生活很奢侈", "decode": "房子是王宫般的装饰，吃的是山珍诲味，而你又整天和许多美女在一起，这个梦境意味着你很富有，但是花在女人身上的钱，将是一笔可观的数目。"},
        {"dream": "梦见她过着从未有过的奢侈生活", "decode": "这是代表她的生活状况已经有好转的迹象。"},
        {"dream": "梦见自己正在系领带", "decode": "系来系去并弄不好，表示你在人际关系总是处理不好，最好是找个朋友帮你分析一下该怎么做，一定很有帮助。"},
        {"dream": "梦见自己系着漂亮的领带", "decode": "表明你的社交能力很强。"},
        {"dream": "梦见领带", "decode": "预示着你会遇到一位风度翩翩的男士。"},
        {"dream": "梦见自己的领带歪歪的", "decode": "表示你可能会在社交场合出丑，或是碰到让你尴尬的场面。"},
        {"dream": "梦见别人打领带", "decode": "主求职;求职运势不错，机会较多，需要调整自己、灵活处理的时候较多，对原则的坚持和机会的诱惑形成矛盾。"},
        {"dream": "梦见裙子好漂亮", "decode": "预示着感情一般，彼此会因为金钱利益发生冲突，也会因为一些小矛盾发生争吵，如果彼此都不能放宽心态的对待，这对感情继续的开展很不利。"},
        {"dream": "梦见漂亮的小花裙子","decode": "预示着近期的玩心比较重，对新奇的事物有着很强的追求感，也会有机会到国外去走走，心情也会很好。"},
        {"dream": "梦见好多穿着漂亮裙子的小姑娘", "decode": "预示着最近有想要拓展人生经验的想法，不如大胆的去尝试，也可以多补充自己的专业知识，这对你在职场的表现很有帮助，是祥兆。"},
        {"dream": "梦见找到了被藏匿的宝藏", "decode": "意味着将会在打官司上破费很多。"},
        {"dream": "梦见奶粉", "decode": "会做出不切实际的行为!今天的你有这样的冲动，而且往往一旦付诸实现，会让自己的状况变得糟糕。"},
        {"dream": "梦见买奶粉", "decode": "工作上出现新的机会!选择跳槽或者创业，对你来说都是不错的时机。"},
        {"dream": "梦见买婴儿奶粉", "decode": "有些懒散的一天!想轻松自由地一个人逛逛。"},
        {"dream": "梦见喝奶粉", "decode": "意味着用本心去待人就可以得到很好的效果。"},
        {"dream": "梦见正在做棉袄和棉袍", "decode": "暗示她的住宅虽然寒酸，但是住起来很方便。"},
        {"dream": "梦到正在做棉袄棉袍", "decode": "暗示她有一个性喜冒险的丈夫。"},
        {"dream": "梦见棉袄", "decode": "意味着会发财，棉花蓬蓬松松，财富像雪球一样越滚越大。"},
        {"dream": "梦见棉袄一般来说是好的寓意", "decode": "棉花蓬蓬松松，象征着发财，财富像雪球一样越滚越大。"},
        {"dream": "梦见棉袍", "decode": "意味着环境使自己觉得轻松自在，生活没有什么波折。"},
        {"dream": "梦到小孩的棉衣","decode": "预示这段时间自己的运气，顺乎自然，真诚待人处事，千万不可沉醉於个人利益与满足本身欲望，否则有灾难发生。"},
        {"dream": "梦见正在做棉袍", "decode": "意味着她的住宅虽然寒酸，但是住起来很方便。"},
        {"dream": "梦见穿棉袄", "decode": "预示着你该加强自身的学习了，要不然随着年龄的增长，记忆力将会衰退。"},
        ]

        df = pd.DataFrame(data)  # 创建DataFrame对象

        for item in df.itertuples():
            item_dict = {'dream': item.dream, 'decode': item.decode}
            if match_search_query(item_dict, search_query):
                items.append(item_dict)

        categories = ["人物", "动物", "植物", "物品", "活动", "情感", "生活", "鬼神", "自然", "建筑", "其他"]

        context = {'items': items, 'categories': categories, 'data_items': df.iterrows()}
        return render(request, 'index.html', context)
    elif category == "活动":
        data = [
            {"dream": "梦见在清水中走路", "decode": "看见清泉流水的水源，都是不同的喜讯，解释为两世美好，生活的美满。"},
            {"dream": "梦见清水喷泉", "decode": "爱情会一帆风顺，非常幸福快乐。"},
            {"dream": "梦见喝清水甘泉", "decode": "不管清晰与否都解释为生命的寿限和平静的生活。"},
            {"dream": "梦见从井里打上清水", "decode": "则当事人会平安归来。"},
            {"dream": "梦见像碗的盘子", "decode": "具有妇性意味，有性和生育的含义。"},
            {"dream": "梦见自己或别在贴墙纸", "decode": "预示做梦人的身份、社会地位、生活环境将发生变化。"},
            {"dream": "梦见在贴白色墙纸", "decode": "表明做梦人的工作顺利，环境顺心。"},
            {"dream": "梦见在贴绿色墙纸", "decode": "预示做梦人工作上会取得出色的成绩。"},
            {"dream": "梦见在贴花墙纸", "decode": "暗示做梦人的生活快快乐乐，充满乐趣，花样繁多。"},
            {"dream": "梦见墙纸破了", "decode": "则暗示你目前工作上可能会出现漏洞，需要想方设法弥补，或是换一个新的方式。"},
            {"dream": "梦见破鞋", "decode": "也有破邪之意，预示着困难会过去。"},
            {"dream": "梦见丢鞋", "decode": "从周公解梦来说，是不祥之兆，会大难临头。"},
            {"dream": "梦见我一进家门", "decode": "老公就叫我进盥洗间看看，原来他把盥洗间装上了彩色陶瓷，非常漂亮。"},
            {"dream": "梦见吸尘器", "decode": "通常预示你会通过自己的努力，在感情生活里赢得满意的局面。"},
            {"dream": "梦见自己在使用吸尘器", "decode": "暗示你不但想清除掉旧思想，摒弃旧习惯，甚至还想彻底清除过去生活里的一切痕迹，重新开始新生活。"},
            {"dream": "梦见别人在使用吸尘器", "decode": "提醒你自己要加倍努力，才可能得到心上人的重视。"},
            {"dream": "梦见使用吸尘器时坏了", "decode": "或吸尘器出了故障，则暗示你对待感情要谨慎，提醒你不要四处留情，随便与他人发展关系;或为了生意，升职等目的而刻意和异性交往。"},
            {"dream": "梦见在衣服上洒香水的情景", "decode": "预示家庭开支会大增。"},
            {"dream": "梦见给别人的衣服上洒香水", "decode": "预示你会得到提拔。"},
            {"dream": "梦见给恋人的衣服洒香水", "decode": "预示你将赢得对方的芳心，爱情出现大幅进展。"},
            {"dream": "梦见往丈夫的衣服上洒香水", "decode": "预示会喜得贵子，生一个漂亮的男孩，家庭更加和睦。"},
            {"dream": "梦见去买香水", "decode": "表示你深受欢迎，很多人喜欢你。"},
            {"dream": "梦见去香水店里买香水", "decode": "周围是琳琅满目的香水瓶，暗示你要和领导，权威‘上层人物建立起友谊。"},
            {"dream": "梦见自己开香水店卖香水", "decode": "预示人际关系会给你带来财运，而且不仅自己发财，还会让亲友从中获益。"},
            {"dream": "梦见一般的香味", "decode": "代表的是生活的幸福如意。"},
            {"dream": "梦见扑鼻的异香", "decode": "是在提醒你不要被心术不正的女人所利用。"},
            {"dream": "梦见酸味", "decode": "是健康的象征。"},
            {"dream": "梦见甜味", "decode": "预示会获得甜蜜的爱情，或是将要结婚。"},
            {"dream": "梦见苦味", "decode": "代表的是烦恼的增多。"},
            {"dream": "梦见辣味", "decode": "是在提醒你处事要沉着冷静。"},
            {"dream": "梦见酸甜苦辣", "decode": "意味着在你的心中存有一段感情，这份感情有苦也有甜。"},
            {"dream": "梦见自己坐在断裂的椅子上", "decode": "或是坏椅子上，则预示会遇到挫折打击，令你名声受损。"},
            {"dream": "梦见舒适的椅子", "decode": "通常表示生活舒适安逸。"},
            {"dream": "梦见浴缸", "decode": "一方面，暗示生活能力强，善于处理家务。"},
            {"dream": "梦见在澡盆或浴房里洗澡", "decode": "预示可能有坏运气，遭遇挫折。"},
            {"dream": "梦见在浴盆或浴房里洗澡、淋浴", "decode": "暗示近期可能要怀孕。"},
            {"dream": "梦见浴缸很脏或梦里感到水很冷", "decode": "则暗示你可能和别人有奸情。"},
            {"dream": "梦见放满水的浴盆", "decode": "表示美满幸福的家庭生活将使你感到格外的满足。"},
            {"dream": "梦见空的浴缸", "decode": "象征着你的生活充满不快，你所拥有的财富也将衰减。"},
            {"dream": "梦见毁坏的浴盆", "decode": "预示你的家庭将会出现不和谐因素并伴随有争吵现象。"},
            {"dream": "梦见煤块", "decode": "吉兆，会有好运。"},
            {"dream": "梦见熊熊燃烧的煤炭", "decode": "预示着自己的努力会得到成功。"},
            {"dream": "梦见自己在辛苦地铲煤", "decode": "意味着成功的路上需要努力。"},
            {"dream": "梦见自己在拉煤或送煤", "decode": "预示着自己马上可能成功。"},
            {"dream": "梦见自己敲钟", "decode": "表示意味着职务上的升迁。"},
            {"dream": "梦见表", "decode": "分娩会极不顺利。"},
            {"dream": "梦见戴手表", "decode": "会与丈夫家的女性发生口角。"},
            {"dream": "梦见表停了", "decode": "敌人会向自己屈服。"},
            {"dream": "梦到闹钟响", "decode": "警告你有危险。"},
            {"dream": "梦见蜂窝煤", "decode": "吉兆，预示着会有好运气。"},
            {"dream": "梦见你正在用热水瓶倒开水", "decode": "表示你们家庭之中，可能会常常为了一些小小事，而爆发争吵与呕气。"},
        ]

        df = pd.DataFrame(data)  # 创建DataFrame对象

        for item in df.itertuples():
            item_dict = {'dream': item.dream, 'decode': item.decode}
            if match_search_query(item_dict, search_query):
                items.append(item_dict)

        categories = ["人物", "动物", "植物", "物品", "活动", "情感", "生活", "鬼神", "自然", "建筑", "其他"]

        context = {'items': items, 'categories': categories, 'data_items': df.iterrows()}
        return render(request, 'index.html', context)
    elif category == "情感":
        data = [
            {"dream": "梦见和男(女)朋友领结婚证", "decode": "代表着好事将近。"},
        {"dream": "梦见别人领结婚证", "decode": "意味着你对幸福生活的向往。"},
        {"dream": "梦见和情人领结婚证", "decode": "预示你们不久就要结婚了。"},
        {"dream": "梦到示爱", "decode": "意味着梦者的人际关系在近期会发生很大的改变。"},
        {"dream": "梦见向陌生的异性示爱",
         "decode": "这个梦与你成为别人感情的第三者无关，只是表示现在的你，正处于性欲旺盛的阶段，但要小心别被花言巧语给骗了。"},
        {"dream": "梦见向恋人示爱",
         "decode": "表示两人的关系发展得非常亲密，已经到了可以向对方表明想要结婚的愿望了，是时候该直接告诉对方你想结婚的意愿。"},
        {"dream": "梦见有人向自己示爱",
         "decode": "表示你内心中一直渴望可以好好的谈一场恋爱，不过有太多的事情耽误了。"},
        {"dream": "梦见自己的朋友对别人示爱",
         "decode": "表示你内心中一直渴望可以好好的谈一场恋爱，生活幸福美满。"},
        {"dream": "梦见对别人示爱", "decode": "暗示你在现实生活中对自己没有信心，认为自己完成不了某个事情。"},
        {"dream": "梦见向同性恋友人示爱",
         "decode": "先不用担心自己会变同性恋，这个梦只是在暗示你，提醒你过于忙着工作的事情，忽略了自己身边的朋友，相互之间的感表变淡了。"},
        {"dream": "梦见与同性或异性好朋友示爱", "decode": "在梦中出现的同性或异性友人，就是你的分身。"},
        {"dream": "梦见他和异性交谈得很快乐的话",
         "decode": "表示你心里一直渴望能好好谈场恋爱，只是被你的意识压抑掉了。"},
        {"dream": "梦见情人向你示爱", "decode": "情敌出现的可能性极大。"},
        {"dream": "梦见两个女人同时对自己示爱",
         "decode": "预示着爱情方面会有幸运的事情，也会受到情意绵绵的轻松，是祥兆。"},
        {"dream": "梦见了自己正在向恋人示爱求婚",
         "decode": "意味着在生意的过程中所遭遇到的各种阻碍都将被解决，而解决的原因很大程度上归结于做梦者的生活中将会出现一个会对自己有所帮助的朋友。"},
        {"dream": "梦见动物示爱",
         "decode": "暗示你对自己所拥有的很知足，尽管你可能并不这么认为;有段时间，你会非常幸运。"},
        {"dream": "梦见男人赤身裸体", "decode": "除了暴露欲，有可能表达异性恋或同性恋欲望。"},
        {"dream": "梦见偶然看见男人赤身裸体",
         "decode": "预示着你在钱财上会受窘，可能会有一段资金不充足的日子，令你的社交生活有些尴尬。"},
        {"dream": "梦见男人在清水中赤身裸体",
         "decode": "预示着梦里的男人在现实生活中将会有很多人爱慕他，他的内心也会很骄傲、自豪。"},
        {"dream": "梦见男人在浑浊的水中赤身裸体",
         "decode": "预示着仰慕者将会因为嫉妒而恶意造谣，会令自己很难堪。"},
        {"dream": "梦见男人赤身裸体并疾走", "decode": "预示着你内心很渴望能痛苦的发泄压抑已久的感情。"},
        {"dream": "梦见男人赤身裸体并感到很舒服",
         "decode": "预示着你很希望去掉各种遮掩，要把自己真是的一面，坦诚的展现在众人面前。"},
        {"dream": "梦见熟悉的男人赤身裸体",
         "decode": "内心很反感，预示着你在现实生活中对这个人的真实动机感到很愤怒。"},
        {"dream": "梦见男人在公共场所赤身裸体",
         "decode": "并举止自信愉快，预示着你很希望和他人坦诚相见，在某些事情上担心自己被人误解。"},
        {"dream": "梦见男子一丝不挂", "decode": "表示能命运通达。"},
        {"dream": "梦见男人穿裙子",
         "decode": "预示着求职运势不错，不过自己需要抓住机会好好的施展自己的才能，要尽可能的迎合招聘方的要求，找到适合自己的职位。"},
        {"dream": "梦见男人穿红裙子",
         "decode": "预示着运势还算不错，也要计划的事情也会进展的很顺利，生活也会很幸福。"},
        ]

        df = pd.DataFrame(data)  # 创建DataFrame对象

        for item in df.itertuples():
            item_dict = {'dream': item.dream, 'decode': item.decode}
            if match_search_query(item_dict, search_query):
                items.append(item_dict)

        categories = ["人物", "动物", "植物", "物品", "活动", "情感", "生活", "鬼神", "自然", "建筑", "其他"]

        context = {'items': items, 'categories': categories, 'data_items': df.iterrows()}
        return render(request, 'index.html', context)
    elif category == "生活":
        data = [
            {"dream": "梦见爬上楼梯望天空", "decode": "暗示财运大展，会从始料未及的地方来一笔意外的收人。"},
        {"dream": "梦见在学校楼梯上上下下", "decode": "表示暗示成绩忽上忽下，很不稳定。"},
        {"dream": "梦见赤脚渡浅水河在个性上会有很大的变化", "decode": "将会有无比的耐性。"},
        {"dream": "梦见赤脚过河",
         "decode": "说明你是一个能吃苦的人，你所面对的困难最终会败在你的耐性之下，成功就在不远方。"},
        {"dream": "梦见泥泞",
         "decode": "非常难走或者艰难前行，通常这种梦暗示了你对目前工作的无信任感，或者说不满。"},
        {"dream": "梦见在泥泞中行走",
         "decode": "还反映出现在或者接下来的生活中会出现大大小小的烦恼，也就是代表你梦中泥泞的路。"},
        {"dream": "梦见在山上迷路", "decode": "则预示你会得到长辈的提点，得到提拔。"},
        {"dream": "梦见在森林里迷路", "decode": "要小心，不要上了仇人的当，陷入困境。"},
        {"dream": "梦见迷路了",
         "decode": "或是明明在往前走，但却无法前进，这表示最近的你已经迷失了自我，不知道自己在干嘛了，应该要冷静下来好好思考才行。"},
        {"dream": "梦见迷路", "decode": "从心理方面讲，象征人生孤独辛苦，不断追寻，不断失落，多曲折。"},
        {"dream": "梦见在街上迷路", "decode": "愿望不能得以实现。"},
        {"dream": "梦见听钢琴音乐", "decode": "会与丈夫过上幸福的生活。"},
        {"dream": "梦见听钢琴乐", "decode": "不久会与恋人各奔前程。"},
        {"dream": "梦见弹钢琴", "decode": "会与别的女人发生口角。"},
        {"dream": "梦见玩骨牌游戏", "decode": "并且输了，表示有人会冒犯你，你的亲人因此会担心你的安全。"},
        {"dream": "梦见骨牌游戏中你赢了",
         "decode": "意味着你的性格很自私，往往只顾满足自己而不顾给亲人带来愁苦。"},
        {"dream": "梦到玩游戏",
         "decode": "说明你已经意识到你的生意只有靠更多的人脉，才能得到稳固的发展，这会让你认识更多的朋友。"},
        {"dream": "梦见和陌生人玩游戏", "decode": "暗示你会做一些很不值得的事情，只会让你的金钱遭受损失。"},
        {"dream": "梦见和小孩子玩游戏",
         "decode": "预示着你在不经意间做出的某件事情，让你受益非浅，这是在提醒你平时要多注意细节的方面。"},
        {"dream": "梦见和别人玩游戏",
         "decode": "暗示你所做的事情不仅不会给你带来好处，反而会浪费你的精力与钱财，同时也让你颜面扫地。"},
        {"dream": "梦见喜剧", "decode": "是愉快的生活和低俗享受的象征。"},
        {"dream": "梦见自己是喜剧中的一个角色", "decode": "表示你将沉湎于愚蠢和短暂的享乐之中。"},
        {"dream": "梦见自己观看喜剧", "decode": "预示轻松愉快的任务。"},
        {"dream": "梦见你正在观赏滑稽表演",
         "decode": "表示做梦者会沉迷于低俗的享受中，而所得的快乐不但时间短暂，而且显得愚昧。"},
        {"dream": "梦见完成了某项任务或一批工作",
         "decode": "表示在你生命的早期会学到一技之长，以后你可以随心所欲的打发日子。"},
        {"dream": "梦见她做成一件衣服", "decode": "表示她将很快地有一个丈夫。"},
        {"dream": "梦见完成一次旅行", "decode": "表示只要你喜欢，什么时候都能去旅行。"},
        {"dream": "梦见自己干活", "decode": "则意味着会生女孩;。"},
        {"dream": "梦见自己干不熟悉的体力活", "decode": "身体会很快复原。"},
        {"dream": "梦见有人要与你决斗", "decode": "表示你会在社交界陷入进退维谷的困境，并将失去某些人的友谊。"},
        ]

        df = pd.DataFrame(data)  # 创建DataFrame对象

        for item in df.itertuples():
            item_dict = {'dream': item.dream, 'decode': item.decode}
            if match_search_query(item_dict, search_query):
                items.append(item_dict)

        categories = ["人物", "动物", "植物", "物品", "活动", "情感", "生活", "鬼神", "自然", "建筑", "其他"]

        context = {'items': items, 'categories': categories, 'data_items': df.iterrows()}
        return render(request, 'index.html', context)
    elif category == "鬼神":
        data = [
            {"dream": "梦见妖精压在您身上", "decode": "烦心事将可解除，是开运的吉梦。"},
        {"dream": "梦到自己成为神仙去抓狐狸精", "decode": "预示着你的恋情有变数。"},
        {"dream": "梦见女鬼",
         "decode": "反映你自己感情上，受到伤害的过去，或者是代表你朋友，感情上受到伤害，对你产生的影响。"},
        {"dream": "梦见自己向女鬼进攻", "decode": "自己可以避免一场灾祸。"},
        {"dream": "梦见自己见到女鬼而逃跑", "decode": "预示着克服工作上的困难，或者打败竞争对手。"},
        {"dream": "梦见天空中有女鬼在飘",
         "decode": "表示你在科学方面有研究成果，但在生活上却有隐忧，有可能会有灾难降临。"},
        {"dream": "梦见红衣女鬼", "decode": "代表梦者内心对某些事物的恐惧和阴影。"},
        {"dream": "梦见白衣女鬼", "decode": "代表梦者孤独而缺乏生命力。"},
        {"dream": "梦见水怪在游泳", "decode": "爱情将停滞不前。"},
        {"dream": "梦见龙飞往地面", "decode": "临时收入将增加。"},
        {"dream": "梦见龙在天上飞行", "decode": "表示成绩方面运气上升。"},
        {"dream": "梦见遭受怪兽袭击", "decode": "健康方面运势将下降。"},
        {"dream": "梦见遭怪兽袭击",
         "decode": "预示你可能会患玻做这个梦提醒你近期要多注意身体健康，尤其要注意预防食物中毒、痢疾、肠胃炎等消化系统的疾病，并保持良好的饮食习惯，少吃零食等。"},
        {"dream": "梦见有水怪在水里游泳、翻滚",
         "decode": "预示你的爱情可能会遇到挫折，你跟恋人之间也许会产生误会，让你感觉受了冷落。"},
        {"dream": "梦见怪兽之间互相残杀",
         "decode": "预示在感情方面时来运转，好事连连，但在约会中，最好能多听从女方的主意，这样才能发展顺利。"},
        {"dream": "梦见鬼怪是凶兆", "decode": "梦见抓鬼是吉兆。"},
        {"dream": "梦见抓鬼、向鬼怪进攻", "decode": "吉兆，可以避免灾祸。"},
        {"dream": "梦见被恶魔追逐", "decode": "你将陷人伪装成朋友的敌人预先设好的陷阱之中。"},
        {"dream": "梦见自己性欲高涨", "decode": "暗示除非将来丈夫稳重并对自己忠诚，否则她会以出轨来寻求平衡。"},
        {"dream": "梦见鬼屋", "decode": "在现实中如果有不好的感觉，心里觉得不对，就不要进去似曾相识的房子里。"},
        {"dream": "梦见被妖怪追逐", "decode": "表示在不久的将来，悲伤和不幸将充斥你的生活。"},
        {"dream": "梦见杀死妖怪", "decode": "表示你将成功地战胜敌人，并荣升到显赫的社会地位。"},
        {"dream": "梦见自己受妖怪攻击", "decode": "将发生危及性命的事情。"},
        {"dream": "梦见被妖怪杀害", "decode": "是凶兆;梦见怪物跑到家中，是凶兆。"},
        {"dream": "梦见自己战胜了魔鬼", "decode": "你将战胜竞争对手，脱颖而出，最终功成名就。"},
        {"dream": "梦见鬼火飞翔", "decode": "会收到他人的惊吓。"},
        {"dream": "梦见已逝父亲或者母亲的鬼魂",
         "decode": "表示你将面临危险，在和陌生人打交道时要格外小心谨慎。"},
        {"dream": "梦见已故朋友的鬼魂", "decode": "预示你将和一个讨厌的同伴一起，开始一次漫长的旅行。"},
        {"dream": "梦见天使或幽灵现身空中", "decode": "表示亲人的离去等不幸。"},
        ]

        df = pd.DataFrame(data)  # 创建DataFrame对象

        for item in df.itertuples():
            item_dict = {'dream': item.dream, 'decode': item.decode}
            if match_search_query(item_dict, search_query):
                items.append(item_dict)

        categories = ["人物", "动物", "植物", "物品", "活动", "情感", "生活", "鬼神", "自然", "建筑", "其他"]

        context = {'items': items, 'categories': categories, 'data_items': df.iterrows()}
        return render(request, 'index.html', context)
    elif category == "自然":
        data = [
            {"dream": "梦见雪", "decode": "可能象征性地提醒你要对周围的人，更加热情。"},
        {"dream": "梦见自购树上落满了雪花",
         "decode": "预示可能有人会为你投资，或者你投资的项目将获得很好的回报。"},
        {"dream": "梦见星光映照在水面是您目前正在祈愿的事将要破碎的凶梦", "decode": "特别是恋爱，不会成功。"},
        {"dream": "梦见星光灿烂", "decode": "希望本身变得开朗有活力，将来路上多姿多彩一路顺风。"},
        {"dream": "梦见月色昏黑星光黯淡",
         "decode": "家里最近将有大变故，病人梦见月色昏黑星光黯淡，病人将陷入危境，是恶梦，或长辈有变故，且举头无亲，勿轻举妄。"},
        {"dream": "梦见星光映照在水面", "decode": "股市现在看起来好像不错，其实是股市低落的前兆。"},
        {"dream": "梦见霜落",
         "decode": "是在暗示你最近不要执行计划，否则只会无功而返，同时也要多注意身体健康，可能出现了一些问题。"},
        {"dream": "梦见山中有墓或冢",
         "decode": "股市暗示低价时暂为最低，高价时暂为极限，如是黑云密布，就停止买卖，会低迷一阵子。"},
        {"dream": "梦见墓上有云飘浮", "decode": "暗示将有喜事。"},
        {"dream": "梦见墓上黑云密布", "decode": "则是一家将有不祥的事发生，是最恶的梦。"},
        {"dream": "梦见山上有坟墓", "decode": "预示着你在不久会名声大噪，是属于好兆头来的。"},
        {"dream": "梦见山上有很多坟墓",
         "decode": "预示着你的考试成绩很不错，需要继续努力，要是想让自己的成绩更好的话，可以请一个“钛合金文殊菩萨吊坠项坠”佩戴身上，保佑学业顺利。"},
        {"dream": "梦见山上的坟墓",
         "decode": "预示你最近将要出远门，虽然路上会有问题出现，但无大碍，提醒你要提前作好计划再去做决定。"},
        {"dream": "梦见山顶积雪",
         "decode": "股市暗示今天的高价是极限，但是梦见仰看或爬登雪山，就表示股价将一路上升。"},
        {"dream": "梦见山顶雪崩", "decode": "则表示纵然有一时的刺激或混乱，但随后事态就会慢慢好转。"},
        {"dream": "梦见雪崩是一切将崩盘", "decode": "勿进场买卖。"},
        {"dream": "梦见土块扔向别人", "decode": "将受到别人的损害。"},
        {"dream": "梦见给人土块", "decode": "表示最近会与别人一起饮食，而是由您付帐。"},
        {"dream": "梦见办公室的几个小姑娘一起在一个小山坡的断壁下商量工作上的事",
         "decode": "山坡上就发下来土块砸我们，预示着不久的将来你会在不经意间处在危险的境况下。"},
        {"dream": "梦见搬运泥土", "decode": "预示你近期到户外会有好运气。"},
        {"dream": "梦见遁入泥土中", "decode": "在金钱方面可能会有意外的收获。"},
        {"dream": "梦见躺在泥土中", "decode": "爱情方面出现停滞。"},
        {"dream": "梦见土块", "decode": "股市暗示出现抛售的现象，是突然跌价的前兆，不动产的股票会下跌。"},
        {"dream": "梦见天色染红",
         "decode": "股市暗示诸股高涨之兆，但如果东边天红则股价将回到原来的水平，西边天红则应该买进。"},
        {"dream": "梦见五色彩云", "decode": "表示运势会持续亨通。"},
        ]

        df = pd.DataFrame(data)  # 创建DataFrame对象

        for item in df.itertuples():
            item_dict = {'dream': item.dream, 'decode': item.decode}
            if match_search_query(item_dict, search_query):
                items.append(item_dict)

        categories = ["人物", "动物", "植物", "物品", "活动", "情感", "生活", "鬼神", "自然", "建筑", "其他"]

        context = {'items': items, 'categories': categories, 'data_items': df.iterrows()}
        return render(request, 'index.html', context)
    elif category == "建筑":
        data = [
            {"dream": "梦见仰望高楼", "decode": "暗示了对男性阳刚气质的憧憬。"},
        {"dream": "梦见爬上高楼", "decode": "可能内心中有征服欲望或是渴望有个情人。"},
        {"dream": "梦见大厦内很豪华",
         "decode": "预示生活上，或是工作上，会面临一些你不喜欢的变化，而你不得不接受。"},
        {"dream": "梦见大厦空荡荡的或非常简陋", "decode": "则预示条件将会得到改善，或处境会有好的转变。"},
        {"dream": "梦见自己从大厦顶上向下看", "decode": "但是感到很害怕，表示了你对性爱既期待又害怕的心理。"},
        {"dream": "梦见由大厦的旋转餐厅",
         "decode": "或是观景阳台，或是游乐场向下看，预示爱情方面会有意想不到的发展。"},
        {"dream": "梦见自己住在一栋大厦里",
         "decode": "暗示你最近有些情绪不安，可能因为无法向对方表白，或是感到压力重重却不好与人沟通而忧虑。"},
        {"dream": "梦见黑房子",
         "decode": "通常是你自己内心的象征，暗示你的关注度从外部世界又退缩回了自己的内心世界。"},
        {"dream": "梦见战壕",
         "decode": "暗示目前所处的环境让你感到非常害怕、不安，你希望能避开那些让你感到害怕的人和事，以及每天迎头而来的纷繁压力。"},
        {"dream": "梦见土牢", "decode": "预示你会有烦恼和困难，或内心将遭受痛苦煎熬。"},
        {"dream": "梦见自己被关进土牢里",
         "decode": "预示你将遇到严重的困难，或是杂乱无章难以处理的难题，同时也表示你会想方设法找到解决之道，突破困境，改变现状。"},
        {"dream": "梦见自己走出了土牢", "decode": "预示你就要摆脱困境。"},
        {"dream": "梦见身陷牢房",
         "decode": "预示着梦者在生活中将遇到严重的麻烦与困难;梦见走出牢房，意味着梦者最终能从困境中走出来。"},
        {"dream": "梦见走出牢房", "decode": "意味着梦者最终能从困境中走出来。"},
        {"dream": "梦见建猪圈", "decode": "吉兆，生活会幸福。"},
        {"dream": "梦见猪圈和猪",
         "decode": "这是平生难得的吉梦，可能给你带来不小的财势，养猪致富是不少中国农民的梦想，可能猪是农民眼中的生钱物，不久的将来你就会拥有大量的财富。"},
        {"dream": "梦见猪圈里猪群肥头大耳",
         "decode": "这是吉梦，预示着你的财势很旺，钱财会滚滚而来，会带来意想不到的好事情或小额投资带来高回报。"},
        {"dream": "梦见把猪赶进猪圈", "decode": "这是金钱上的祥瑞。"},
        {"dream": "梦见救起掉进粪池的猪", "decode": "开启名誉运、财运等的吉祥之兆。"},
        {"dream": "梦见混浊的鱼塘", "decode": "表示因生活放荡而引起的疾病。"},
        {"dream": "梦见池水清澈的鱼塘中许多鱼儿欢快地游来游去",
         "decode": "暗示事业上收人颇丰，你将享受到很多快乐。"},
        {"dream": "梦见空荡荡的鱼塘", "decode": "预示死对头正向你逼近。"},
        {"dream": "梦见掉进一个清澈的池塘",
         "decode": "预示好运和相亲相爱一定要来临;如果池塘很脏，预示的情况正好相反。"},
        {"dream": "梦到住破房子", "decode": "则象征爱情方面的运势，爱情必然将会获得成功。"},
        {"dream": "梦见盖新房", "decode": "身体不久会康复。"},
        ]

        df = pd.DataFrame(data)  # 创建DataFrame对象

        for item in df.itertuples():
            item_dict = {'dream': item.dream, 'decode': item.decode}
            if match_search_query(item_dict, search_query):
                items.append(item_dict)

        categories = ["人物", "动物", "植物", "物品", "活动", "情感", "生活", "鬼神", "自然", "建筑", "其他"]

        context = {'items': items, 'categories': categories, 'data_items': df.iterrows()}
        return render(request, 'index.html', context)
    elif category == "其他":
        data = [
            {"dream": "梦见原谅了别人", "decode": "大家会和睦相处。"},
        {"dream": "梦见自己对某中特殊的工作一无所知", "decode": "实际上却很精通此项工作。"},
        {"dream": "梦见对自己的工作职责不清楚", "decode": "会得到晋升。"},
        {"dream": "梦见自己不懂宗教礼节", "decode": "家人会接连生病。"},
        {"dream": "梦见你参加某次战斗", "decode": "表示在事业上会遇到反对者，而法律对你也不利。"},
        {"dream": "梦见战斗景象", "decode": "表示你正在挥霍你的金钱和时间。"},
        {"dream": "梦见她的爱人正在战斗", "decode": "表示她的男友不值得结交。"},
        {"dream": "梦见你被人打败了", "decode": "意味着你将失去你的权利和财富。"},
        {"dream": "梦见你鞭打入侵者", "decode": "表示勇气和坚强，你能克服别人的阻碍而获得财富和名声。"},
        {"dream": "梦见赚钱", "decode": "往往暗示要赔钱、破财。"},
        {"dream": "梦见自己赚到了钱", "decode": "暗示做梦人近期正殚精竭虑想赚钱。"},
        {"dream": "梦见别人赚了钱", "decode": "表示做梦人正下定决心，给自己施加压力，努力赚钱。"},
        {"dream": "梦见赚到了钱",
         "decode": "预示生意终于要进入盈利阶段，也许现在生意还有些不如人意，但就快获得丰厚收益。"},
        {"dream": "梦见赚钱了", "decode": "预示工作上将取得成绩、销售成绩显著，并将得到领导重视。"},
        {"dream": "梦见自己去了美国或是人在美国",
         "decode": "或是在看地图上的美国，通常预示事业上会有令你激动的变化。"},
        {"dream": "梦见腐烂的苹果", "decode": "就意味着你最近会有经济上的损失。"},
        {"dream": "梦见与动物交谈", "decode": "是凶兆，不久会患病，必须注意身体健康。"},
        {"dream": "梦见自己被单位或学校开除", "decode": "预示会出名。"},
        {"dream": "梦见自己被逐出家庭或家族", "decode": "则预示你将来会有独到建树，并深受人们尊敬。"},
        {"dream": "梦见有亲戚被家族开除", "decode": "则预示工作中你将得到提升，或学习成绩提高。"},
        {"dream": "梦见自己把别人从家庭或家族中赶出去", "decode": "预示你会和那个人成为朋友。"},
        {"dream": "梦见自己处于三角形中", "decode": "这梦表明现在的你对家人或朋友感到不满。"},
        {"dream": "梦见三角形",
         "decode": "预示你将充满忧伤地与朋友分别或预示你的恋爱进程将以激烈争吵来宣告结束。"},
        {"dream": "梦见你看到了三角形的东西", "decode": "象征着朋友的离散，爱情的红灯亮起了。"},
        {"dream": "梦见不规则的物体", "decode": "可能是你白天看到某物体，并对此感兴趣。"},
        {"dream": "梦到自己处于一个不规则的物体内", "decode": "预示着你的生活不规律，提示你要思考和调整自己。"},
        {"dream": "梦见周围很多不规则物体", "decode": "表示着你对某种制度的排斥，提示要适应现状。"},
        {"dream": "梦见形状又丑又怪的任何物品", "decode": "都是失望的预兆。"},
        {"dream": "梦见的形状美丽和谐", "decode": "预示促进健康和事业发展的有利条件。"},
        ]

        df = pd.DataFrame(data)  # 创建DataFrame对象

        for item in df.itertuples():
            item_dict = {'dream': item.dream, 'decode': item.decode}
            if match_search_query(item_dict, search_query):
                items.append(item_dict)

        categories = ["人物", "动物", "植物", "物品", "活动", "情感", "生活", "鬼神", "自然", "建筑", "其他"]

        context = {'items': items, 'categories': categories, 'data_items': df.iterrows()}
        return render(request, 'index.html', context)
    else:
        with open('data/data0.csv', 'r', encoding='GBK') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['category'] == category and (search_query in row['dream'] or search_query in row['decode']):
                    items.append({'dream': row['dream'], 'decode': row['decode']})

        categories = ["人物", "动物", "植物", "物品", "活动", "情感", "生活", "鬼神", "自然", "建筑", "其他"]

        context = {'items': items, 'categories': categories}
        return render(request, 'index.html', context)

def home_page_view(request):
    return render(request, 'home_page.html')

def chat_view(request):
    return render(request, 'chat.html')

# 定义一个函数匹配搜索查询
def match_search_query(row, search_query):
    if search_query in row['dream'] or search_query in row['decode']:
        return True
    else:
        return False

from django.shortcuts import render
from .dream_interpreter import interpret_dream

def dream_interpreter(request):
    result = {}
    if request.method == 'POST':
        dream = request.POST.get('dream')
        result['interpretation'] = interpret_dream(dream)
    return render(request, 'interpreter.html', result)

def emotion_analysis(request):
    sentiment_result = None
    elements = None
    if request.method == 'POST':
        dream_description = request.POST['dream_description']
        sentiment_result, elements = analyze_dream(dream_description)
    return render(request, 'emotion.html', {'sentiment_result': sentiment_result, 'elements': elements})


from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from paddlenlp import Taskflow
from paddlenlp.transformers import GPTLMHeadModel, GPTChineseTokenizer
import paddle

# 情感分析模型初始化
senta = Taskflow("sentiment_analysis", model="skep_ernie_1.0_large_ch")

# 文本生成模型初始化
model_name = 'gpt-cpm-small-cn-distill'
tokenizer = GPTChineseTokenizer.from_pretrained(model_name)
model = GPTLMHeadModel.from_pretrained(model_name)
model.eval()


@csrf_exempt
def dream_analysis(request):
    completed_dream = None
    sentiment_result = None

    if request.method == 'POST':
        dream_input = request.POST['dream_input']
        # 将输入的梦境转化为模型可接受的格式
        inputs_ids = tokenizer(dream_input)['input_ids']
        # 增加一个维度，并转化为 PaddlePaddle Tensor
        inputs_ids = paddle.to_tensor([inputs_ids])

        # 使用文本生成模型补全梦境
        outputs, _ = model.generate(
            input_ids=inputs_ids,
            max_length=50,  # 你可以根据需要修改生成文本的最大长度
            decode_strategy='beam_search',
            repetition_penalty=1.3,
            num_beams=2)

        # 转化模型输出为文本
        completed_dream = tokenizer.convert_ids_to_string(outputs[0].numpy().tolist())
        sentiment_result = senta(completed_dream)

    return render(request, 'shengcheng.html',
                  {'completed_dream': completed_dream, 'sentiment_result': sentiment_result})


from django.shortcuts import render
from .dream_interpreter import interpret_dream
from .dream_analyzer import analyze_dream
from paddlenlp import Taskflow
from paddlenlp.transformers import GPTLMHeadModel, GPTChineseTokenizer
import paddle

# 情感分析模型初始化
senta = Taskflow("sentiment_analysis", model="skep_ernie_1.0_large_ch")

# 文本生成模型初始化
model_name = 'gpt-cpm-small-cn-distill'
tokenizer = GPTChineseTokenizer.from_pretrained(model_name)
model = GPTLMHeadModel.from_pretrained(model_name)
model.eval()


def new_view(request):
    from .analysis import ciyun_analysis  # 注意在正确的位置导入这个函数

    completed_dream = None
    sentiment_result = None
    interpretation = None
    elements = None
    analysis = None

    if request.method == 'POST':
        form_id = request.POST.get('form_id')

        if form_id == 'short_form':
            dream_input = request.POST.get('dream_input')

            # 梦境生成
            inputs_ids = tokenizer(dream_input)['input_ids']
            inputs_ids = paddle.to_tensor([inputs_ids])
            outputs, _ = model.generate(
                input_ids=inputs_ids,
                max_length=50,
                decode_strategy='beam_search',
                repetition_penalty=1.3,
                num_beams=2)
            completed_dream = tokenizer.convert_ids_to_string(outputs[0].numpy().tolist())

            # 情感分析和梦境元素的解析
            sentiment_result, elements = analyze_dream(completed_dream)

            # 梦境解析
            interpretation = interpret_dream(completed_dream)

        elif form_id == 'detailed_form':
            dream_input = request.POST.get('dream_input_detailed')
            # 词云分析
            analysis = ciyun_analysis(dream_input)

    return render(request, 'new.html',
                  {'completed_dream': completed_dream, 'sentiment_result': sentiment_result,
                   'interpretation': interpretation, 'elements': elements, 'analysis': analysis})


from django.shortcuts import render
from .analysis import ciyun_analysis

def ciyun_view(request):
    dream = ""
    analysis = None
    if request.method == 'POST':
        dream = request.POST.get('dream', '')
        if dream:
            analysis = ciyun_analysis(dream)
    return render(request, 'ciyun.html', {'dream': dream, 'analysis': analysis})




