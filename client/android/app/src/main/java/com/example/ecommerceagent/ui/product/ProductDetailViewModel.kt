package com.example.ecommerceagent.ui.product

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.ecommerceagent.data.model.ProductDetail
import com.example.ecommerceagent.data.repository.ProductRepository
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class ProductDetailViewModel(private val repository: ProductRepository = ProductRepository()) : ViewModel() {
    private val _product = MutableStateFlow<ProductDetail?>(null)
    val product = _product.asStateFlow()
    fun load(id: String) { if (_product.value?.productId == id) return; viewModelScope.launch(Dispatchers.IO) { _product.value = repository.get(id) } }
}

