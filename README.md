# Hungarian Traffic Signals

Kotlin + Jetpack Compose rewrite of the 2011 Eclipse app (`trafficsignals-e`). Application id `com.lkovari.mobile.apps.trafficsignals`.

**Version:** 2.0.0 (versionCode 2)  
**SDK:** minSdk 24 · targetSdk 36 · compileSdk 36  
**UI:** English by default; Hungarian when the device locale is Hungarian. Material 3.

A catalog of Hungarian KRESZ traffic signs, grouped in nine categories on a 3×3 home grid. Open a category, search, then tap a sign for a full-size image and description. The first-run Acknowledge screen and About fit on one phone screen.

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
./gradlew assembleRelease   # signed APK: app/build/outputs/apk/release/app-release.apk
./gradlew bundleRelease     # Play App Bundle
```

## Artwork

Matched signs use Wikimedia Commons files named `Hungary road sign {KRESZ-code}.svg`, rasterized to 1024px in `drawable-xxhdpi` and snapped to **SignBlue** `#0050A0`, **SignRed** `#C8102E`, and **SignYellow** `#F5C400`. Road markings, traffic-light photos, and unmatched signs keep the original rasters (JPEG originals converted to PNG). Category tiles are vectors except Additional signs (mandatory sign + time plate) and Type of route (main-road diamond + motorway).

Replacement SVGs are attributed to Wikimedia Commons on the About screen.

### `tools/sign-art` Python scripts

These scripts are a **developer-only** artwork pipeline. They are not compiled into the app, not copied into `assets`, and **do not ship in the release APK or Play bundle**. The phone runs only the PNG/XML already under `app/src/main/res/`. `assembleDebug` / `assembleRelease` do not run Python.

**What they were for:** one-time (and repeatable) migration from the 2011 Eclipse catalog (`trafficsignals-e`): copy sign ids and strings into Compose, import the original rasters, then replace as many diagrams as possible with Wikimedia KRESZ SVGs and a shared palette. Low-resolution JPEGs and `(c) KL ☺` watermarks were cleaned or redrawn in the same pass.

**What they are for now:** regenerate or fix catalog images, category tiles, and the launcher icon without editing hundreds of bitmaps by hand. Optional Gradle wrapper: `./gradlew unifySignArt` (venv + Pillow/NumPy; does not run on every build). Cache and `.venv` are gitignored (`tools/sign-art/cache/`, `tools/sign-art/.venv/`).

| Script | Role |
|---|---|
| `generate_catalog.py` | **Was:** import Eclipse Java category lists, EN/HU strings, and ldpi rasters into `SignCatalog.kt`, `values/`, and `drawable-xxhdpi`. **Now:** re-run only if you rebuild the catalog from `trafficsignals-e`. |
| `kresz_map.py` | Sign resource id → KRESZ code (`E-005`, …) used by fetch/unify. |
| `inventory.csv` | Catalog inventory (id, category, file, titles, Wikimedia match). Written by `generate_catalog.py`, read by the other scripts. |
| `fetch_wikimedia.py` | Download `Hungary road sign {code}.svg` from Wikimedia Commons into the local cache. |
| `palette.py` | Shared SignBlue / SignRed / SignYellow, SVG hex snap, 1024px rasterize, write PNG into `drawable-xxhdpi`. |
| `unify_palette.py` | Snap cached SVGs and remaining photos onto the palette; strip watermarks on photo originals. |
| `remove_watermark.py` | Fill the top-left `(c) KL ☺` band on blue (and similar) photo rasters. Used by unify. |
| `redraw_originals.py` | Replace signs that have no usable photo: Wikimedia SVG (e.g. E-005) or drawn composites (plates, P+R, bus-and-cycle lane, …). |
| `render_category_icons.py` | The nine home-grid tiles in `res/drawable/` (seven vectors, two PNG composites). |
| `render_launcher.py` | Launcher foreground / mipmaps and `docs/icon.png` from `launcher.svg`. |
| `launcher.svg` | Source drawing for the launcher, not a Python script. |

Typical regenerate order (needs the sibling `trafficsignals-e` tree only for `generate_catalog.py`):

```bash
python3 tools/sign-art/generate_catalog.py
python3 tools/sign-art/fetch_wikimedia.py
python3 tools/sign-art/unify_palette.py
python3 tools/sign-art/redraw_originals.py
python3 tools/sign-art/render_category_icons.py
python3 tools/sign-art/render_launcher.py
```

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
