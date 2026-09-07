package com.lkovari.mobile.apps.trafficsignals

import com.lkovari.mobile.apps.trafficsignals.ui.screens.aboutLogoSizeDp
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class AboutLayoutTest {
    @Test
    fun logoFitsXever7ProContentHeight() {
        val available = 800f - 64f - 48f
        val logo = aboutLogoSizeDp(available)
        assertEquals(110.08f, logo, 0.1f)
        assertTrue(logo <= 112f)
        val fixedChrome = logo + 20f + 16f + 20f + 16f + 20f + 20f + 16f + 33f
        assertTrue(fixedChrome < available)
    }

    @Test
    fun logoShrinksOnShortPhones() {
        val available = 640f - 64f - 48f - 48f
        val logo = aboutLogoSizeDp(available)
        assertEquals(76.8f, logo, 0.1f)
        assertTrue(logo >= 64f)
    }

    @Test
    fun logoNeverExceedsCap() {
        assertEquals(112f, aboutLogoSizeDp(2000f), 0.01f)
        assertEquals(64f, aboutLogoSizeDp(100f), 0.01f)
    }
}
