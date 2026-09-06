# Claude Code prompt: add missing Hungarian KRESZ signs

Copy everything below the line into Claude Code.

---

You are working in the Android repo `trafficsignals` (Kotlin + Jetpack Compose, application id `com.lkovari.mobile.apps.trafficsignals`). This is an offline catalog of Hungarian KRESZ traffic signs.

## Goal

Close the catalog gaps found by comparing the app against the in-force Hungarian Highway Code (`1/1975. (II. 5.) KPM–BM`) and Wikimedia Commons files named `Hungary road sign {CODE}.svg`.

Read `missing-tables-signs-hu.md` in the repo root first. It is the audit source of truth (Hungarian). This prompt is the implementation brief.

Do **not** implement the 2026 KRESZ draft. Stay on the current KRESZ.

## Current state (audit)

- 355 catalog entries, 234 with a KRESZ code, 9 categories.
- Wikimedia Commons has ~395 unique current Hungarian codes. **162 coded signs are missing** from the app.
- Priority series **B-001…B-006 is complete**.
- The entire **police / officer signals** set is missing. KRESZ §6 overrides signs and lights. There is **no** Commons `Hungary road sign` SVG series for these. §7 flagman/disc is only partly covered (`H-021` plus some railway composites).
- Many app entries are composites (main sign + additional panel in one raster). Commons stores those as separate H-codes. Do not treat composites as missing if the meaning is already in the catalog.

Sources:

- KRESZ: https://net.jogtar.hu/jogszabaly?docid=97500001.KPM
- Wikipedia: https://en.wikipedia.org/wiki/Road_signs_in_Hungary
- Commons by number: https://commons.wikimedia.org/wiki/Category:Road_signs_of_Hungary_by_number
- Official diagrams: https://ume.kozut.hu/p/kresz-tablak-jelzeskepei
- Police arm signals (text): https://edukresz.hu/rendori-karjelzesek/
- Police figures 1–5: https://epa.oszk.hu/05200/05238/00002/pdf/EPA05238_belugyi_2014_11_069-082.pdf

## How this app stores signs

Follow existing patterns. Do not invent a parallel catalog.

| Piece | Path |
|---|---|
| Category enum | `app/src/main/java/com/lkovari/mobile/apps/trafficsignals/data/TrafficSign.kt` |
| Catalog list | `app/src/main/java/.../data/SignCatalog.kt` |
| EN strings (default) | `app/src/main/res/values/strings.xml` — string `name` equals sign `id` |
| HU strings | `app/src/main/res/values-hu/strings.xml` |
| Artwork | `app/src/main/res/drawable-xxhdpi/{id}.png` |
| Inventory | `tools/sign-art/inventory.csv` |
| Code map | `tools/sign-art/kresz_map.py` (`ID_TO_CODE`) |
| Fetch SVGs | `tools/sign-art/fetch_wikimedia.py` |
| Category tile icons | `tools/sign-art/render_category_icons.py` |
| Tests | `app/src/test/java/.../SignCatalogTest.kt` |

Sign id convention: `{prefix}_{ascii_slug}`, lowercase, no hyphens. Prefixes already in use: `utvonaltipus_`, `elsobseg_`, `utasitastado_`, `tilalmi_`, `veszely_`, `tajekoztato_`, `kulonleges_`, `kiegeszito_`, `utburkolat_`, `fenyjelzo_`. For police use a new prefix `rendori_`.

Each new sign needs **all** of: unique id, `SignCatalog` entry, EN title, HU title, drawable, inventory.csv row, `kresz_map.py` entry when a code exists. Then fetch/rasterize Wikimedia artwork where a file exists.

Place new signs in the matching existing category (Warning, Prohibitory, Mandatory, Information, Additional, TrafficLight, RoadMarking). Police signals get a **new** `SignCategory`.

## Constraints

- Do not add comments in source code.
- Do not use type assertions.
- Keep EN in `values/strings.xml` and HU in `values-hu/strings.xml`. No in-app language switcher.
- Do not commit secrets. Do not change git config. Do not commit unless asked.
- Wikimedia Commons is rate-limited (HTTP 429). Use the existing User-Agent in `fetch_wikimedia.py`, sleep between downloads, retry with backoff. Prefer thumbnail/original URLs already returned by the Commons API. Do not hammer upload.wikimedia.org.
- Hungarian road-sign SVGs are public domain under Hungarian copyright law (legal/official works). Keep About-screen attribution as-is unless you add a new artwork source for police drawings.
- Do not regenerate the whole catalog from the Eclipse app (`generate_catalog.py` overwrites from `trafficsignals-e`). Add entries by hand (or a small additive script).
- After adding signs, update `SignCatalogTest` counts. Today they are locked to the 2011 catalog (9 categories, 355 signs).
- After palette/icon work, run the existing sign-art scripts if you touch artwork (`unify_palette.py`, `render_category_icons.py`) so category tiles stay consistent.

