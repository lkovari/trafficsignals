package com.lkovari.mobile.apps.trafficsignals

import com.lkovari.mobile.apps.trafficsignals.data.LicensePreferences
import com.lkovari.mobile.apps.trafficsignals.data.SignCatalog
import com.lkovari.mobile.apps.trafficsignals.data.SignCategory
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test
import java.io.File

class SignCatalogTest {
    @Test
    fun nineCategories() {
        assertEquals(9, SignCatalog.categories.size)
    }

    @Test
    fun uniqueSignIds() {
        val ids = SignCatalog.signs.map { sign -> sign.id }
        assertEquals(ids.size, ids.toSet().size)
    }

    @Test
    fun categoryCountsMatchLegacyCatalog() {
        assertEquals(8, SignCatalog.signsIn(SignCategory.RouteType).size)
        assertEquals(9, SignCatalog.signsIn(SignCategory.Priority).size)
        assertEquals(38, SignCatalog.signsIn(SignCategory.Mandatory).size)
        assertEquals(43, SignCatalog.signsIn(SignCategory.Prohibitory).size)
        assertEquals(64, SignCatalog.signsIn(SignCategory.Warning).size)
        assertEquals(105, SignCatalog.signsIn(SignCategory.Information).size)
        assertEquals(46, SignCatalog.signsIn(SignCategory.Additional).size)
        assertEquals(26, SignCatalog.signsIn(SignCategory.RoadMarking).size)
        assertEquals(16, SignCatalog.signsIn(SignCategory.TrafficLight).size)
        assertEquals(355, SignCatalog.signs.size)
    }

    @Test
    fun everySignHasEnglishAndHungarianStrings() {
        val english = parseStringNames(File("src/main/res/values/strings.xml"))
        val hungarian = parseStringNames(File("src/main/res/values-hu/strings.xml"))
        SignCatalog.signs.forEach { sign ->
            assertTrue(sign.id, english.contains(sign.id))
            assertTrue(sign.id, hungarian.contains(sign.id))
        }
        SignCatalog.categories.forEach { category ->
            val key = stringNameFor(category)
            assertTrue(key, english.contains(key))
            assertTrue(key, hungarian.contains(key))
        }
    }

    @Test
    fun licenseDefaultsToNotAccepted() {
        assertFalse(LicensePreferences.DEFAULT_ACCEPTED)
        assertEquals("islicenseaccepted", LicensePreferences.ACCEPTED_KEY.name)
    }

    private fun stringNameFor(category: SignCategory): String {
        return when (category) {
            SignCategory.RouteType -> "kategoria_utvonaltipus"
            SignCategory.Priority -> "kategoria_elsobsegetszabalyozo"
            SignCategory.Mandatory -> "kategoria_utasitastado"
            SignCategory.Prohibitory -> "kategoria_tilalmi"
            SignCategory.Warning -> "kategoria_veszelytjelzo"
            SignCategory.Information -> "kategoria_tajekoztatastado"
            SignCategory.Additional -> "kategoria_kiegeszito"
            SignCategory.RoadMarking -> "kategoria_utburkolatijelek"
            SignCategory.TrafficLight -> "kategoria_fenyjelzokeszulekek"
        }
    }

    private fun parseStringNames(file: File): Set<String> {
        val names = mutableSetOf<String>()
        val regex = Regex("""<string name="([^"]+)">""")
        regex.findAll(file.readText(Charsets.UTF_8)).forEach { match ->
            names.add(match.groupValues[1])
        }
        return names
    }
}
