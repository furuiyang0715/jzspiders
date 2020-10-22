def get_language_mark(language):
    language_map = {
        "中文": "zh-CHS",
        "英语": "en",
        "韩语": "ko",
        "日语": "ja",
        "法语": "fr",
        "俄语": "ru",
        "西班牙语": "es",
        "葡萄牙语": "pt",
        "印地语": "hi",
        "阿拉伯语": "ar",
        "丹麦语": "da",
        "德语": "de",
        "希腊语": "el",
        "芬兰语": "fi",
        "意大利语": "it",
        "马来语": "ms",
        "越南语": "vi",
        "印尼语": "id",
        "荷兰语": "nl"
    }
    return language_map.get(language, 'auto')


print(get_language_mark('中文'))
