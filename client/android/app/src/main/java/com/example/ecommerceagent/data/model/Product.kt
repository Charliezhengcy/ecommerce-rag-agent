package com.example.ecommerceagent.data.model

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class ProductCardUiModel(
    @SerialName("product_id") val productId: String,
    val title: String,
    val brand: String,
    val category: String,
    @SerialName("sub_category") val subCategory: String,
    val price: Double,
    @SerialName("price_text") val priceText: String,
    @SerialName("image_url") val imageUrl: String,
    val reason: String = "",
    val tags: List<String> = emptyList()
)

@Serializable
data class ProductDetail(
    @SerialName("product_id") val productId: String,
    val title: String, val brand: String, val category: String,
    @SerialName("sub_category") val subCategory: String,
    @SerialName("price_text") val priceText: String,
    @SerialName("image_url") val imageUrl: String,
    @SerialName("marketing_description") val description: String = "",
    val skus: List<Sku> = emptyList(),
    @SerialName("official_faq") val faq: List<Faq> = emptyList(),
    @SerialName("user_reviews") val reviews: List<Review> = emptyList()
)

@Serializable data class Sku(@SerialName("sku_id") val skuId: String = "", val properties: Map<String, String> = emptyMap(), val price: Double = 0.0)
@Serializable data class Faq(val question: String = "", val answer: String = "")
@Serializable data class Review(val nickname: String = "", val rating: Int = 0, val content: String = "")

