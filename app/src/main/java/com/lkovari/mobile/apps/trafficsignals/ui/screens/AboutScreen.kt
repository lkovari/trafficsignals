package com.lkovari.mobile.apps.trafficsignals.ui.screens

import androidx.compose.foundation.Image
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.safeDrawing
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.outlined.Copyright
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clipToBounds
import androidx.compose.ui.draw.scale
import androidx.compose.ui.platform.LocalUriHandler
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextDecoration
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.lkovari.mobile.apps.trafficsignals.R
import com.lkovari.mobile.apps.trafficsignals.data.AppLanguage
import com.lkovari.mobile.apps.trafficsignals.ui.LanguageSwitcher

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AboutScreen(
    language: AppLanguage,
    onLanguage: (AppLanguage) -> Unit,
    onBack: () -> Unit
) {
    val uriHandler = LocalUriHandler.current
    val sourceUrl = stringResource(R.string.about_source_url)
    val privacyUrl = stringResource(R.string.about_privacy_url)
    Scaffold(
        contentWindowInsets = WindowInsets.safeDrawing,
        topBar = {
            TopAppBar(
                title = { Text(stringResource(R.string.menu_info)) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(
                            imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                            contentDescription = null
                        )
                    }
                },
                actions = {
                    LanguageSwitcher(selected = language, onSelect = onLanguage)
                }
            )
        }
    ) { inner ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(inner)
                .verticalScroll(rememberScrollState())
                .padding(horizontal = 16.dp, vertical = 8.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(6.dp)
        ) {
            Image(
                painter = painterResource(R.drawable.ic_launcher_foreground),
                contentDescription = null,
                modifier = Modifier
                    .size(192.dp)
                    .clipToBounds()
                    .scale(1.9f)
            )
            Text(
                text = stringResource(R.string.about_appname),
                style = MaterialTheme.typography.titleMedium,
                textAlign = TextAlign.Center
            )
            Text(
                text = stringResource(R.string.about_description),
                style = MaterialTheme.typography.bodySmall.copy(lineHeight = 16.sp),
                textAlign = TextAlign.Center
            )
            Text(
                text = stringResource(R.string.about_author),
                style = MaterialTheme.typography.bodySmall
            )
            Text(
                text = stringResource(R.string.about_artwork),
                style = MaterialTheme.typography.bodySmall.copy(lineHeight = 16.sp),
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                textAlign = TextAlign.Center
            )
            Spacer(modifier = Modifier.height(8.dp))
            val kreszUrl = stringResource(R.string.about_kresz_url)
            Text(
                text = stringResource(R.string.about_kresz_label),
                style = MaterialTheme.typography.labelLarge,
                color = MaterialTheme.colorScheme.primary,
                textAlign = TextAlign.Center,
                modifier = Modifier.clickable { uriHandler.openUri(kreszUrl) }
            )
            Text(
                text = kreszUrl,
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.primary,
                textDecoration = TextDecoration.Underline,
                textAlign = TextAlign.Center,
                modifier = Modifier.clickable { uriHandler.openUri(kreszUrl) }
            )
            Text(
                text = stringResource(R.string.about_watermark),
                style = MaterialTheme.typography.bodySmall.copy(lineHeight = 16.sp),
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                textAlign = TextAlign.Center
            )
            Spacer(modifier = Modifier.height(8.dp))
            Text(
                text = stringResource(R.string.about_source_label),
                style = MaterialTheme.typography.labelLarge,
                color = MaterialTheme.colorScheme.primary,
                textDecoration = TextDecoration.Underline,
                modifier = Modifier.clickable { uriHandler.openUri(sourceUrl) }
            )
            Text(
                text = stringResource(R.string.about_privacy_policy),
                style = MaterialTheme.typography.labelLarge,
                color = MaterialTheme.colorScheme.primary,
                textDecoration = TextDecoration.Underline,
                modifier = Modifier.clickable { uriHandler.openUri(privacyUrl) }
            )
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.Center,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = stringResource(R.string.about_copyright_prefix),
                    style = MaterialTheme.typography.bodySmall
                )
                Icon(
                    imageVector = Icons.Outlined.Copyright,
                    contentDescription = null,
                    modifier = Modifier
                        .padding(horizontal = 4.dp)
                        .size(14.dp)
                )
                Text(
                    text = stringResource(R.string.about_copyright_holder),
                    style = MaterialTheme.typography.bodySmall
                )
            }
        }
    }
}
