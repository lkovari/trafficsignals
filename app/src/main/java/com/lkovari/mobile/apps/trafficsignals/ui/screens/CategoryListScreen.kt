package com.lkovari.mobile.apps.trafficsignals.ui.screens

import androidx.compose.foundation.Image
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.safeDrawing
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Info
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
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
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.lkovari.mobile.apps.trafficsignals.R
import com.lkovari.mobile.apps.trafficsignals.data.AppLanguage
import com.lkovari.mobile.apps.trafficsignals.data.SignCatalog
import com.lkovari.mobile.apps.trafficsignals.data.SignCategory
import com.lkovari.mobile.apps.trafficsignals.ui.LanguageSwitcher

private const val CategoryColumns = 3

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CategoryListScreen(
    language: AppLanguage,
    onLanguage: (AppLanguage) -> Unit,
    onCategory: (SignCategory) -> Unit,
    onAbout: () -> Unit
) {
    Scaffold(
        contentWindowInsets = WindowInsets.safeDrawing,
        topBar = {
            TopAppBar(
                title = { Text(stringResource(R.string.menuTitle)) },
                actions = {
                    LanguageSwitcher(selected = language, onSelect = onLanguage)
                    IconButton(onClick = onAbout) {
                        Icon(
                            imageVector = Icons.Outlined.Info,
                            contentDescription = stringResource(R.string.menu_info)
                        )
                    }
                }
            )
        }
    ) { inner ->
        val rows = SignCatalog.categories.chunked(CategoryColumns)
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(inner)
                .padding(horizontal = 12.dp, vertical = 8.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            rows.forEach { rowItems ->
                Row(
                    modifier = Modifier
                        .weight(1f)
                        .fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    rowItems.forEach { category ->
                        CategoryTile(
                            category = category,
                            onClick = { onCategory(category) },
                            modifier = Modifier
                                .weight(1f)
                                .fillMaxHeight()
                        )
                    }
                    repeat(CategoryColumns - rowItems.size) {
                        Spacer(modifier = Modifier.weight(1f))
                    }
                }
            }
        }
    }
}

@Composable
private fun CategoryTile(
    category: SignCategory,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    val count = SignCatalog.signsIn(category).size
    Card(
        modifier = modifier.clickable(onClick = onClick),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(bottom = 6.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Image(
                painter = painterResource(SignCatalog.categoryIconRes(category)),
                contentDescription = stringResource(SignCatalog.categoryTitleRes(category)),
                modifier = Modifier
                    .weight(1f)
                    .fillMaxWidth()
                    .padding(6.dp),
                contentScale = ContentScale.Fit
            )
            Text(
                text = stringResource(SignCatalog.categoryTitleRes(category)),
                modifier = Modifier.padding(horizontal = 6.dp),
                style = MaterialTheme.typography.labelMedium,
                textAlign = TextAlign.Center,
                maxLines = 2,
                overflow = TextOverflow.Ellipsis
            )
            Text(
                text = stringResource(R.string.category_sign_count, count),
                modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp),
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                textAlign = TextAlign.Center,
                maxLines = 1
            )
        }
    }
}
