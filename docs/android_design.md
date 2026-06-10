# Android 设计

客户端采用 Compose + MVVM + Navigation。ChatSseClient 按 `event:`、`data:` 和空行解析 SSE；ChatViewModel 逐步追加 delta，并将商品卡片绑定到助手消息。

ChatScreen 包含快捷问题、消息列表和输入区。点击卡片进入 ProductDetailScreen，由 ProductApi 加载真实详情。

