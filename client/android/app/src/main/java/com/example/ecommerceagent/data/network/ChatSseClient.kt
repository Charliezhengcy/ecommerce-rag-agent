package com.example.ecommerceagent.data.network

import com.example.ecommerceagent.data.model.ProductCardUiModel
import com.example.ecommerceagent.data.model.SseEvent
import kotlinx.serialization.Serializable
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.toRequestBody
import java.io.IOException

class ChatSseClient(private val client: OkHttpClient = OkHttpClient()) {
    private val json = Json { ignoreUnknownKeys = true }
    @Serializable private data class Delta(val text: String = "")
    @Serializable private data class Start(val message_id: String = "")
    @Serializable private data class ErrorBody(val message: String = "")
    @Serializable private data class Cards(val products: List<ProductCardUiModel> = emptyList())

    fun stream(sessionId: String, message: String, onEvent: (SseEvent) -> Unit): Call {
        val body = """{"session_id":${json.encodeToString(sessionId)},"message":${json.encodeToString(message)}}"""
        val request = Request.Builder().url("${ApiConfig.BASE_URL}/api/chat/stream")
            .header("Accept", "text/event-stream").post(body.toRequestBody("application/json".toMediaType())).build()
        return client.newCall(request).also { call ->
            call.enqueue(object : Callback {
                override fun onFailure(call: Call, e: IOException) = onEvent(SseEvent.Error(e.message ?: "网络错误"))
                override fun onResponse(call: Call, response: Response) {
                    response.use {
                        val source = response.body?.source() ?: return
                        var event = ""; val data = StringBuilder()
                        while (!source.exhausted()) {
                            val line = source.readUtf8Line() ?: break
                            when {
                                line.startsWith("event:") -> event = line.substringAfter("event:").trim()
                                line.startsWith("data:") -> data.append(line.substringAfter("data:").trim())
                                line.isBlank() -> {
                                    dispatch(event, data.toString(), onEvent); event = ""; data.clear()
                                }
                            }
                        }
                    }
                }
            })
        }
    }

    private fun dispatch(event: String, data: String, callback: (SseEvent) -> Unit) {
        if (data.isBlank()) return
        callback(when (event) {
            "message_start" -> SseEvent.Start(json.decodeFromString<Start>(data).message_id)
            "message_delta" -> SseEvent.Delta(json.decodeFromString<Delta>(data).text)
            "product_cards" -> SseEvent.Products(json.decodeFromString<Cards>(data).products)
            "error" -> SseEvent.Error(json.decodeFromString<ErrorBody>(data).message)
            "message_done" -> SseEvent.Done
            else -> return
        })
    }
}
