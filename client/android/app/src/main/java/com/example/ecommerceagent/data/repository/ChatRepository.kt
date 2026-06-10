package com.example.ecommerceagent.data.repository
import com.example.ecommerceagent.data.model.SseEvent
import com.example.ecommerceagent.data.network.ChatSseClient
class ChatRepository(private val client: ChatSseClient = ChatSseClient()) {
    fun stream(sessionId: String, message: String, onEvent: (SseEvent) -> Unit) = client.stream(sessionId, message, onEvent)
}

