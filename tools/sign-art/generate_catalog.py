#!/usr/bin/env python3
import os
import re
import shutil
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path("/Users/kovarilaszlo/src/mobile")
SRC = ROOT / "trafficsignals-e"
DST = ROOT / "trafficsignals"
JAVA_DIR = SRC / "src/com/lkovari/mobile/apps/trafficsignals"
DRAWABLE_DIR = SRC / "res/drawable-ldpi"
EN_XML = SRC / "res/values-en/strings.xml"
HU_XML = SRC / "res/values-hu/strings.xml"
OUT_XXHDPI = DST / "app/src/main/res/drawable-xxhdpi"
OUT_VALUES = DST / "app/src/main/res/values"
OUT_VALUES_HU = DST / "app/src/main/res/values-hu"
OUT_CATALOG = DST / "app/src/main/java/com/lkovari/mobile/apps/trafficsignals/data/SignCatalog.kt"
OUT_CSV = DST / "tools/sign-art/inventory.csv"

CATEGORIES = [
    ("Utvtip.java", "RouteType"),
    ("Elsobseg.java", "Priority"),
    ("Utasitastado.java", "Mandatory"),
    ("Tilalmi.java", "Prohibitory"),
    ("Veszely.java", "Warning"),
    ("Tajekoztatas.java", "Information"),
    ("Kiegeszito.java", "Additional"),
    ("Utburkolat.java", "RoadMarking"),
    ("Fenyjelzo.java", "TrafficLight"),
]

UI_KEYS_EN = {
    "app_name": "Hungarian Traffic Signals",
    "hello": "Welcome to Hungarian Traffic Signals",
    "accept_btn": "Accept",
    "refuse_btn": "Refuse",
    "license": (
        "You acknowledge and agree that DEVELOPER owns all legal right, title and interest in and to the Software, "
        "including any intellectual property rights which subsist in the Software (whether those rights happen to be "
        "registered or not, and wherever in the world those rights may exist). You further acknowledge that the Software "
        "may contain information which is designated confidential by developer and that you shall not disclose such "
        "information without DEVELOPER's prior written consent. YOU EXPRESSLY UNDERSTAND AND AGREE THAT YOUR USE OF THE "
        "SOFTWARE IS AT YOUR SOLE RISK AND THAT THE SOFTWARE IS PROVIDED \"AS IS\" AND \"AS AVAILABLE.\" "
        "Copyright (C) 2011-2026 by László Kővári - DEVELOPER"
    ),
    "menuTitle": "Traffic signs and signals",
    "menu_info": "About",
    "search_signs": "Search signs",
    "search_no_results": "No signs match this search.",
    "sign_detail_title": "Sign",
    "previous_sign": "Previous",
    "next_sign": "Next",
    "about_appname": "Hungarian Traffic Signals",
    "about_description": (
        "Browse Hungarian KRESZ traffic signs by category. Open a category to see every sign in that group, "
        "then tap a sign for a full-size image and description. Descriptions follow the device language: "
        "Hungarian when the locale is Hungarian, English otherwise."
    ),
    "about_author": "Author: László Kőváry",
    "about_artwork": (
        "Replacement sign diagrams are based on Hungarian KRESZ tables and Wikimedia Commons SVG road-sign diagrams. "
        "Original raster artwork is kept where no matching diagram was available."
    ),
    "about_source_label": "Original source",
    "about_source_url": "https://bitbucket.org/laszlokovary/trafficsignals-e/src/master/",
    "about_copyright_prefix": "Copyright",
    "about_copyright_holder": "2016 - 2026 by László Kővári",
    "about_privacy_policy": "Privacy policy",
    "about_privacy_url": "https://lkovari.github.io/KLHome/assets/bigfiles/trafficsignals-privacy-policy.html",
    "kategoria_utvonaltipus": "Type of route signs",
    "kategoria_elsobsegetszabalyozo": "Priority governing signs",
    "kategoria_utasitastado": "Instruction signs",
    "kategoria_tilalmi": "Regulatory signs",
    "kategoria_veszelytjelzo": "Warning signs",
    "kategoria_tajekoztatastado": "Information signs",
    "kategoria_kiegeszito": "Additional signs",
    "kategoria_utburkolatijelek": "Road markings",
    "kategoria_fenyjelzokeszulekek": "Traffic signals",
    "category_sign_count": "%d signs",
}

