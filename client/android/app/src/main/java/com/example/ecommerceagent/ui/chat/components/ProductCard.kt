package com.example.ecommerceagent.ui.chat.components

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.unit.dp
import coil.compose.AsyncImage
import com.example.ecommerceagent.data.model.ProductCardUiModel
import com.example.ecommerceagent.data.network.ApiConfig

@Composable fun ProductCard(product: ProductCardUiModel, onClick: () -> Unit) {
    Card(Modifier.width(240.dp).padding(end = 10.dp).clickable(onClick = onClick), shape = RoundedCornerShape(16.dp)) {
        Column {
            AsyncImage(model = ApiConfig.BASE_URL + product.imageUrl, contentDescription = product.title,
                modifier = Modifier.fillMaxWidth().height(130.dp), contentScale = ContentScale.Crop)
            Column(Modifier.padding(12.dp)) {
                Text(product.title, maxLines = 2, style = MaterialTheme.typography.titleSmall)
                Text("${product.brand} · ${product.subCategory}", style = MaterialTheme.typography.bodySmall)
                Text(product.priceText, color = MaterialTheme.colorScheme.primary, style = MaterialTheme.typography.titleMedium)
                Text(product.reason, maxLines = 2, style = MaterialTheme.typography.bodySmall)
            }
        }
    }
}

