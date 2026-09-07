package com.lkovari.mobile.apps.trafficsignals

import com.lkovari.mobile.apps.trafficsignals.data.AppLanguage
import com.lkovari.mobile.apps.trafficsignals.data.LanguagePreferences
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

class AppLanguageTest {
    @Test
    fun deviceHungarianUsesHungarian() {
        assertEquals(AppLanguage.Hungarian, AppLanguage.fromDevice("hu"))
        assertEquals(AppLanguage.Hungarian, AppLanguage.fromDevice("HU"))
        assertEquals(AppLanguage.Hungarian, AppLanguage.fromDevice("hu-HU"))
    }

    @Test
    fun deviceNonHungarianUsesEnglish() {
        assertEquals(AppLanguage.English, AppLanguage.fromDevice("en"))
        assertEquals(AppLanguage.English, AppLanguage.fromDevice("de"))
        assertEquals(AppLanguage.English, AppLanguage.fromDevice("en-GB"))
    }

    @Test
    fun storedChoiceOverridesDeviceLocale() {
        assertEquals(AppLanguage.English, AppLanguage.resolve("en", "hu"))
        assertEquals(AppLanguage.Hungarian, AppLanguage.resolve("hu", "en"))
    }

    @Test
    fun missingStoredChoiceFollowsDevice() {
        assertEquals(AppLanguage.Hungarian, AppLanguage.resolve(null, "hu"))
        assertEquals(AppLanguage.English, AppLanguage.resolve("", "de"))
        assertEquals(AppLanguage.Hungarian, AppLanguage.resolve("fr", "hu"))
    }

    @Test
    fun languagePreferenceHasNoDefaultOverride() {
        assertNull(LanguagePreferences.DEFAULT_TAG)
        assertEquals("language_tag", LanguagePreferences.LANGUAGE_KEY.name)
    }

    @Test
    fun languageSwitcherStringsExistInEnglishAndHungarian() {
        val english = parseStringNames(java.io.File("src/main/res/values/strings.xml"))
        val hungarian = parseStringNames(java.io.File("src/main/res/values-hu/strings.xml"))
        listOf("language_hungarian", "language_english").forEach { key ->
            assertTrue(key, english.contains(key))
            assertTrue(key, hungarian.contains(key))
        }
    }

    private fun parseStringNames(file: java.io.File): Set<String> {
        val names = mutableSetOf<String>()
        val regex = Regex("""<string name="([^"]+)">""")
        regex.findAll(file.readText(Charsets.UTF_8)).forEach { match ->
            names.add(match.groupValues[1])
        }
        return names
    }
}
