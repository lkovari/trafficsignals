# Changelog

All notable changes to **Hungarian Traffic Signals** (`com.lkovari.mobile.apps.trafficsignals`) are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning matches `versionName` **2.0.0** / `versionCode` **2** (minSdk 24, targetSdk 36).

## [Unreleased]

### Fixed

- Home category grid stays inside the system safe area on all phones (status bar, gesture/nav bar); tiles shrink to fit four rows instead of clipping.

### Added

- Police signals category (KRESZ 6–7. §): arm signals, stop disc, stop from a moving police vehicle, and flagman.
- Everyday/exam signs A-026, C-006, C-024, C-041, D-005, D-006, D-007, D-011, D-012, E-028, E-029, G-401.

## [2.0.0] — 2026-09-06

Kotlin + Jetpack Compose rewrite of the 2011 Eclipse app (`trafficsignals-e`). Privacy policy: https://lkovari.github.io/KLHome/assets/bigfiles/trafficsignals-privacy-policy.html. Play what’s-new: [docs/play-console/whatsnew.txt](docs/play-console/whatsnew.txt).

### Added

- Material 3 catalog: license gate, nine categories, searchable sign grid, detail with previous/next, About.
- English default strings; Hungarian in `values-hu` when the device locale is Hungarian.
- Sign catalog generated from the Eclipse category lists (355 unique signs).
- Wikimedia Commons Hungarian road-sign SVGs rasterized to 1024px and snapped to SignBlue `#0050A0` / SignRed `#C8102E` / SignYellow `#F5C400`; unmatched road-marking and traffic-light photos keep the original rasters.
- DataStore preference for license acceptance (`trsipr` / `islicenseaccepted`).
- Play listing assets: [docs/icon.png](docs/icon.png) (512×512), [docs/play-console/feature-graphic.png](docs/play-console/feature-graphic.png) (1024×500).
- Bilingual privacy policy that follows the browser locale (Hungarian only when `hu`, otherwise English), with an EN/HU toggle.
- Initial release notes: [docs/RELEASE-NOTES-en.md](docs/RELEASE-NOTES-en.md), [docs/RELEASE-NOTES-hu.md](docs/RELEASE-NOTES-hu.md).

### Changed

- Replaced deprecated `Gallery` and per-category Activities with a single Compose navigation graph.
- Home is a 3×3 category grid. Additional-signs uses a mandatory sign over a time plate; type-of-route uses the yellow main-road diamond with the motorway square.
- Default language fallback is English (the Eclipse app fell back to Hungarian).
- License (Acknowledge) and About fit one phone screen: compact spacing, auto-sized license text, Accept/Refuse always visible.
- About source and privacy policy are tappable labels (full URLs are not shown).
- Copyright line: 2016 – 2026 László Kővári.

### Fixed

- Duplicate gallery entries dropped; commented-out police-arm category still omitted.
- Missing titles that used to show `-` now have EN/HU strings.
- Wrong string bindings from the old `ImagesView` map (sign id now matches the string resource name).
- Category key typo `kategoria_utvonatlipus` corrected to `kategoria_utvonaltipus`.
- Removed `(c) LK` watermarks from catalog diagrams; low-resolution JPEGs replaced with PNG or redrawn KRESZ SVGs.
