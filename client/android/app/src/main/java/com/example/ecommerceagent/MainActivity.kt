package com.example.ecommerceagent
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) { super.onCreate(savedInstanceState); setContent { EcommerceAgentApp() } }
}
