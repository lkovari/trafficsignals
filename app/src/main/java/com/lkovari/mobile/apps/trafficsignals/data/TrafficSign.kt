package com.lkovari.mobile.apps.trafficsignals.data

enum class SignCategory {
    Police,
    RouteType,
    Priority,
    Mandatory,
    Prohibitory,
    Warning,
    Information,
    Additional,
    RoadMarking,
    TrafficLight
}

data class TrafficSign(
    val id: String,
    val category: SignCategory,
    val imageRes: Int,
    val titleRes: Int
)