## Implementation order

Ship in phases. Finish a phase so the app compiles and tests pass before starting the next.

### Phase 1 — P1 everyday / exam signs (Wikimedia)

Add these as first-class catalog entries. Fetch `Hungary road sign {CODE}.svg`, rasterize to 1024px PNG with `rsvg-convert` (same as `fetch_wikimedia.py`), write to `drawable-xxhdpi`.

**Warning**

| Code | Suggested id | EN title (short) | Commons |
|---|---|---|---|
| A-026 | `veszely_fenyjelzokeszulek` | Traffic signals ahead | https://commons.wikimedia.org/wiki/File:Hungary_road_sign_A-026.svg |
| A-046 | `veszely_vasutiatjaroelojelzo1j` | Level-crossing countdown, right, 150 m | https://commons.wikimedia.org/wiki/File:Hungary_road_sign_A-046.svg |
| A-048 | `veszely_vasutiatjaroelojelzo2j` | Level-crossing countdown, right, 100 m | https://commons.wikimedia.org/wiki/File:Hungary_road_sign_A-048.svg |
| A-050 | `veszely_vasutiatjaroelojelzo3j` | Level-crossing countdown, right, 50 m | https://commons.wikimedia.org/wiki/File:Hungary_road_sign_A-050.svg |
| A-043 | `veszely_vasutiatjarokezdete1j` | Railroad crossbuck, single track (mirror) | https://commons.wikimedia.org/wiki/File:Hungary_road_sign_A-043.svg |
| A-044 | `veszely_vasutiatjarokezdete2j` | Railroad crossbuck, multiple tracks (mirror) | https://commons.wikimedia.org/wiki/File:Hungary_road_sign_A-044.svg |

HU titles: match official KRESZ wording (veszélyt jelző táblák). A-026 = „Forgalomirányító fényjelző készülék”.

**Prohibitory**

| Code | Suggested id | EN title | Commons |
|---|---|---|---|
| C-006 | `tilalmi_segedmotorossalbehajtanitilos` | No mopeds | https://commons.wikimedia.org/wiki/File:Hungary_road_sign_C-006.svg |
| C-024 | `tilalmi_tengelyterheleskorlatozas` | Axle weight limit | https://commons.wikimedia.org/wiki/File:Hungary_road_sign_C-024.svg |
| C-011 | `tilalmi_jelzettjarmuvekkelbehajtanitilos` | No entry for vehicles shown | https://commons.wikimedia.org/wiki/File:Hungary_road_sign_C-011.svg |
| C-041 | `tilalmi_kotelezomegallasrendorseg` | Mandatory stop — police | https://commons.wikimedia.org/wiki/File:Hungary_road_sign_C-041.svg |
| C-040 | `tilalmi_kotelezomegallaskomp` | Mandatory stop — ferry | https://commons.wikimedia.org/wiki/File:Hungary_road_sign_C-040.svg |
| C-049 | `tilalmi_dijfizeteselorejelzese` | Toll / charge ahead | https://commons.wikimedia.org/wiki/File:Hungary_road_sign_C-049.svg |

HU: C-006 = „Segédmotoros kerékpárral behajtani tilos”; C-024 = „Tengelyterhelés-korlátozás”; C-041 = „Kötelező megállás RENDŐRSÉG”.

**Mandatory** (`kresz_map.py` already maps D-005 to `utasitastado_kotelezohaladasiiranyjobbraesegyenesen` but that id is **not** in the catalog — add the sign, reuse that id if you keep the map.)

| Code | Suggested id | EN title | Commons |
|---|---|---|---|
| D-005 | `utasitastado_kotelezohaladasiiranyjobbraesegyenesen` | Proceed ahead or right | https://commons.wikimedia.org/wiki/File:Hungary_road_sign_D-005.svg |
| D-006 | `utasitastado_kotelezohaladasiiranyjobbraelore` | Turn right ahead | https://commons.wikimedia.org/wiki/File:Hungary_road_sign_D-006.svg |
| D-007 | `utasitastado_kotelezohaladasiiranybalraelore` | Turn left ahead | https://commons.wikimedia.org/wiki/File:Hungary_road_sign_D-007.svg |
| D-011 | `utasitastado_kotelezohaladasiiranyharomirany` | Ahead, left or right | https://commons.wikimedia.org/wiki/File:Hungary_road_sign_D-011.svg |
| D-012 | `utasitastado_kotelezomegfordulas` | U-turn only | https://commons.wikimedia.org/wiki/File:Hungary_road_sign_D-012.svg |
| D-031 | `utasitastado_gyalogkerekparutosztottforditott` | Separated pedestrian/cycle path (swapped sides) | https://commons.wikimedia.org/wiki/File:Hungary_road_sign_D-031.svg |
| D-032 | `utasitastado_gyalogkerekparutosztottforditottvege` | End of swapped separated path | https://commons.wikimedia.org/wiki/File:Hungary_road_sign_D-032.svg |

