package com.example.ecommerceagent.ui.product

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import coil.compose.AsyncImage
import com.example.ecommerceagent.data.network.ApiConfig

@OptIn(ExperimentalMaterial3Api::class)
@Composable fun ProductDetailScreen(id: String, viewModel: ProductDetailViewModel, onBack: () -> Unit) {
    val product by viewModel.product.collectAsStateWithLifecycle()
    LaunchedEffect(id) { viewModel.load(id) }
    Scaffold(topBar = { TopAppBar(title = { Text("商品详情") }, navigationIcon = { TextButton(onClick = onBack) { Text("返回") } }) }) { padding ->
        product?.let { productItem ->
            LazyColumn(Modifier.padding(padding), contentPadding = PaddingValues(bottom = 24.dp)) {
                item { AsyncImage(ApiConfig.BASE_URL + productItem.imageUrl, productItem.title, Modifier.fillMaxWidth().height(280.dp), contentScale = ContentScale.Crop) }
                item { Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                    Text(productItem.title, style = MaterialTheme.typography.headlineSmall); Text("${productItem.brand} · ${productItem.category} / ${productItem.subCategory}")
                    Text(productItem.priceText, color = MaterialTheme.colorScheme.primary, style = MaterialTheme.typography.headlineSmall)
                    Text("商品描述", style = MaterialTheme.typography.titleMedium); Text(productItem.description)
                    Text("SKU", style = MaterialTheme.typography.titleMedium); productItem.skus.forEach { Text("${it.properties.values.joinToString()} · ¥${it.price}") }
                    Text("官方问答", style = MaterialTheme.typography.titleMedium); productItem.faq.forEach { Text("问：${it.question}\n答：${it.answer}") }
                    Text("用户评价", style = MaterialTheme.typography.titleMedium); productItem.reviews.forEach { Text("${it.nickname} ${it.rating}分：${it.content}") }
                } }
            }
        } ?: Box(Modifier.fillMaxSize().padding(padding)) { CircularProgressIndicator() }
    }
}
