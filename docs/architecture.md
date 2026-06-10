# 架构

Android Compose 通过 OkHttp 调用 FastAPI。商品 API 返回真实详情；聊天 API 以 SSE 推送文本和卡片。

后端链路：Query Parser -> Session 合并 -> Structured Filter -> Chroma/关键词检索 -> Ranker -> Prompt Builder -> Doubao/Fallback -> SSE。静态图片由 `/static/dataset` 提供。