**Information / special regulations**

| Code | Suggested id | EN title | Commons |
|---|---|---|---|
| E-028 | `kulonleges_korlatozottsebesseguovezet` | Maximum speed zone | https://commons.wikimedia.org/wiki/File:Hungary_road_sign_E-028.svg |
| E-029 | `kulonleges_korlatozottsebesseguovezetvege` | End of maximum speed zone | https://commons.wikimedia.org/wiki/File:Hungary_road_sign_E-029.svg |
| E-030 | `kulonleges_korlatozottforgalmuovezet` | Limited traffic zone (weight) | https://commons.wikimedia.org/wiki/File:Hungary_road_sign_E-030.svg |
| E-031 | `kulonleges_korlatozottforgalmuovezetvege` | End of limited traffic zone | https://commons.wikimedia.org/wiki/File:Hungary_road_sign_E-031.svg |
| E-007 | `tajekoztato_autobuszforgalmisavvege` | End of bus lane | https://commons.wikimedia.org/wiki/File:Hungary_road_sign_E-007.svg |
| E-005 | `tajekoztato_autobuszeskerekparsav` | Bus and bicycle lane | https://commons.wikimedia.org/wiki/File:Hungary_road_sign_E-005.svg |
| G-401 | `tajekoztato_altalanossebesseghatarok` | National default speed limits | https://commons.wikimedia.org/wiki/File:Hungary_road_sign_G-401.svg |

Note: the app already has `utasitastado_autobuszsavvege` without a code. Prefer wiring **E-007** to a new information-category id (or map the existing id to E-007 and replace its artwork). Do not leave two “end of bus lane” entries with the same meaning.

HU for E-028/E-029: „Korlátozott sebességű övezet” / „… vége” (KRESZ figures 53/a, 53/b). These are the highest-value missing street signs (zone 30).

### Phase 2 — Police signals (P0), new category

Add `SignCategory.Police` (or `OfficerSignals`) to the enum. Wire:

- `SignCatalog.categories` (enum entries order controls the home grid)
- `categoryIconRes` / `categoryTitleRes`
- EN/HU strings `kategoria_rendori` — EN: “Police signals”, HU: “Rendőri jelzések”
- Category tile in `render_category_icons.py` (officer + red-and-white disc, same 512 canvas and palette as other tiles)
- `SignCatalogTest.nineCategories` → 10 categories; add a count assertion for the new category
- Navigation already uses `category.name`; a new enum value should work without NavHost changes

There are **no** Commons SVGs. Draw simple, readable educational diagrams (vector → PNG) in the app palette (`tools/sign-art/palette.py`: SIGN_RED, SIGN_BLUE, WHITE, BLACK, ASPHALT). Do not paste copyrighted textbook photos. Match KRESZ §6 meaning, not decorative realism.

Required entries:

| Suggested id | KRESZ | What to draw | EN / HU meaning |
|---|---|---|---|
| `rendori_karokoldalra` | §6 (1) a) | Officer, both arms out. Label or small arrows: parallel = go, perpendicular = stop. | Arms outstretched: go from the sides, stop from front/back |
| `rendori_karfuggoleges` | §6 (1) b) | One arm vertical. | Change of direction (like amber / red-amber) |
| `rendori_balramogott` | §6 (1) c) | Right arm beckoning back, left palm toward left-hand traffic. | Right-hand traffic may go; left turn **behind** the officer |
| `rendori_balraelott` | §6 (1) d) | Right arm horizontal forward, left arm beckoning. | Left-hand traffic may go; left turn **in front of** the officer |
| `rendori_alapallas` | §6 (1) e) | Arms at sides. Same go/stop as (a). | Rest stance |
| `rendori_gyorsitas` | §6 (1) f) first | Arm beckoning toward body. | Speed up |
| `rendori_lassitas` | §6 (1) f) second | Arm pumping up and down. | Slow down |
| `rendori_megallitotarcsa` | §6 (2) a) aa) | White-rimmed **red disc**, optionally raised arm / whistle. | Stop for a standing officer (also public-space warden, §6 (5)) |
| `rendori_megallitasjarmubol` | §6 (2) a) ab) | Patrol car/motorcycle, flashing lights, disc or lamp moved up and down. | Stop for a moving police vehicle |
| `rendori_jelzoor` | §7 (1) | Red disc or red lamp held / on a stand. | Stop for a flagman / civil-guard flagman |

