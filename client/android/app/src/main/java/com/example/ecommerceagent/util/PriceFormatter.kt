package com.example.ecommerceagent.util
object PriceFormatter { fun format(value: Double) = "¥${if (value % 1.0 == 0.0) value.toInt() else value}" }
