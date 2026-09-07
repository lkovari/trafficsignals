package com.lkovari.mobile.apps.trafficsignals.ui

import android.app.Application
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Surface
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewModelScope
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument
import com.lkovari.mobile.apps.trafficsignals.data.AppLanguage
import com.lkovari.mobile.apps.trafficsignals.data.LanguagePreferences
import com.lkovari.mobile.apps.trafficsignals.data.LicensePreferences
import com.lkovari.mobile.apps.trafficsignals.data.SignCatalog
import com.lkovari.mobile.apps.trafficsignals.data.SignCategory
import com.lkovari.mobile.apps.trafficsignals.ui.screens.AboutScreen
import com.lkovari.mobile.apps.trafficsignals.ui.screens.CategoryListScreen
import com.lkovari.mobile.apps.trafficsignals.ui.screens.LicenseScreen
import com.lkovari.mobile.apps.trafficsignals.ui.screens.SignDetailScreen
import com.lkovari.mobile.apps.trafficsignals.ui.screens.SignGridScreen
import com.lkovari.mobile.apps.trafficsignals.ui.theme.TrafficSignalsTheme
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

class LicenseViewModel(application: Application) : AndroidViewModel(application) {
    private val preferences = LicensePreferences(application)

    val accepted: StateFlow<Boolean?> = preferences.accepted.map { value -> value }.stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5_000),
        initialValue = null
    )

    fun accept() {
        viewModelScope.launch {
            preferences.accept()
        }
    }
}

class LanguageViewModel(application: Application) : AndroidViewModel(application) {
    private val preferences = LanguagePreferences(application)
    private val deviceLanguageTag = application.resources.configuration.locales[0].toLanguageTag()
    private val override = MutableStateFlow<AppLanguage?>(null)

    val language: StateFlow<AppLanguage> = combine(
        preferences.languageTag,
        override
    ) { stored, immediate ->
        immediate ?: AppLanguage.resolve(stored, deviceLanguageTag)
    }.stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5_000),
        initialValue = AppLanguage.fromDevice(deviceLanguageTag)
    )

    fun setLanguage(language: AppLanguage) {
        override.value = language
        viewModelScope.launch {
            preferences.setLanguage(language)
        }
    }
}

@Composable
fun TrafficSignalsApp(
    onRefuseLicense: () -> Unit,
    licenseViewModel: LicenseViewModel = viewModel(),
    languageViewModel: LanguageViewModel = viewModel()
) {
    val accepted by licenseViewModel.accepted.collectAsStateWithLifecycle()
    val language by languageViewModel.language.collectAsStateWithLifecycle()
    TrafficSignalsTheme {
        ProvideAppLocale(language) {
            Surface(modifier = Modifier.fillMaxSize()) {
                when (accepted) {
                    null -> { }
                    false -> LicenseScreen(
                        onAccept = { licenseViewModel.accept() },
                        onRefuse = onRefuseLicense
                    )
                    true -> TrafficSignalsNav(
                        language = language,
                        onLanguage = languageViewModel::setLanguage
                    )
                }
            }
        }
    }
}

@Composable
private fun TrafficSignalsNav(
    language: AppLanguage,
    onLanguage: (AppLanguage) -> Unit
) {
    val navController = rememberNavController()
    NavHost(navController = navController, startDestination = "categories") {
        composable("categories") {
            CategoryListScreen(
                language = language,
                onLanguage = onLanguage,
                onCategory = { category ->
                    navController.navigate("category/${category.name}")
                },
                onAbout = { navController.navigate("about") }
            )
        }
        composable(
            route = "category/{category}",
            arguments = listOf(navArgument("category") { type = NavType.StringType })
        ) { entry ->
            val category = SignCategory.valueOf(entry.arguments?.getString("category").orEmpty())
            SignGridScreen(
                category = category,
                onBack = { navController.popBackStack() },
                onSign = { sign ->
                    navController.navigate("sign/${sign.category.name}/${sign.id}")
                }
            )
        }
        composable(
            route = "sign/{category}/{id}",
            arguments = listOf(
                navArgument("category") { type = NavType.StringType },
                navArgument("id") { type = NavType.StringType }
            )
        ) { entry ->
            val category = SignCategory.valueOf(entry.arguments?.getString("category").orEmpty())
            val id = entry.arguments?.getString("id").orEmpty()
            val signs = SignCatalog.signsIn(category)
            val index = signs.indexOfFirst { sign -> sign.id == id }
            SignDetailScreen(
                signs = signs,
                index = if (index >= 0) index else 0,
                onBack = { navController.popBackStack() },
                onSelect = { sign ->
                    navController.navigate("sign/${sign.category.name}/${sign.id}") {
                        popUpTo("sign/${category.name}/$id") { inclusive = true }
                    }
                }
            )
        }
        composable("about") {
            AboutScreen(
                language = language,
                onLanguage = onLanguage,
                onBack = { navController.popBackStack() }
            )
        }
    }
}