HU descriptions should track the statute, not slang. Mention that officer signals override signs and lights (§6 (3)). Mention §6 (4) other entitled persons (military traffic regulator, disaster management, customs, fire, transport authority inspector) on the disc/stop entries, not as extra drawings unless you have spare slots.

### Phase 3 — P2 common coded signs

Add Wikimedia entries (same pipeline as Phase 1):

**Lanes / parking (E):** E-001, E-002, E-003, E-004, E-010, E-011, E-014, E-015, E-047, E-048, E-060.

The app already has uncoded `kulonleges_forgalmisavoklegkisebbsebessege` and `kulonleges_besorolasirend3`. Either bind those ids to E-001 / E-014 and replace artwork, or add coded siblings and keep the composites. Prefer **one meaning → one entry**.

**Facilities (F):** F-030 Police, F-031 Traffic control, F-026–F-028 vertical chevrons, F-035–F-036 narrow chevrons. Uncoded `tajekoztato_terelotabla` may map to a chevron.

**Direction (G):** G-004 end of recommended speed (G-003 is already in the app), G-306, G-307, G-308 pedestrian over/underpass variants, G-312, G-313 side-street dead end, G-351 motorway exit, G-205 EU border. Skip G-202 (obsolete county border) unless you mark it obsolete in the title.

**Additional (H) — add the useful ones, not all 86:**

Must-have: H-002…H-010 (priority-road diagrams; app only has H-001), H-011 STOP distance, H-013–H-015 time/day, H-017–H-020 distance/extent, H-025 frogs, H-104 speed hump (uncoded `kiegeszito_fekvorendor` exists), H-115 two-way bicycle traffic, H-112/H-113 cycle priority variants, H-040/H-042–H-046 sidewalk parking mirrors, H-063/H-065/H-066 plus a representative “except” set (H-083 permission, H-099 disabled, H-084 cars).

Full missing H list is in `missing-tables-signs-hu.md`. Do not dump every vehicle pictogram in one PR if the APK size balloons; batch remaining H/I codes later.

### Phase 4 — Traffic lights and road markings

App has 16 lights and 26 markings, mostly original rasters.

Add TrafficLight entries (simple diagrams, not photos unless you already have rights):

- Lane-use: red X, green downward arrow, flashing amber diagonal arrow — KRESZ §9 (1) e) and (8)
- Cycle signals: three-aspect lamp with bicycle symbols — §9 (1) b)
- Tram / emergency two-lamp head as a device type — §9 (1) c) (red over amber). The app already has some flashing-amber / red photos; add a labelled device plate if those photos are ambiguous.

Add RoadMarking entries:

- Yellow solid line = no stopping
- Yellow broken line = no waiting/parking
- BUS lane wordmark
- Double broken barrier line on reversible-lane sections

### Phase 5 — Low priority (only if Phases 1–2 are done)

- Tourist I-001, I-004, I-025, I-031, I-032, I-034, I-037, I-040, I-044 (app already has I-005, I-026, I-045)
- Obsolete multilingual customs STOP C-035…C-039 (same as C-034, other scripts). Skip unless you want exam completeness.
- G-076…G-079, G-106, G-653, G-654 direction templates (city names vary). App already has uncoded direction rasters.
- A-021a (stacked children variant) — skip; A-021 is enough.

## Suggested add-sign workflow

1. Pick a phase-1 code.
2. Add `ID_TO_CODE` in `kresz_map.py`.
3. Append `inventory.csv` (`status` empty until fetch).
4. Add EN + HU strings (`name` = id). Titles are the educational description shown on the detail screen; keep them one or two sentences, same tone as existing strings.
5. Add `TrafficSign(...)` in `SignCatalog.kt` next to siblings in that category (not dumped at the end of the file unless that category already ends there).
6. Run `python3 tools/sign-art/fetch_wikimedia.py` (or a targeted fetch) so the PNG lands in `drawable-xxhdpi`.
7. If you add a category, extend enum, strings, icon renderer, tests.
8. Update `SignCatalogTest` unique ids, per-category counts, total count, and string-key coverage.
9. `./gradlew test` and `./gradlew assembleDebug`.

## Acceptance

- Phase 1 signs appear in the correct category grid, search, and detail screen in both EN and HU.
- Artwork is the Commons Hungarian SVG where a file exists, rasterized like existing wikimedia rows.
- Police category is on the home grid; all §6 (1) a–f plus disc, moving stop, and §7 flagman are present with EN+HU explanations.
- Tests updated and passing.
- No duplicate meanings for E-007 vs existing bus-lane-end.
- APK still offline: no network calls from app code.

When a phase is done, stop and summarize: ids added, files changed, remaining phases.
