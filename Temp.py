### function definition
def name_reduction(product_name, all_keywords):
    results = []
    for idx, string in enumerate(all_keywords):
        index = product_name.find(string)
        if index != -1:
            results.append(index)
    if results != []:
        return product_name[results[len(results)-1]:]
    return product_name

def find_shelf_with_keywords(product_name):

    shelves_keywords = {
        "飲料": ["水", "咖啡", "拿鐵", "花生湯", "茶", "沙士", "豆漿", "可爾必思", "果菜汁", "梅子酢", "黑麥汁", "仙草蜜", "可樂", "雪碧"],
        "酒類": ["威士忌", "啤酒"],
        "南北貨": ["米", "麵粉", "紅豆", "黃豆", "麵筋", "花瓜", "鰻魚罐頭", "玉米罐頭"],
        "調味料": ["醬", "醋", "油", "鹽", "蔗糖", "美乃滋", "黑糖", "味醂"],
        "營養品": ["奶粉", "B群", "維他命", "鈣", "酵素", "錠", "麥片", "雞精", "抹茶粉", "善存", "益生菌"],
        "清潔用品": ["紙巾", "尿布", "衛生紙", "夾鏈袋", "保鮮膜", "洗碗", "洗衣", "菜瓜布", "手套", "漂白水", "沐浴", "牙膏", "牙刷", "洗髮", "棉", "皂", "洗面乳", "洗手", "漱口水"],
        "冷藏/凍食品": ["豆腐", "餃", "抓餅", "餛飩", "饅頭", "肉片", "火鍋料", "布丁", "冰淇淋", "牛奶", "優酪乳", "優格", "蛋", "湯底"],
        "休閒食品": ["餅乾", "洋芋片", "巧克力", "零食", "果凍", "牛奶糖", "喉糖", "棉花糖", "海苔", "堅果", "夾心", "金莎", "脆笛酥", "乖乖", "蒟蒻", "麻花捲"],
    }

    all_keywords = []
    for category in shelves_keywords.values():
        all_keywords.extend(category)
    product_name = name_reduction(product_name, all_keywords)

    for shelf, keywords in shelves_keywords.items():
        for keyword in keywords:
            index = product_name.find(keyword)
            if index != -1:
                return [shelf, keyword]
    return ["未找到貨架", "未找到商品"]

def find_shelf_position(shelf, keyword):

    shelves_position = {
        "茶": (4, 24),
        "啤酒": (5, 12),
        "米": (10, 25),
        "醬": (1, 6),
        "雞精": (10, 7),
        "衛生紙": (18, 16),
        "牛奶": (26, 23),
        "巧克力": (27, 5),
        "堅果": (28, 6),
        "飲料": (3.6, 25),
        "酒類": (3.6, 15),
        "南北貨": (16, 25),
        "調味料": (3.6, 5),
        "營養品": (16, 15),
        "清潔用品": (16, 5),
        "冷藏/凍食品": (27.5, 20),
        "休閒食品": (27.5, 6)
        # "冷藏/凍食品": (26.5, 19),
        # "休閒食品": (26.5, 6)
    }

    for string, position in shelves_position.items():
        if keyword == string:
            return [position[0], position[1], 1]    # 1: 回傳商品座標
    for string, position in shelves_position.items():
        if shelf == string:
            return [position[0], position[1], 0]    # 0: 未有對應商品的座標，回傳類別位置
    return [-1, -1, -1]

### calling function
[shelf, keyword] = find_shelf_with_keywords(product_name="衛生紙")
[x, y, label] = find_shelf_position(shelf, keyword)