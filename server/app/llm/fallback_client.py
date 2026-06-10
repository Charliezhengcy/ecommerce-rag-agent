from app.utils.text_utils import chunks


class FallbackClient:
    def recommendation(self, products: list[dict]) -> str:
        if not products:
            return ("我没有在当前商品库中找到完全符合你条件的商品。\n\n"
                    "你可以尝试：\n1. 放宽预算范围；\n2. 减少排除条件；\n3. 换一个相近类目重新搜索。")
        lines = ["我根据当前商品库和你的条件，筛选出以下选择："]
        for index, item in enumerate(products[:3], 1):
            tags = "、".join(item.get("tags", [])[:3]) or item["sub_category"]
            lines.append(f"{index}. {item['title']}，{item['brand']}，¥{item['min_sku_price']:g} 起；匹配点：{tags}。")
        lines.append("商品卡片中的标题、价格和图片均来自真实商品库，建议点开详情确认具体 SKU。")
        return "\n".join(lines)

    def comparison(self, products: list[dict], focus: str) -> str:
        if len(products) < 2:
            return "目前没有足够的上一轮推荐商品可供对比，请先让我推荐至少两款商品。"
        first, second = products[:2]
        return (
            f"1. {first['title']}：{first['brand']}，¥{first['min_sku_price']:g} 起，"
            f"标签包括{'、'.join(first.get('tags', [])[:3]) or first['sub_category']}。\n"
            f"2. {second['title']}：{second['brand']}，¥{second['min_sku_price']:g} 起，"
            f"标签包括{'、'.join(second.get('tags', [])[:3]) or second['sub_category']}。\n"
            f"围绕“{focus}”选择时，优先看商品详情和真实评价中是否明确覆盖该需求；预算优先可选价格更低的一款。"
        )

    async def stream_text(self, text: str):
        for chunk in chunks(text):
            yield chunk