UI_KEYS_HU = {
    "app_name": "Magyar Közlekedési Jelzések",
    "hello": "Üdvözöllek a közlekedési jelzések alkalmazásban",
    "accept_btn": "Elfogad",
    "refuse_btn": "Elutasít",
    "license": (
        "Ön elismeri és tudomásul veszi, hogy a FEJLESZTŐ a Szoftverrel kapcsolatos minden jog jogosultja, beleértve a "
        "Szoftverrel kapcsolatos szellemi tulajdonjogot is (függetlenül attól, hogy ezeket a jogokat nyilvántartásba "
        "vették-e, illetve függetlenül attól, hogy ezek a jogok a világ mely országában állnak fenn). Továbbá, Ön elismeri, "
        "hogy a Szolgáltatások tartalmazhatnak olyan információkat, amelyeket a fejlesztő bizalmasként jelöl meg és "
        "amelyeket Ön a FEJLESZTŐ előzetes írásbeli engedélye nélkül nem hozhat nyilvánosságra. ÖN TUDOMÁSUL VESZI HOGY "
        "A PROGRAM HASZNÁLATÁT SAJÁT KIZÁRÓLAGOS FELELŐSÉGÉRE TESZI, ÉS ELFOGADJA HOGY A FEJLESZTŐ AZT MINDENKORI "
        "FORMÁJUKBAN BOCSÁJTJA AZ ÖN RENDELKEZÉSÉRE, ÉS A FEJLESZTŐ NEM VÁLLAL RÁ SEMMILYEN SZAVATOSSÁGOT! "
        "Copyright (C) 2011-2026 Minden jog fenntartva Kővári László - FEJLESZTŐ"
    ),
    "menuTitle": "KRESZ táblák és jelzések",
    "menu_info": "Névjegy",
    "search_signs": "Táblák keresése",
    "search_no_results": "Nincs a keresésnek megfelelő tábla.",
    "sign_detail_title": "Tábla",
    "previous_sign": "Előző",
    "next_sign": "Következő",
    "about_appname": "Magyar Közlekedési Jelzések",
    "about_description": (
        "Böngéssze a magyar KRESZ táblákat kategóriák szerint. Egy kategória megnyitása után megjelennek a csoport táblái, "
        "egy táblára koppintva pedig a nagy kép és a leírás. A leírás nyelve a készülék nyelvéhez igazodik: magyar, "
        "ha a locale magyar, egyébként angol."
    ),
    "about_author": "Szerző: Kőváry László",
    "about_artwork": (
        "A csereábrák a magyar KRESZ táblagyűjtemények és a Wikimedia Commons SVG közúti jelzésábrái alapján készültek. "
        "Ahol nem volt megfelelő ábra, az eredeti raszteres kép maradt."
    ),
    "about_source_label": "Eredeti forrás",
    "about_source_url": "https://bitbucket.org/laszlokovary/trafficsignals-e/src/master/",
    "about_copyright_prefix": "Copyright",
    "about_copyright_holder": "2016 - 2026 Kővári László",
    "about_privacy_policy": "Adatvédelmi tájékoztató",
    "about_privacy_url": "https://lkovari.github.io/KLHome/assets/bigfiles/trafficsignals-privacy-policy.html",
    "kategoria_utvonaltipus": "Útvonaltípust jelző táblák",
    "kategoria_elsobsegetszabalyozo": "Elsőbbséget szabályozó táblák",
    "kategoria_utasitastado": "Utasítást adó táblák",
    "kategoria_tilalmi": "Tilalmi táblák",
    "kategoria_veszelytjelzo": "Veszélyt jelző táblák",
    "kategoria_tajekoztatastado": "Tájékoztatást adó táblák",
    "kategoria_kiegeszito": "Kiegészítő táblák",
    "kategoria_utburkolatijelek": "Útburkolati jelek",
    "kategoria_fenyjelzokeszulekek": "Fényjelző készülék",
    "category_sign_count": "%d tábla",
}

