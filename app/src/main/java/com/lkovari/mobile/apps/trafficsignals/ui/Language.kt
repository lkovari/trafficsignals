package com.lkovari.mobile.apps.trafficsignals.ui

import android.content.res.Configuration
import android.os.LocaleList
import androidx.compose.foundation.Image
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.SideEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.platform.LocalConfiguration
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalResources
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import com.lkovari.mobile.apps.trafficsignals.R
import com.lkovari.mobile.apps.trafficsignals.data.AppLanguage
import java.util.Locale

@Composable
fun ProvideAppLocale(language: AppLanguage, content: @Composable () -> Unit) {
    val baseContext = LocalContext.current
    val locale = remember(language) { language.toLocale() }
    val localizedContext = remember(baseContext, locale) {
        val config = Configuration(baseContext.resources.configuration)
        config.setLocale(locale)
        config.setLocales(LocaleList(locale))
        baseContext.createConfigurationContext(config)
    }
    SideEffect {
        Locale.setDefault(locale)
    }
    CompositionLocalProvider(
        LocalContext provides localizedContext,
        LocalConfiguration provides localizedContext.resources.configuration,
        LocalResources provides localizedContext.resources,
        content = content
    )
}

@Composable
fun LanguageSwitcher(
    selected: AppLanguage,
    onSelect: (AppLanguage) -> Unit,
    modifier: Modifier = Modifier
) {
    Row(modifier = modifier, verticalAlignment = Alignment.CenterVertically) {
        FlagButton(
            flagRes = R.drawable.flag_hungary,
            contentDescription = stringResource(R.string.language_hungarian),
            selected = selected == AppLanguage.Hungarian,
            onClick = { onSelect(AppLanguage.Hungarian) }
        )
        FlagButton(
            flagRes = R.drawable.flag_gb,
            contentDescription = stringResource(R.string.language_english),
            selected = selected == AppLanguage.English,
            onClick = { onSelect(AppLanguage.English) }
        )
    }
}

@Composable
private fun FlagButton(
    flagRes: Int,
    contentDescription: String,
    selected: Boolean,
    onClick: () -> Unit
) {
    val shape = RoundedCornerShape(2.dp)
    IconButton(onClick = onClick, modifier = Modifier.size(40.dp)) {
        Image(
            painter = painterResource(flagRes),
            contentDescription = contentDescription,
            modifier = Modifier
                .size(width = 28.dp, height = 18.dp)
                .border(
                    width = if (selected) 2.dp else 1.dp,
                    color = if (selected) {
                        MaterialTheme.colorScheme.primary
                    } else {
                        MaterialTheme.colorScheme.outline
                    },
                    shape = shape
                )
                .clip(shape)
        )
    }
}
