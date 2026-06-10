package com.example.ecommerceagent.util
import java.util.UUID
object SessionIdProvider { val id: String = "android-${UUID.randomUUID()}" }

