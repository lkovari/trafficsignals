# Changelog

All notable changes to **Hungarian Traffic Signals** (`com.lkovari.mobile.apps.trafficsignals`) are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning matches `versionName` **2.0.0** / `versionCode` **2** (minSdk 24, targetSdk 36).

## [Unreleased]

## [2.0.0] — 2026-09-06

Kotlin + Jetpack Compose rewrite of the 2011 Eclipse app (`trafficsignals-e`). Privacy policy: https://lkovari.github.io/KLHome/assets/bigfiles/trafficsignals-privacy-policy.html. Play what’s-new: [docs/play-console/whatsnew.txt](docs/play-console/whatsnew.txt).

### Added

- Material 3 catalog: license gate, nine categories, searchable sign grid, detail with previous/next, About.
- English default strings; Hungarian in `values-hu` when the device locale is Hungarian.
- Sign catalog generated from the Eclipse category lists (355 unique signs).
- Wikimedia Commons Hungarian road-sign SVGs rasterized to 512px for 232 matched signs; unmatched signs keep the original rasters.
- DataStore preference for license acceptance (`trsipr` / `islicenseaccepted`).
- Play listing assets: [docs/icon.png](docs/icon.png) (512×512), [docs/play-console/feature-graphic.png](docs/play-console/feature-graphic.png) (1024×500).
- Bilingual privacy policy that follows the browser locale (Hungarian only when `hu`, otherwise English), with an EN/HU toggle.
- Initial release notes: [docs/RELEASE-NOTES-en.md](docs/RELEASE-NOTES-en.md), [docs/RELEASE-NOTES-hu.md](docs/RELEASE-NOTES-hu.md).

### Changed

- Replaced deprecated `Gallery` and per-category Activities with a single Compose navigation graph.
- Default language fallback is English (the Eclipse app fell back to Hungarian).
- About credits Wikimedia diagrams and links the original Bitbucket source.
- Copyright line: 2016 – 2026 László Kővári.

### Fixed

- Duplicate gallery entries dropped; commented-out police-arm category still omitted.
- Missing titles that used to show `-` now have EN/HU strings.
- Wrong string bindings from the old `ImagesView` map (sign id now matches the string resource name).
- Category key typo `kategoria_utvonatlipus` corrected to `kategoria_utvonaltipus`.
