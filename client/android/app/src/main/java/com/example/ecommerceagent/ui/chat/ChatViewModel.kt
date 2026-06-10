package com.example.ecommerceagent.ui.chat

import androidx.lifecycle.ViewModel
import com.example.ecommerceagent.data.model.*
import com.example.ecommerceagent.data.repository.ChatRepository
import com.example.ecommerceagent.util.SessionIdProvider
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

class ChatViewModel(private val repository: ChatRepository = ChatRepository()) : ViewModel() {
    private val _state = MutableStateFlow(ChatUiState(SessionIdProvider.id))
    val state: StateFlow<ChatUiState> = _state.asStateFlow()

    fun updateInput(value: String) { _state.value = _state.value.copy(inputText = value) }
    fun send(text: String = _state.value.inputText) {
        if (text.isBlank() || _state.value.isStreaming) return
        val assistantId = "assistant-${System.currentTimeMillis()}"
        _state.value = _state.value.copy(
            inputText = "", isStreaming = true, errorMessage = null,
            messages = _state.value.messages + ChatMessage("user-${System.currentTimeMillis()}", MessageRole.USER, text) +
                ChatMessage(assistantId, MessageRole.ASSISTANT, "", isStreaming = true)
        )
        repository.stream(_state.value.sessionId, text) { event ->
            when (event) {
                is SseEvent.Delta -> updateAssistant(assistantId) { it.copy(content = it.content + event.text) }
                is SseEvent.Products -> updateAssistant(assistantId) { it.copy(productCards = event.products) }
                is SseEvent.Error -> {
                    updateAssistant(assistantId) { it.copy(content = if (it.content.isBlank()) event.message else it.content, isStreaming = false) }
                    _state.value = _state.value.copy(isStreaming = false, errorMessage = event.message)
                }
                SseEvent.Done -> {
                    updateAssistant(assistantId) { it.copy(isStreaming = false) }
                    _state.value = _state.value.copy(isStreaming = false)
                }
                is SseEvent.Start -> Unit
            }
        }
    }
    private fun updateAssistant(id: String, transform: (ChatMessage) -> ChatMessage) {
        _state.value = _state.value.copy(messages = _state.value.messages.map { if (it.id == id) transform(it) else it })
    }
}

