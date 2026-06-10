package com.example.ecommerceagent.data.model

sealed interface SseEvent {
    data class Start(val messageId: String): SseEvent
    data class Delta(val text: String): SseEvent
    data class Products(val products: List<ProductCardUiModel>): SseEvent
    data class Error(val message: String): SseEvent
    data object Done: SseEvent
}

