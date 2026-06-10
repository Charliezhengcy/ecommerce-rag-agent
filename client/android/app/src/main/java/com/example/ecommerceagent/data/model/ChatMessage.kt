package com.example.ecommerceagent.data.model

data class ChatMessage(
    val id: String, val role: MessageRole, val content: String,
    val productCards: List<ProductCardUiModel> = emptyList(),
    val isStreaming: Boolean = false, val createdAt: Long = System.currentTimeMillis()
)
enum class MessageRole { USER, ASSISTANT }
data class ChatUiState(
    val sessionId: String, val messages: List<ChatMessage> = emptyList(),
    val inputText: String = "", val isStreaming: Boolean = false, val errorMessage: String? = null
)

