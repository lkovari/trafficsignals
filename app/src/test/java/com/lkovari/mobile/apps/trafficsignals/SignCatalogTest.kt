package com.lkovari.mobile.apps.trafficsignals

import com.lkovari.mobile.apps.trafficsignals.data.KreszCitation
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
    fun tenCategories() {
        assertEquals(10, SignCatalog.categories.size)
    }

    @Test
    fun uniqueSignIds() {
        val ids = SignCatalog.signs.map { sign -> sign.id }
        assertEquals(ids.size, ids.toSet().size)
    }

    @Test
    fun categoryCountsMatchLegacyCatalog() {
        assertEquals(10, SignCatalog.signsIn(SignCategory.Police).size)
        assertEquals(8, SignCatalog.signsIn(SignCategory.RouteType).size)
        assertEquals(9, SignCatalog.signsIn(SignCategory.Priority).size)
        assertEquals(45, SignCatalog.signsIn(SignCategory.Mandatory).size)
        assertEquals(49, SignCatalog.signsIn(SignCategory.Prohibitory).size)
        assertEquals(70, SignCatalog.signsIn(SignCategory.Warning).size)
        assertEquals(123, SignCatalog.signsIn(SignCategory.Information).size)
        assertEquals(63, SignCatalog.signsIn(SignCategory.Additional).size)
        assertEquals(29, SignCatalog.signsIn(SignCategory.RoadMarking).size)
        assertEquals(20, SignCatalog.signsIn(SignCategory.TrafficLight).size)
        assertEquals(426, SignCatalog.signs.size)
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
        SignCatalog.signs.forEach { sign ->
            val nameRes = sign.nameRes
            if (nameRes != null) {
                val key = "${sign.id}_name"
                assertTrue(key, english.contains(key))
                assertTrue(key, hungarian.contains(key))
            }
        }
        listOf("kresz_paragraph", "about_kresz_label").forEach { key ->
            assertTrue(key, english.contains(key))
            assertTrue(key, hungarian.contains(key))
        }
    }

    @Test
    fun everySignHasKreszParagraph() {
        SignCatalog.signs.forEach { sign ->
            val citation = sign.kreszParagraph
            assertTrue(sign.id, citation.contains("§"))
            assertEquals(citation, KreszCitation.forId(sign.id))
        }
    }

    @Test
    fun kreszParagraphsMatchStatute() {
        assertEquals("6. § (1) a)", SignCatalog.signById("rendori_karokoldalra")?.kreszParagraph)
        assertEquals("7. § (1)", SignCatalog.signById("rendori_jelzoor")?.kreszParagraph)
        assertEquals("8. § (2) a)", SignCatalog.signById("fenyjelzo_gyalogos_zold")?.kreszParagraph)
        assertEquals("9. § (4) d)", SignCatalog.signById("fenyjelzo_piros")?.kreszParagraph)
        assertEquals("11. § (1) a)", SignCatalog.signById("utvonaltipus_autopalyakezdete")?.kreszParagraph)
        assertEquals("12. § (1) b)", SignCatalog.signById("elsobseg_alljelsobsegadaskotelezo")?.kreszParagraph)
        assertEquals("13. § (1) c)", SignCatalog.signById("utasitastado_korforgalom")?.kreszParagraph)
        assertEquals("14. § (1) z)", SignCatalog.signById("tilalmi_behajtanitilos")?.kreszParagraph)
        assertEquals("15. § (1) a)", SignCatalog.signById("tilalmi_megallnitilos")?.kreszParagraph)
        assertEquals("16. § (1) p)", SignCatalog.signById("veszely_gyalogosatkeles")?.kreszParagraph)
        assertEquals("17. § (1) a)", SignCatalog.signById("kulonleges_gyalogosatkelohely")?.kreszParagraph)
        assertEquals("18. § (1) c)", SignCatalog.signById("utburkolat_zarovonal")?.kreszParagraph)
        assertEquals("19. § (6) a)", SignCatalog.signById("veszely_fenysorompo_tilos")?.kreszParagraph)
        assertEquals("10. § (2)", SignCatalog.signById("kiegeszito_idoszak")?.kreszParagraph)
    }

    @Test
    fun licenseDefaultsToNotAccepted() {
        assertFalse(LicensePreferences.DEFAULT_ACCEPTED)
        assertEquals("islicenseaccepted", LicensePreferences.ACCEPTED_KEY.name)
    }

    private fun stringNameFor(category: SignCategory): String {
        return when (category) {
            SignCategory.Police -> "kategoria_rendori"
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
