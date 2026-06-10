# API 设计

- `GET /health`：健康检查。
- `GET /api/products`：支持 `category`、`sub_category`、`keyword`、`limit`。
- `GET /api/products/{id}`：返回完整真实商品详情。
- `POST /api/chat/stream`：请求包含 `session_id`、`message`。

SSE 事件：`message_start`、`message_delta`、`product_cards`、`message_done`、`error`。卡片字段由 ProductService 生成。

