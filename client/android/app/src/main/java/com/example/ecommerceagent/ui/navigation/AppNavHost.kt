package com.example.ecommerceagent.ui.navigation

import androidx.compose.runtime.Composable
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavType
import androidx.navigation.compose.*
import androidx.navigation.navArgument
import com.example.ecommerceagent.ui.chat.ChatScreen
import com.example.ecommerceagent.ui.chat.ChatViewModel
import com.example.ecommerceagent.ui.product.ProductDetailScreen
import com.example.ecommerceagent.ui.product.ProductDetailViewModel

@Composable fun AppNavHost() {
    val nav = rememberNavController()
    NavHost(nav, startDestination = "chat") {
        composable("chat") { ChatScreen(viewModel<ChatViewModel>()) { nav.navigate("product/$it") } }
        composable("product/{id}", arguments = listOf(navArgument("id") { type = NavType.StringType })) {
            ProductDetailScreen(it.arguments!!.getString("id")!!, viewModel<ProductDetailViewModel>()) { nav.popBackStack() }
        }
    }
}

