package com.example.ecommerceagent.data.network

import com.example.ecommerceagent.data.model.ProductDetail
import kotlinx.serialization.json.Json
import okhttp3.OkHttpClient
import okhttp3.Request

class ProductApi(private val client: OkHttpClient = OkHttpClient()) {
    private val json = Json { ignoreUnknownKeys = true }
    fun get(productId: String): ProductDetail {
        val response = client.newCall(Request.Builder().url("${ApiConfig.BASE_URL}/api/products/$productId").build()).execute()
        response.use { return json.decodeFromString(it.body!!.string()) }
    }
}

