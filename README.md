# Hungarian Traffic Signals

Kotlin + Jetpack Compose rewrite of the 2011 Eclipse app (`trafficsignals-e`). Application id `com.lkovari.mobile.apps.trafficsignals`.

**Version:** 2.0.0 (versionCode 2)  
**SDK:** minSdk 24 · targetSdk 36 · compileSdk 36  
**UI:** English by default; Hungarian when the device locale is Hungarian. Material 3.

A catalog of Hungarian KRESZ traffic signs, grouped in nine categories. Open a category, search, then tap a sign for a full-size image and description.

**Privacy policy:** https://lkovari.github.io/KLHome/assets/bigfiles/trafficsignals-privacy-policy.html — Hungarian when the browser locale is Hungarian, English otherwise (EN/HU toggle on the page). Source: [docs/privacy-policy.html](docs/privacy-policy.html).

---

## Open in Android Studio

1. File → Open → this `trafficsignals` folder.
2. Let Gradle sync (AGP 9.2.1, Gradle 9.4.1, Kotlin 2.2.10).
3. Run the `app` configuration on an emulator or device.

## Locale

- `app/src/main/res/values/strings.xml` is English (default for every non-Hungarian locale).
- `app/src/main/res/values-hu/strings.xml` is Hungarian.
- There is no in-app language switcher.

## Release signing

Copy `keystore.properties` from `sensors-s` (same EKL upload key, alias `ekldroidapps`). The file is gitignored.

```bash
./gradlew bundleRelease
```

## Artwork

Sign diagrams are replaced from Wikimedia Commons files named `Hungary road sign {KRESZ-code}.svg` where a match exists. Road markings, traffic-light photos, and unmatched signs keep the original rasters.

Regenerate the catalog from the Eclipse sources, then fetch replacements:

```bash
python3 tools/sign-art/generate_catalog.py
python3 tools/sign-art/fetch_wikimedia.py
```

Replacement SVGs are attributed to Wikimedia Commons on the About screen.

---

## Documents

| Document | What it is |
|---|---|
| [CHANGELOG.md](CHANGELOG.md) | Version history |
| [docs/privacy-policy.html](docs/privacy-policy.html) | Privacy policy source (locale: Hungarian if `hu`, otherwise English). Live: https://lkovari.github.io/KLHome/assets/bigfiles/trafficsignals-privacy-policy.html |
| [docs/play-console/privacy-policy.html](docs/play-console/privacy-policy.html) | Same policy, Play Console folder |
| [docs/RELEASE-NOTES-en.md](docs/RELEASE-NOTES-en.md) | Initial release notes (English) |
| [docs/RELEASE-NOTES-hu.md](docs/RELEASE-NOTES-hu.md) | Kezdeti kiadási megjegyzések (magyar) |
| [docs/play-console/whatsnew.txt](docs/play-console/whatsnew.txt) | Play Console EN/HU what’s-new |
| [docs/icon.png](docs/icon.png) | Play high-res icon (512×512) |
| [docs/feature-graphic.png](docs/feature-graphic.png) | Play feature graphic (1024×500) |
| [docs/play-console/feature-graphic.png](docs/play-console/feature-graphic.png) | Same feature graphic for the Play Console folder |
