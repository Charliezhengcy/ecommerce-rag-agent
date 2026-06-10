# ecommerce-rag-agent

基于真实商品数据的 Android Kotlin + FastAPI + Chroma + Doubao-Seed-2.0-lite 电商智能导购。后端先执行价格、类目与排除条件过滤，再进行向量/关键词检索和 RAG 解释；商品卡片始终由真实商品库生成。未配置 Doubao 时自动使用本地模板回复，完整 SSE 链路仍可演示。

## 功能

- Android Jetpack Compose 聊天、SSE 流式回复、商品卡片与详情页
- 商品清洗、图片映射、RAG 文档与 Chroma 索引构建
- Query Parser、硬条件过滤、语义检索、排序、RAG Prompt
- 多轮条件继承、排除条件累积、上一轮前两款商品对比
- Doubao 调用失败或无 API Key 时的本地 fallback
- 防幻觉：模型不能生成卡片，价格、图片、品牌、SKU 均来自商品库

## 1. 数据

本仓库工作区已解压数据。重新解压时执行：

```bash
mkdir -p data/raw
unzip ecommerce_agent_dataset.zip -d data/raw
```

最终应存在 `data/raw/ecommerce_agent_dataset/`。

## 2. 后端

```bash
cd server
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

在 `server/.env` 中自行填写 `DOUBAO_API_KEY` 和 `DOUBAO_MODEL`。不要提交 `.env`。不填写时使用 fallback。

```bash
python scripts/inspect_dataset.py
python scripts/prepare_data.py
python scripts/build_chroma_index.py
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

检查：

```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/products?limit=2
```

索引脚本优先使用本机已缓存的 `paraphrase-multilingual-MiniLM-L12-v2`；模型不可用时使用稳定的离线哈希向量构建 Chroma。未构建索引时，服务会退回本地关键词排序。

## 3. 测试

```bash
cd server
source .venv/bin/activate
pytest -q
```

## 4. Android

```bash
cd client/android
./gradlew assembleDebug
```

也可用 Android Studio 打开 `client/android` 并运行到 Emulator。默认后端地址为 `http://10.0.2.2:8000`；真机请修改 `ApiConfig.BASE_URL` 为电脑局域网 IP。

## API

- `GET /health`
- `GET /api/products`
- `GET /api/products/{product_id}`
- `POST /api/chat/stream`

SSE 顺序为 `message_start`、多个 `message_delta`、可选 `product_cards`、`message_done`；错误时发送 `error`。

详细设计见 [docs](docs/)。
