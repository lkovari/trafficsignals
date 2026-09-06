package com.lkovari.mobile.apps.trafficsignals.data

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.booleanPreferencesKey
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.preferencesDataStore
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

private val Context.licenseDataStore: DataStore<Preferences> by preferencesDataStore(name = "trsipr")

class LicensePreferences(private val context: Context) {
    val accepted: Flow<Boolean> = context.licenseDataStore.data.map { prefs ->
        prefs[ACCEPTED_KEY] ?: DEFAULT_ACCEPTED
    }

    suspend fun accept() {
        context.licenseDataStore.edit { prefs ->
            prefs[ACCEPTED_KEY] = true
        }
    }

    companion object {
        val ACCEPTED_KEY = booleanPreferencesKey("islicenseaccepted")
        const val DEFAULT_ACCEPTED = false
    }
}