STRING_RE = re.compile(r'<string name="([^"]+)">([\s\S]*?)</string>')
DRAWABLE_RE = re.compile(r"^\s*imageids\.add\(new Integer\(R\.drawable\.([a-z0-9_]+)\)", re.MULTILINE)

MISSING_EN = {
    "utasitastado_kotelezohaladasiiranysalakban": "Proceed in the direction indicated by the arrows.",
    "kulonleges_trolibuszmegallohely": "Trolleybus stop",
    "kulonleges_taxiallomas": "Taxi stand",
    "fenyjelzo_uzemenkivuls": "The traffic light is out of service. Priority is given by traffic signs.",
    "veszely_veszelyespadka": "Soft verge",
}

MISSING_HU = {
    "utasitastado_kotelezohaladasiiranysalakban": "Kötelező haladási irány a táblán jelzett nyilak szerint.",
    "kulonleges_trolibuszmegallohely": "Trolibusz megállóhely",
    "kulonleges_taxiallomas": "Taxiállomás",
    "fenyjelzo_uzemenkivuls": "A jelzőlámpa üzemen kívül van. Az áthaladási elsőbbséget a jelzőtáblák határozzák meg.",
    "veszely_veszelyespadka": "Veszélyes padka",
}


def parse_strings(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    result = {}
    for name, value in STRING_RE.findall(text):
        result[name] = value.strip().replace("\\'", "'")
    return result


def parse_ids(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    ids = []
    seen = set()
    for match in DRAWABLE_RE.finditer(text):
        sign_id = match.group(1)
        if sign_id in seen:
            continue
        seen.add(sign_id)
        ids.append(sign_id)
    return ids


def find_image(sign_id: str) -> Path | None:
    for ext in (".png", ".jpg", ".jpeg", ".PNG", ".JPG"):
        candidate = DRAWABLE_DIR / f"{sign_id}{ext}"
        if candidate.exists():
            return candidate
    return None


def xml_string(name: str, value: str) -> str:
    escaped = escape(value).replace("'", r"\'")
    return f'    <string name="{name}">{escaped}</string>\n'


def write_strings(path: Path, ui: dict[str, str], sign_ids: list[str], source: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    used = set()
    with path.open("w", encoding="utf-8") as out:
        out.write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n')
        for key, value in ui.items():
            out.write(xml_string(key, value))
            used.add(key)
        out.write("\n")
        for sign_id in sign_ids:
            if sign_id in used:
                continue
            value = source.get(sign_id, sign_id.replace("_", " "))
            out.write(xml_string(sign_id, value))
            used.add(sign_id)
        out.write("</resources>\n")


def main() -> None:
    en = parse_strings(EN_XML)
    hu = parse_strings(HU_XML)
    en.update(MISSING_EN)
    hu.update(MISSING_HU)
    en["fenyjelzo_zold"] = "Green means go if the way is clear."
    catalog = []
    all_ids = []
    OUT_XXHDPI.mkdir(parents=True, exist_ok=True)

    category_icons = {
        "RouteType": "kategoria_utvonaltipus",
        "Priority": "kategoria_elsobseg",
        "Mandatory": "kategoria_utasitastado",
        "Prohibitory": "kategoria_tilalmi",
        "Warning": "kategoria_veszely",
        "Information": "kategoria_tajekoztato",
        "Additional": "kategoria_kiegeszito",
        "RoadMarking": "kategoria_utburkolati",
        "TrafficLight": "kategoria_fenyjelzo",
    }

    for java_name, category in CATEGORIES:
        ids = parse_ids(JAVA_DIR / java_name)
        for sign_id in ids:
            catalog.append((sign_id, category))
            all_ids.append(sign_id)

    unique_ids = []
    seen_ids = set()
    for sign_id in all_ids:
        if sign_id not in seen_ids:
            unique_ids.append(sign_id)
            seen_ids.add(sign_id)

    copied = 0
    missing_images = []
    for sign_id in unique_ids + list(category_icons.values()):
        src = find_image(sign_id)
        if src is None:
            missing_images.append(sign_id)
            continue
        dest = OUT_XXHDPI / f"{sign_id}{src.suffix.lower()}"
        shutil.copy2(src, dest)
        copied += 1

    write_strings(OUT_VALUES / "strings.xml", UI_KEYS_EN, unique_ids, en)
    write_strings(OUT_VALUES_HU / "strings.xml", UI_KEYS_HU, unique_ids, hu)

    OUT_CATALOG.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "package com.lkovari.mobile.apps.trafficsignals.data",
        "",
        "import com.lkovari.mobile.apps.trafficsignals.R",
        "",
        "object SignCatalog {",
        "    val categories: List<SignCategory> = SignCategory.entries",
        "",
        "    val signs: List<TrafficSign> = listOf(",
    ]
    for sign_id, category in catalog:
        lines.append(
            f"        TrafficSign(id = \"{sign_id}\", category = SignCategory.{category}, "
            f"imageRes = R.drawable.{sign_id}, titleRes = R.string.{sign_id}),"
        )
    lines.append("    )")
    lines.append("")
    lines.append("    fun signsIn(category: SignCategory): List<TrafficSign> =")
    lines.append("        signs.filter { sign -> sign.category == category }")
    lines.append("")
    lines.append("    fun signById(id: String): TrafficSign? =")
    lines.append("        signs.firstOrNull { sign -> sign.id == id }")
    lines.append("")
    lines.append("    fun categoryIconRes(category: SignCategory): Int {")
    lines.append("        return when (category) {")
    for category, icon in category_icons.items():
        lines.append(f"            SignCategory.{category} -> R.drawable.{icon}")
    lines.append("        }")
    lines.append("    }")
    lines.append("")
    lines.append("    fun categoryTitleRes(category: SignCategory): Int {")
    lines.append("        return when (category) {")
    lines.append("            SignCategory.RouteType -> R.string.kategoria_utvonaltipus")
    lines.append("            SignCategory.Priority -> R.string.kategoria_elsobsegetszabalyozo")
    lines.append("            SignCategory.Mandatory -> R.string.kategoria_utasitastado")
    lines.append("            SignCategory.Prohibitory -> R.string.kategoria_tilalmi")
    lines.append("            SignCategory.Warning -> R.string.kategoria_veszelytjelzo")
    lines.append("            SignCategory.Information -> R.string.kategoria_tajekoztatastado")
    lines.append("            SignCategory.Additional -> R.string.kategoria_kiegeszito")
    lines.append("            SignCategory.RoadMarking -> R.string.kategoria_utburkolatijelek")
    lines.append("            SignCategory.TrafficLight -> R.string.kategoria_fenyjelzokeszulekek")
    lines.append("        }")
    lines.append("    }")
    lines.append("}")
    lines.append("")
    OUT_CATALOG.write_text("\n".join(lines), encoding="utf-8")

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8") as csv:
        csv.write("id,category,old_file,hu_title,en_title,kresz_code,wiki_file,status\n")
        for sign_id, category in catalog:
            src = find_image(sign_id)
            old_file = src.name if src else ""
            hu_title = hu.get(sign_id, "").replace('"', "'")
            en_title = en.get(sign_id, "").replace('"', "'")
            status = "original" if src else "missing"
            csv.write(f'{sign_id},{category},{old_file},"{hu_title}","{en_title}",,,{status}\n')

    print(f"signs={len(catalog)} unique={len(unique_ids)} copied={copied} missing={missing_images}")


if __name__ == "__main__":
    main()
