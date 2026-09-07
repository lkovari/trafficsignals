package com.lkovari.mobile.apps.trafficsignals.data

import java.util.Locale

enum class AppLanguage(val tag: String) {
    Hungarian("hu"),
    English("en");

    fun toLocale(): Locale = Locale.forLanguageTag(tag)

    companion object {
        fun fromDevice(language: String): AppLanguage {
            val normalized = language.lowercase(Locale.ROOT).replace('_', '-')
            return if (normalized == "hu" || normalized.startsWith("hu-")) {
                Hungarian
            } else {
                English
            }
        }

        fun fromStored(tag: String?): AppLanguage? {
            if (tag.isNullOrBlank()) return null
            return entries.find { language -> language.tag.equals(tag, ignoreCase = true) }
        }

        fun resolve(storedTag: String?, deviceLanguage: String): AppLanguage {
            return fromStored(storedTag) ?: fromDevice(deviceLanguage)
        }
    }
}
