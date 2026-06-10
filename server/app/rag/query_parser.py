import re

from app.schemas.chat import ParsedQuery

CATEGORY_KEYWORDS = {
    "美妆护肤": ["护肤", "美妆", "精华", "面霜", "洗面奶", "洁面", "防晒", "爽肤水", "化妆水", "乳液", "油皮", "干皮", "敏感肌", "保湿", "控油"],
    "数码电子": ["数码", "电子", "耳机", "蓝牙耳机", "手机", "键盘", "鼠标", "充电宝", "音箱", "降噪", "续航", "快充"],
    "服饰运动": ["服饰", "运动", "跑鞋", "跑步鞋", "运动鞋", "外套", "T恤", "裤子", "瑜伽", "轻量", "缓震", "透气"],
    "食品生活": ["食品", "零食", "饮料", "咖啡", "茶", "饼干", "早餐", "低糖", "无糖", "生活"],
}
SUB_CATEGORY_ALIASES = {"跑鞋": "跑步鞋", "运动鞋": "跑步鞋", "耳机": "蓝牙耳机", "无线耳机": "蓝牙耳机", "防晒": "防晒霜", "洁面": "洗面奶"}
PREFERENCE_TERMS = ["油皮", "干皮", "敏感肌", "保湿", "控油", "修护", "温和", "清爽", "降噪", "续航", "快充", "轻量", "缓震", "透气", "通勤", "低糖", "无糖", "健康"]


class QueryParser:
    def __init__(self, products: list[dict]):
        self.sub_categories = {item["sub_category"] for item in products}
        self.categories = {item["category"] for item in products}

    def parse(self, query: str, session: dict | None = None) -> ParsedQuery:
        result = ParsedQuery(raw_query=query)
        if any(term in query for term in ["对比", "比较", "哪个更", "哪款更", "前两款", "刚才推荐的"]):
            result.intent = "compare"
        elif any(term in query for term in ["不要", "不含", "别推荐", "排除", "除了", "不想要"]):
            result.intent = "exclude_search"
        elif session and session.get("current_category") and len(query) <= 15:
            result.intent = "refine"
        elif any(term in query for term in ["推荐", "有没有", "有哪些", "帮我找", "想买", "适合"]):
            result.intent = "recommend"
        else:
            result.intent = "general_question"

        price_range = re.search(r"(\d+(?:\.\d+)?)\s*(?:-|到)\s*(\d+(?:\.\d+)?)", query)
        if price_range:
            result.price_min, result.price_max = map(float, price_range.groups())
        else:
            for pattern in [r"(\d+(?:\.\d+)?)\s*元?以下", r"(\d+(?:\.\d+)?)\s*以内", r"预算\s*(\d+(?:\.\d+)?)", r"不超过\s*(\d+(?:\.\d+)?)", r"低于\s*(\d+(?:\.\d+)?)"]:
                match = re.search(pattern, query)
                if match:
                    result.price_max = float(match.group(1))
                    break

        for category, terms in CATEGORY_KEYWORDS.items():
            if any(term in query for term in terms):
                # The supplied dataset calls this category 食品饮料, while the spec vocabulary says 食品生活.
                result.category = "食品饮料" if category == "食品生活" and "食品饮料" in self.categories else category
                break
        if result.price_max is not None and result.category:
            result.intent = "filter_search" if result.intent == "recommend" else result.intent

        for alias, target in sorted(SUB_CATEGORY_ALIASES.items(), key=lambda item: len(item[0]), reverse=True):
            if alias in query:
                if target in self.sub_categories:
                    result.sub_category = target
                else:
                    result.include_terms.append(alias)
                break
        if not result.sub_category:
            for sub in sorted(self.sub_categories, key=len, reverse=True):
                if sub in query:
                    result.sub_category = sub
                    break

        # Capture each negative phrase up to punctuation/conjunction; normalize "含酒精" to "酒精".
        for match in re.finditer(r"(?:不要|不含|别推荐|排除|除了|不想要)([^，。！？；,;]+)", query):
            phrase = re.split(r"(?:的|也不要|并且|而且)", match.group(1))[0].strip()
            phrase = re.sub(r"^(?:含|有)", "", phrase)
            if phrase:
                result.exclude_terms.append(phrase)
        result.include_terms += [term for term in PREFERENCE_TERMS if term in query and term not in result.exclude_terms]
        result.include_terms = list(dict.fromkeys(result.include_terms))
        result.exclude_terms = list(dict.fromkeys(result.exclude_terms))
        return result
