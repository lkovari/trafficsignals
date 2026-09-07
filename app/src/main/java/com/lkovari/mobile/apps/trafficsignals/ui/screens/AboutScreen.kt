package com.lkovari.mobile.apps.trafficsignals.ui.screens

import androidx.compose.foundation.Image
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.safeDrawing
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.text.TextAutoSize
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
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.lkovari.mobile.apps.trafficsignals.R
import com.lkovari.mobile.apps.trafficsignals.data.AppLanguage
import com.lkovari.mobile.apps.trafficsignals.ui.LanguageSwitcher

internal fun aboutLogoSizeDp(availableHeightDp: Float): Float {
    return (availableHeightDp * 0.16f).coerceIn(64f, 112f)
}

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
    val kreszUrl = stringResource(R.string.about_kresz_url)
    val bodyAutoSize = TextAutoSize.StepBased(
        minFontSize = 10.sp,
        maxFontSize = 13.sp,
        stepSize = 0.25.sp
    )
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
        BoxWithConstraints(
            modifier = Modifier
                .fillMaxSize()
                .padding(inner)
                .padding(horizontal = 12.dp, vertical = 4.dp)
        ) {
            val logoSize = aboutLogoSizeDp(maxHeight.value).dp
            Column(
                modifier = Modifier.fillMaxSize(),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.spacedBy(3.dp)
            ) {
                Image(
                    painter = painterResource(R.drawable.ic_launcher_foreground),
                    contentDescription = null,
                    modifier = Modifier
                        .size(logoSize)
                        .clipToBounds()
                        .scale(1.85f)
                )
                Text(
                    text = stringResource(R.string.about_appname),
                    style = MaterialTheme.typography.titleSmall,
                    textAlign = TextAlign.Center,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
                Text(
                    text = stringResource(R.string.about_description),
                    modifier = Modifier
                        .weight(1f, fill = false)
                        .fillMaxWidth(),
                    style = MaterialTheme.typography.bodySmall.copy(lineHeight = 14.sp),
                    textAlign = TextAlign.Center,
                    overflow = TextOverflow.Ellipsis,
                    autoSize = bodyAutoSize
                )
                Text(
                    text = stringResource(R.string.about_author),
                    style = MaterialTheme.typography.bodySmall,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
                Text(
                    text = stringResource(R.string.about_artwork),
                    modifier = Modifier
                        .weight(1f, fill = false)
                        .fillMaxWidth(),
                    style = MaterialTheme.typography.bodySmall.copy(lineHeight = 14.sp),
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    textAlign = TextAlign.Center,
                    overflow = TextOverflow.Ellipsis,
                    autoSize = bodyAutoSize
                )
                Text(
                    text = stringResource(R.string.about_kresz_label),
                    style = MaterialTheme.typography.labelLarge,
                    color = MaterialTheme.colorScheme.primary,
                    textAlign = TextAlign.Center,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier.clickable { uriHandler.openUri(kreszUrl) }
                )
                Text(
                    text = kreszUrl,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.primary,
                    textDecoration = TextDecoration.Underline,
                    textAlign = TextAlign.Center,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier
                        .fillMaxWidth()
                        .clickable { uriHandler.openUri(kreszUrl) }
                )
                Text(
                    text = stringResource(R.string.about_watermark),
                    modifier = Modifier
                        .weight(0.8f, fill = false)
                        .fillMaxWidth(),
                    style = MaterialTheme.typography.bodySmall.copy(lineHeight = 14.sp),
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    textAlign = TextAlign.Center,
                    overflow = TextOverflow.Ellipsis,
                    autoSize = bodyAutoSize
                )
                Text(
                    text = stringResource(R.string.about_source_label),
                    style = MaterialTheme.typography.labelLarge,
                    color = MaterialTheme.colorScheme.primary,
                    textDecoration = TextDecoration.Underline,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier.clickable { uriHandler.openUri(sourceUrl) }
                )
                Text(
                    text = stringResource(R.string.about_privacy_policy),
                    style = MaterialTheme.typography.labelLarge,
                    color = MaterialTheme.colorScheme.primary,
                    textDecoration = TextDecoration.Underline,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier.clickable { uriHandler.openUri(privacyUrl) }
                )
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.Center,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        text = stringResource(R.string.about_copyright_prefix),
                        style = MaterialTheme.typography.bodySmall,
                        maxLines = 1
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
                        style = MaterialTheme.typography.bodySmall,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                }
            }
        }
    }
}
