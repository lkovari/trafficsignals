package com.lkovari.mobile.apps.trafficsignals.data

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.preferencesDataStore
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

private val Context.languageDataStore: DataStore<Preferences> by preferencesDataStore(name = "language")

class LanguagePreferences(private val context: Context) {
    val languageTag: Flow<String?> = context.languageDataStore.data.map { prefs ->
        prefs[LANGUAGE_KEY]
    }

    suspend fun setLanguage(language: AppLanguage) {
        context.languageDataStore.edit { prefs ->
            prefs[LANGUAGE_KEY] = language.tag
        }
    }

    companion object {
        val LANGUAGE_KEY = stringPreferencesKey("language_tag")
        val DEFAULT_TAG: String? = null
    }
}
