package com.example.ecommerceagent.ui.chat.components

import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.rememberScrollState
import androidx.compose.material3.AssistChip
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier

private val prompts = listOf(
    "适合油皮的护肤品" to "推荐一款适合油皮的护肤品",
    "200 元以下蓝牙耳机" to "200 元以下的蓝牙耳机有哪些？",
    "推荐跑步鞋" to "帮我推荐跑步鞋",
    "不要含酒精的防晒霜" to "推荐防晒霜，但不要含酒精的，也不要日系品牌",
    "对比刚才前两款" to "对比刚才推荐的前两款，哪个更适合敏感肌？"
)

@Composable fun DemoPromptChips(onClick: (String) -> Unit) {
    Row(Modifier.horizontalScroll(rememberScrollState())) {
        prompts.forEach { (label, prompt) -> AssistChip(onClick = { onClick(prompt) }, label = { Text(label) }) }
    }
}

