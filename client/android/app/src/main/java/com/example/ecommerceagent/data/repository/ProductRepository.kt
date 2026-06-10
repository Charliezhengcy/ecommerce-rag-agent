package com.example.ecommerceagent.data.repository
import com.example.ecommerceagent.data.network.ProductApi
class ProductRepository(private val api: ProductApi = ProductApi()) { fun get(id: String) = api.get(id) }

