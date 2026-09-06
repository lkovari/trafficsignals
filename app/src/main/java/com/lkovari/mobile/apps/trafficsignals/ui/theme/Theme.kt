package com.lkovari.mobile.apps.trafficsignals.ui.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

private val LightColors = lightColorScheme(
    primary = SignBlue,
    onPrimary = Color.White,
    secondary = SignRed,
    onSecondary = Color.White,
    tertiary = SignYellow,
    onTertiary = Ink,
    background = Paper,
    onBackground = Ink,
    surface = Color.White,
    onSurface = Ink,
    surfaceVariant = Color(0xFFE6E2D6),
    onSurfaceVariant = MutedInk,
    outline = Color(0xFFC5C0B4),
    error = SignRed,
    onError = Color.White
)

private val DarkColors = darkColorScheme(
    primary = Color(0xFF7EB0E8),
    onPrimary = Asphalt,
    secondary = Color(0xFFE25A6A),
    onSecondary = Asphalt,
    tertiary = SignYellow,
    onTertiary = Asphalt,
    background = Asphalt,
    onBackground = NightCream,
    surface = AsphaltPanel,
    onSurface = NightCream,
    surfaceVariant = Color(0xFF323942),
    onSurfaceVariant = NightMuted,
    outline = Color(0xFF4A5360),
    error = Color(0xFFE25A6A),
    onError = Asphalt
)

@Composable
fun TrafficSignalsTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    MaterialTheme(
        colorScheme = if (darkTheme) DarkColors else LightColors,
        typography = Typography,
        content = content
    )
}
