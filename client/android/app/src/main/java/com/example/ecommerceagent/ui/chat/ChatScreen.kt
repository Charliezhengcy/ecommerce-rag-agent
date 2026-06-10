package com.example.ecommerceagent.ui.chat

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.example.ecommerceagent.ui.chat.components.DemoPromptChips
import com.example.ecommerceagent.ui.chat.components.MessageBubble

@OptIn(ExperimentalMaterial3Api::class)
@Composable fun ChatScreen(viewModel: ChatViewModel, onProductClick: (String) -> Unit) {
    val state by viewModel.state.collectAsStateWithLifecycle()
    Scaffold(topBar = { TopAppBar(title = { Text("AI 电商导购助手") }) }) { padding ->
        Column(Modifier.fillMaxSize().padding(padding).padding(horizontal = 12.dp)) {
            DemoPromptChips(viewModel::send)
            LazyColumn(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(12.dp),
                contentPadding = PaddingValues(vertical = 12.dp)) {
                items(state.messages, key = { it.id }) { MessageBubble(it, onProductClick) }
            }
            Row(Modifier.fillMaxWidth().padding(bottom = 8.dp)) {
                OutlinedTextField(state.inputText, viewModel::updateInput, modifier = Modifier.weight(1f),
                    placeholder = { Text("告诉我你想买什么") }, enabled = !state.isStreaming)
                Button(onClick = { viewModel.send() }, enabled = state.inputText.isNotBlank() && !state.isStreaming,
                    modifier = Modifier.padding(start = 8.dp)) { Text("发送") }
            }
        }
    }
}

