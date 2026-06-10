package com.example.ecommerceagent.ui.chat.components

import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.example.ecommerceagent.data.model.ChatMessage
import com.example.ecommerceagent.data.model.MessageRole

@Composable fun MessageBubble(message: ChatMessage, onProductClick: (String) -> Unit) {
    Column(Modifier.fillMaxWidth(), horizontalAlignment = if (message.role == MessageRole.USER) Alignment.End else Alignment.Start) {
        Surface(color = if (message.role == MessageRole.USER) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant,
            shape = RoundedCornerShape(18.dp), modifier = Modifier.widthIn(max = 340.dp)) {
            Text(message.content + if (message.isStreaming) " ▍" else "", Modifier.padding(12.dp),
                color = if (message.role == MessageRole.USER) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant)
        }
        if (message.productCards.isNotEmpty()) {
            Row(Modifier.padding(top = 8.dp).horizontalScroll(rememberScrollState())) {
                message.productCards.forEach { ProductCard(it) { onProductClick(it.productId) } }
            }
        }
    }
}

