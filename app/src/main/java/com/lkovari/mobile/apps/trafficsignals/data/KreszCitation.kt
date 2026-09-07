package com.lkovari.mobile.apps.trafficsignals.data

object KreszCitation {
    fun forId(id: String): String = when (id) {
        "rendori_karokoldalra" -> "6. § (1) a)"
        "rendori_karfuggoleges" -> "6. § (1) b)"
        "rendori_balramogott" -> "6. § (1) c)"
        "rendori_balraelott" -> "6. § (1) d)"
        "rendori_alapallas" -> "6. § (1) e)"
        "rendori_gyorsitas", "rendori_lassitas" -> "6. § (1) f)"
        "rendori_megallitotarcsa" -> "6. § (2) a) aa)"
        "rendori_megallitasjarmubol" -> "6. § (2) a) ab)"
        "rendori_jelzoor" -> "7. § (1)"

        "utvonaltipus_autopalyakezdete" -> "11. § (1) a)"
        "utvonaltipus_autopalyavege" -> "11. § (1) b)"
        "utvonaltipus_autoutkezdete" -> "11. § (1) c)"
        "utvonaltipus_autoutvege" -> "11. § (1) d)"
        "utvonaltipus_foutvonalkezdete" -> "11. § (1) e)"
        "utvonaltipus_foutvonalvege" -> "11. § (1) f)"
        "utvonaltipus_foutvonalegyenestolelter" -> "11. § (2)"
        "utvonaltipus_foutvonalvegeelorejelzese" -> "11. § (3)"

        "elsobseg_elsobsegadaskotelezo",
        "elsobseg_elsobsegadaskotelezovastag",
        "elsobseg_elsobsegadaskotelezobicikli" -> "12. § (1) a)"
        "elsobseg_alljelsobsegadaskotelezo",
        "elsobseg_alljelsobsegadaskotelezovastag" -> "12. § (1) b)"
        "elsobseg_szembejovoforgalomelsobsege" -> "12. § (1) c)"
        "elsobseg_elsobsegaszembejovoforgalommalszemben" -> "12. § (1) d)"
        "elsobseg_elsobsegadaskotelezoelorejelzes" -> "12. § (2)"
        "elsobseg_alljelsobsegadaskotelezoelorejelzes" -> "12. § (3)"

        "utasitastado_kotelezohaladasiiranyegyenesen",
        "utasitastado_kotelezohaladasiiranybalra",
        "utasitastado_kotelezohaladasiiranybalra1",
        "utasitastado_kotelezohaladasiiranybalravissza",
        "utasitastado_kotelezomegfordulas",
        "utasitastado_kotelezohaladasiiranybalraesegyenesen",
        "utasitastado_kotelezohaladasiiranyjobbraesegyenesen",
        "utasitastado_kotelezohaladasiiranybalraesjobbra",
        "utasitastado_kotelezohaladasiiranyharomirany",
        "utasitastado_kotelezohaladasiiranyjobbra",
        "utasitastado_kotelezohaladasiiranyjobbra1",
        "utasitastado_kotelezohaladasiiranyjobbraelore",
        "utasitastado_kotelezohaladasiiranybalraelore",
        "utasitastado_kotelezohaladasiiranysalakban" -> "13. § (1) a)"
        "utasitastado_kerekparjelzettiranybanhaladhat",
        "utasitastado_autobuszjelzettiranybanhaladhat" -> "13. § (1) a)"
        "utasitastado_kotelezohaladasiiranyveszelyesanyagotszallitojarmureszereb",
        "utasitastado_kotelezohaladasiiranyveszelyesanyagotszallitojarmureszere",
        "utasitastado_kotelezohaladasiiranyveszelyesanyagotszallitojarmureszerej" -> "13. § (1) a/1."
        "utasitastado_kikerulesiiranybalra",
        "utasitastado_kikerulesiiranyjobbra",
        "utasitastado_kikerulesiiranybalrajobbra" -> "13. § (1) b)"
        "utasitastado_korforgalom" -> "13. § (1) c)"
        "utasitastado_kotelezolegkisebbsebesseg" -> "13. § (1) d)"
        "utasitastado_kotelezolegkisebbsebessegvege" -> "13. § (1) d)"
        "utasitastado_kerekparut" -> "13. § (1) e)"
        "utasitastado_kerekparutvege" -> "13. § (1) f)"
        "utasitastado_gyalogut",
        "utasitastado_gyalogut69" -> "13. § (1) g)"
        "utasitastado_gyalogutvege" -> "13. § (1) h)"
        "utasitastado_gyalogkerekparut",
        "utasitastado_gyalogkerekparut919",
        "utasitastado_gyalogkerekparutosztott",
        "utasitastado_gyalogkerekparutosztottforditott" -> "13. § (1) i)"
        "utasitastado_gyalogkerekparutvege",
        "utasitastado_gyalogkerekparutosztottvege",
        "utasitastado_gyalogkerekparutosztottforditottvege" -> "13. § (1) j)"
        "utasitastado_gyalogosovezet" -> "13. § (1) g/1."
        "utasitastado_gyalogosovezetvege" -> "13. § (1) h/1."
        "kulonleges_gyalogoskerekparosovezet" -> "13. § (1) i/1."
        "kulonleges_gyalogoskerekparosovezetvege" -> "13. § (1) j/1."
        "utasitastado_holanchasznalatakotelezo" -> "13. § (1) k)"
        "utasitastado_holanchasznalatakotelezovege" -> "13. § (1) k/1."
        "utasitastado_autobuszsav",
        "utasitastado_autobuszsavvege" -> "17. § (1) g)"

        "tilalmi_jobbrabekanyarodnitilos" -> "14. § (1) a)"
        "tilalmi_balrabekanyarodnitilos" -> "14. § (1) b)"
        "tilalmi_megfordulnitilos" -> "14. § (1) c)"
        "tilalmi_sebessegkorlatozas30" -> "14. § (1) d)"
        "tilalmi_legkisebbkovetesitavolsag",
        "tilalmi_legkisebbkovetesitavolsag1" -> "14. § (1) e)"
        "tilalmi_eloznitilos" -> "14. § (1) f)"
        "tilalmi_tehergepkocsivaleloznitilos",
        "tilalmi_tehergepkocsivaleloznitilos75" -> "14. § (1) g)"
        "tilalmi_kotelezomegallasvamcustoms",
        "tilalmi_kotelezomegallasrendorseg",
        "tilalmi_kotelezomegallaskomp",
        "tilalmi_dijfizeteselorejelzese" -> "14. § (1) h)"
        "tilalmi_szelessegkorlatozas2m" -> "14. § (1) i)"
        "tilalmi_magassagkorlatozas36m" -> "14. § (1) j)"
        "tilalmi_hosszusagkorlatozas" -> "14. § (1) k)"
        "tilalmi_ossztomegkorlatozas55t" -> "14. § (1) l)"
        "tilalmi_tengelyterheleskorlatozas" -> "14. § (1) m)"
        "tilalmi_mindketiranybolbehajtanitilos" -> "14. § (1) n)"
        "tilalmi_gepjarmuvelmgvlassujbehajtanitilos" -> "14. § (1) o)"
        "tilalmi_motorkerekparralbehajtanitilos" -> "14. § (1) p)"
        "tilalmi_autobusszalbehajtanitilos" -> "14. § (1) q)"
        "tilalmi_tehergepkocsivalbehajtanitilos",
        "tilalmi_tehergepkocsivalbehajtanitilos10t",
        "tilalmi_tehergepkocsivalbehajtanitilos35t" -> "14. § (1) r)"
        "tilalmi_mgvontatovalbehajtanitilos" -> "14. § (1) s)"
        "tilalmi_jarmuszerelvennyelbehajtanitilos",
        "tilalmi_potkocsivalbehajtanitilos5t" -> "14. § (1) t)"
        "tilalmi_segedmotorossalbehajtanitilos" -> "14. § (1) u)"
        "tilalmi_kerekparralbehajtanitilos" -> "14. § (1) v)"
        "tilalmi_kezikocsivalbemennitilos" -> "14. § (1) w)"
        "tilalmi_lovaskocsivallbehajtanitilos" -> "14. § (1) x)"
        "tilalmi_veszelyesanyagotszalljarmuvelbehajtanitilos",
        "tilalmi_vizszennyezoanyagotszallitojarmuvelbehajtanitilos",
        "tilalmi_robbanotuzveszanyszalljarmuvelbehajtanitilos" -> "14. § (1) y)"
        "tilalmi_behajtanitilos" -> "14. § (1) z)"
        "tilalmi_kornyezetvedelmiovezet",
        "tilalmi_kornyezetvedelmiovezetkek",
        "tilalmi_kornyezetvedelmiovezetvege" -> "14. § (1) z/3."
        "tilalmi_jelzettjarmuvekkelbehajtanitilos",
        "tilalmi_mgvbiciklilovaskocsivalbehajtanitilos",
        "tilalmi_motorkerekparraszgkvalbehajtanitilos" -> "14. § (2)"
        "tilalmi_sebessegkorlatozasvege",
        "tilalmi_elozesitilalomvege",
        "tilalmi_tehergepkocsivaleloznitilovege",
        "tilalmi_tilalmakvege" -> "14. § (7)"
        "tilalmi_gyalogoskozlekedesetilos" -> "14. §"
        "tilalmi_megallnitilos" -> "15. § (1) a)"
        "tilalmi_varakoznitilos" -> "15. § (1) b)"

        "veszely_veszelyesutkanyarulatbal",
        "veszely_veszelyesutkanyarulatbal100",
        "veszely_veszelyesutkanyarulatjobb" -> "16. § (1) a)"
        "veszely_veszelyesutkanyarulatokbaljobb",
        "veszely_veszelyesutkanyarulatokjobbbal" -> "16. § (1) b)"
        "veszely_veszelyeslejto",
        "veszely_emelkedo" -> "16. § (1) c)"
        "veszely_utszukuletb",
        "veszely_utszukuletj",
        "veszely_utszukuletjb" -> "16. § (1) d)"
        "veszely_szembejovoforgalom" -> "16. § (1) e)"
        "veszely_kompatkelesnyithatohid" -> "16. § (1) f)"
        "veszely_rakpartmeredekpart",
        "veszely_rakpartmeredekpartj" -> "16. § (1) g)"
        "veszely_bukkano" -> "16. § (1) h)"
        "veszely_egyenetlenuttest",
        "veszely_egyenetlenuttest50" -> "16. § (1) i)"
        "veszely_csuszosuttest" -> "16. § (1) j)"
        "veszely_kavicsfelverodes" -> "16. § (1) k)"
        "veszely_koomlas",
        "veszely_koomlasj" -> "16. § (1) l)"
        "veszely_utonfolyomunkak" -> "16. § (1) m)"
        "veszely_melyrepules" -> "16. § (1) n)"
        "veszely_oldalszel" -> "16. § (1) o)"
        "veszely_gyalogosatkeles" -> "16. § (1) p)"
        "veszely_gyermekek" -> "16. § (1) q)"
        "veszely_haziallatok",
        "veszely_szabadoneloallatok" -> "16. § (1) r)"
        "veszely_fenyjelzokeszulek" -> "16. § (1) s)"
        "veszely_egyenranguutakkeresztezodese" -> "16. § (1) t)"
        "veszely_utkeresztezodesalarendeltuttal1",
        "veszely_utkeresztezodesalarendeltuttal2",
        "veszely_utkeresztezodesalarendeltuttal3",
        "veszely_utkeresztezodesalarendeltuttal4",
        "veszely_utkeresztezodesalarendeltuttal5",
        "veszely_utkeresztezodesalarendeltuttal6",
        "veszely_utkeresztezodesalarendeltuttal7",
        "veszely_utkeresztezodesalarendeltuttal8",
        "veszely_utkeresztezodesalarendeltuttal9",
        "veszely_utkeresztezodesalarendeltuttal10" -> "16. § (1) u)"
        "veszely_vasutiatkelosoromponelkul",
        "veszely_vasutiatkelofenysorompoval",
        "veszely_fenysorompovalbiztositottatkelo" -> "16. § (1) v)"
        "veszely_vasutiatkelosorompo" -> "16. § (1) x)"
        "veszely_villamos" -> "16. § (1) y)"
        "veszely_egyebveszely",
        "veszely_jelzoorrelbiztositottatkelo",
        "veszely_vasutiatkelojelzoorrel",
        "veszely_jardaszigetnelkulivillamosmegallo" -> "16. § (1) z)"
        "veszely_gyalogosok" -> "16. § (1) z/1."
        "veszely_kerekparosok",
        "veszely_utatkeresztezokerekparut" -> "16. § (1) z/2."
        "veszely_utzar" -> "16. § (1) z/4."
        "veszely_korforgalomelorejelzese" -> "16. § (1) z/5."
        "veszely_forgalmitorlodas" -> "16. § (1) z/6."
        "veszely_vasutiatjarokezdete1",
        "veszely_vasutiatjarokezdete1j",
        "veszely_vasutiatjarokezdete1a",
        "veszely_vasutiatjarokezdete2",
        "veszely_vasutiatjarokezdete2j",
        "veszely_vasutiatjarokezdete2a" -> "16. § (4) a)"
        "veszely_vasutiatjaroelojelzo1",
        "veszely_vasutiatjaroelojelzo1j",
        "veszely_vasutiatjaroelojelzo2",
        "veszely_vasutiatjaroelojelzo2j",
        "veszely_vasutiatjaroelojelzo3",
        "veszely_vasutiatjaroelojelzo3j" -> "16. § (4) b)"
        "veszely_fenysorompo_szabad" -> "19. § (8) a)"
        "veszely_fenysorompo_tilos" -> "19. § (6) a)"
        "veszely_fenysorompo_uzemenkivul" -> "19. § (7) a)"

        "kulonleges_gyalogosatkelohely" -> "17. § (1) a)"
        "tajekoztato_gyalogosalulvagyfeluljaro" -> "17. § (1) a/1."
        "tajekoztato_alagutkezdete" -> "17. § (1) a/2."
        "tajekoztato_alagutvege" -> "17. § (1) a/3."
        "kulonleges_egyiranyuforgalmuut1",
        "kulonleges_egyiranyuforgalmuut2",
        "tajekoztato_egyiranyuforgaluutkivevebusz",
        "tajekoztato_egyiranyuforgalmuutkivevekerekpar" -> "17. § (1) b)"
        "tajekoztato_zsakutca",
        "tajekoztato_zsakutcaoldalsoutcabal",
        "tajekoztato_zsakutcaoldalsoutcajobb" -> "17. § (1) c)"
        "tajekoztato_zsakutcakerekparostovabbhaladasilehetoseggel" -> "17. § (1) c/1."
        "kulonleges_autobuszmegallohely",
        "kulonleges_trolibuszmegallohely",
        "kulonleges_villamosmegallohely" -> "17. § (1) d)"
        "kulonleges_taxiallomas" -> "17. § (1) d/1."
        "tajekoztato_maganut" -> "17. § (1) d/2."
        "kulonleges_parkolo",
        "kulonleges_parkolohaz",
        "kulonleges_parkoloamegjeloltjarmunek",
        "kulonleges_parkoloelorejelzes",
        "kulonleges_mozgaskorlatozottakvarakozohelye",
        "kulonleges_parkolomozgasserultekreszere",
        "tajekoztato_parkolokerekparosoknak",
        "tajekoztato_parkolokerekparosoknak1",
        "tajekoztato_parkoloparkolaskotelezomodja",
        "tajekoztato_parkoloparkometer",
        "tajekoztato_parkoloparkoloora",
        "kulonleges_parkoljesutazz",
        "kulonleges_parkoljesutazzautobusszal",
        "kulonleges_parkoljesutazzmetroval",
        "kulonleges_parkoljesutazztrolibusszal",
        "kulonleges_parkoljesutazzvillamossal" -> "17. § (1) e)"
        "kulonleges_parkolasiovezet",
        "kulonleges_parkolasiovezetvege" -> "17. § (1) e/2."
        "kulonleges_besorolasirend3" -> "17. § (1) f)"
        "kulonleges_kerekparoskozvetlenkapcsolat" -> "17. § (1) f/1."
        "tajekoztato_autobuszforgalmisav",
        "tajekoztato_kerekparosalltalhasznalhatoautobuszforgalmisav" -> "17. § (1) g)"
        "tajekoztato_kerekparsav" -> "17. § (1) g/1."
        "tajekoztato_kerekparsavvege" -> "17. § (1) g/2."
        "kulonleges_utmelettikerekparut",
        "kulonleges_utmelettikerekparutkezdete" -> "17. § (1) g/4."
        "kulonleges_utmelettikerekparutvege" -> "17. § (1) g/5."
        "tajekoztato_kapaszkodosav",
        "kulonleges_kiegeszitosavkezdete50",
        "kulonleges_forgalmisavoklegkisebbsebessege" -> "17. § (1) h)"
        "tajekoztato_kapaszkodosavvege",
        "kulonleges_kiegeszitosavvege50" -> "17. § (1) i)"
        "kulonleges_lakopihenoovezet" -> "17. § (1) j)"
        "kulonleges_lakopihenoovezetvege" -> "17. § (1) k)"
        "tajekoztato_kikeruloutirany",
        "tajekoztato_kikeruloutiranysuly" -> "17. § (1) r)"
        "kulonleges_lakotteruletkezdete",
        "kulonleges_lakotteruletkezdete1",
        "kulonleges_lakotteruletkezdete2" -> "17. § (1) s)"
        "kulonleges_lakotteruletvege",
        "kulonleges_lakotteruletvege1",
        "kulonleges_lakotteruletvege2" -> "17. § (1) t)"
        "tajekoztato_helynevtabla" -> "17. § (1) u)"
        "tajekoztato_utiranyelorejelzotabla" -> "17. § (1) v)"
        "tajekoztato_iranytablabalra",
        "tajekoztato_iranytablabalra1",
        "tajekoztato_iranytablajobbra",
        "tajekoztato_iranytablajobbra1",
        "tajekoztato_utiranyjelzotabla",
        "tajekoztato_utiranyjelzotablaz",
        "tajekoztato_utiranyjelzotablaz300",
        "tajekoztato_utiranyjelzotablavas" -> "17. § (1) x)"
        "tajekoztato_utvonalmegerositotabla",
        "tajekoztato_utvonalmegerositotablahn" -> "17. § (1) y)"
        "tajekoztato_terelout" -> "17. § (1) z)"
        "kulonleges_korlatozottsebesseguovezet",
        "kulonleges_korlatozottsebesseguovezetvege" -> "14. § (1) z/1."
        "kulonleges_korlatozottforgalmuovezet",
        "kulonleges_korlatozottforgalmuovezetvege" -> "14. § (1) z/2."
        "kulonleges_korlatozottvarakozasiovezet",
        "kulonleges_korlatozottvarakozasiovezetvege" -> "15. § (1) c)"
        "kulonleges_gyalogosovezetvege" -> "13. § (1) h/1."
        "tajekoztato_altalanossebesseghatarok" -> "26. §"
        "tajekoztato_terelotabla" -> "20. § (2)"

        "kiegeszito_foutvonalvonalvezetese",
        "kiegeszito_foutvonalvonalvezetese2",
        "kiegeszito_foutvonalvonalvezetese3",
        "kiegeszito_foutvonalvonalvezetese4",
        "kiegeszito_foutvonalvonalvezetese5",
        "kiegeszito_foutvonalvonalvezetese6",
        "kiegeszito_foutvonalvonalvezetese7",
        "kiegeszito_foutvonalvonalvezetese8",
        "kiegeszito_foutvonalvonalvezetese9",
        "kiegeszito_foutvonalvonalvezetese10" -> "11. § (2)"
        "kiegeszito_dijfizetes",
        "kiegeszito_dijfizetesikotelezettseg",
        "kiegeszito_utdijfizetesajelzettjarmuneksulyhatartol" -> "11. § (4)"
        "kiegeszito_utdijfizetesajelzettjarmuneksulyhatartolvege" -> "11. § (4)"
        "kiegeszito_jelzoor" -> "7. § (2)"
        "kiegeszito_fenysorompo" -> "16. § (1) v)"
        "kiegeszito_hoeses",
        "kiegeszito_hoeses1",
        "kiegeszito_esozes" -> "16. § (5)"
        "kiegeszito_nyomvajusutszakasz" -> "16. § (1) z)"
        "kiegeszito_balesetveszely" -> "16. § (1) z)"
        "kiegeszito_bekak" -> "16. § (1) r)"
        "kiegeszito_jardaszigetnelkulivillamosmegallo" -> "16. § (1) z)"
        "kiegeszito_urszerelvenybenyulofa" -> "16. § (1) z)"
        "kiegeszito_keresztiranyukozlekedes" -> "16. § (1) z/3."
        "kiegeszito_utatkeresztezokerekparoselsobsege" -> "12. § (1) a)"
        "kiegeszito_kivevecelforgalom" -> "14. § (3)"
        "kiegeszito_kivevearuszallitas" -> "14. § (4)"
        "kiegeszito_kiveveengedely",
        "kiegeszito_kivevetaxi" -> "14. § (14)"
        "kiegeszito_kivevebusz",
        "kiegeszito_kivevekerekpar" -> "14. § (15)"
        "kiegeszito_kiveveszemelygepkocsi",
        "kiegeszito_kivevemozgaskorlatozott" -> "14. §"
        "kiegeszito_tilalomkezdete",
        "kiegeszito_tilalomvege" -> "15. § (3)"
        "kiegeszito_elszallitas" -> "15. § (9)"
        "kiegeszito_kerekbilincs" -> "15. § (10)"
        "kiegeszito_utpadkantortenomegallasvarakozastiltasa" -> "15. § (7)"
        "kiegeszito_idotartam" -> "15. § (5)"
        "kiegeszito_idoszak" -> "10. § (2)"
        "kiegeszito_rakodoterulet" -> "15. § (6)"
        "kiegeszito_jardanvarakozasfel",
        "kiegeszito_jardanvarakozasteljes" -> "17. § (1) e)"
        "kiegeszito_parkoloora" -> "17. § (1) e)"
        "kiegeszito_mozgaskorlatozottakreszere" -> "17. § (1) e)"
        "kiegeszito_ketiranyukerekparosforgalom" -> "17. § (3)"
        "kiegeszito_celszerusebessegjelzese",
        "kiegeszito_celszerusebessegvege" -> "20. § (5)"
        "kiegeszito_kiseretnelkuligyerekek" -> "20. § (6)"
        "kiegeszito_terelokup" -> "20. § (3)"
        "kiegeszito_fekvorendor" -> "16. § (1) i)"
        "kiegeszito_gyalogosathaladasbalra",
        "kiegeszito_gyalogosathaladasjobbra" -> "17. § (1) a)"
        "kiegeszito_forgalomcsillapirokozepsziget" -> "16. § (1) z)"
        "kiegeszito_jegyvaltas" -> "17. § (1) e)"
        "kiegeszito_kornyezetvedelmimatricaszine" -> "14. § (1) z/3."
        "kiegeszito_szemelgepkocsikreszere",
        "kiegeszito_tehergepkocsikreszere",
        "kiegeszito_buszokreszere",
        "kiegeszito_motorkerekparreszere",
        "kiegeszito_segedmotorosreszere",
        "kiegeszito_mgvontatoreszere" -> "10. § (2)"

        "utburkolat_terelovonal" -> "18. § (1) b)"
        "utburkolat_zarovonal" -> "18. § (1) c)"
        "utburkolat_buszfelirat" -> "18. § (1) d)"
        "utburkolat_haladasiiranelorejelzese",
        "utburkolat_haladasiiranelorejelzesejobbra",
        "utburkolat_haladasiiranelorejelzesejobbraegyenesen" -> "18. § (1) e)"
        "utburkolat_terelonyilforgalmisavelhagyasanakiranya" -> "18. § (1) f)"
        "utburkolat_gyalogosatkelohely" -> "18. § (1) g)"
        "utburkolat_elsobsegadaskotelezo" -> "18. § (1) h)"
        "utburkolat_eloretoltkerekparosfelallohelybalrakanyarodashoz" -> "18. § (1) h/1."
        "utburkolat_kotelezomegallashelyenekjelzese" -> "18. § (1) i)"
        "utburkolat_varakozohely",
        "utburkolat_varakozohelyferde" -> "18. § (1) j)"
        "utburkolat_jarmuvektolelzartterulet" -> "18. § (1) k)"
        "utburkolat_megallohely" -> "18. § (1) l)"
        "utburkolat_megallasitilalomsargavonal" -> "18. § (1) m)"
        "utburkolat_varakozasitilalomsargavonal" -> "18. § (1) n)"
        "utburkolat_veszelyeshelyrefigyelmeztetovonal",
        "utburkolat_veszelyeshelyrefigyelmeztetovonalgyalogos",
        "utburkolat_veszelyeshelyrefigyelmeztetovonalkerekpar",
        "utburkolat_veszelyeshelyrefigyelmeztetovonalvasutiatkelo" -> "18. § (1) o)"
        "utburkolat_sebessegkorlatozasvagymegallaselorejelzese" -> "18. § (1) p)"
        "utburkolat_keresztezokerekparut",
        "utburkolat_kerekparut" -> "18. § (1) p/1."
        "utburkolat_kerekparsav" -> "18. § (4)"
        "utburkolat_kerekparosnyom" -> "18. § (9)"
        "utburkolat_varakozastilalmaazxhelyen" -> "18. § (1) s)"
        "utburkolat_veszelyesteruletvarakoznitilosezenahelyen" -> "18. § (3)"
        "utburkolat_ideiglenesmunkakmiatthaladasiirany" -> "18. § (8)"

        "fenyjelzo_piros" -> "9. § (4) d)"
        "fenyjelzo_pirossarga" -> "9. § (4) e)"
        "fenyjelzo_zold" -> "9. § (4) a)"
        "fenyjelzo_sarga" -> "9. § (4) c)"
        "fenyjelzo_uzemenkivul",
        "fenyjelzo_uzemenkivuls" -> "9. § (9)"
        "fenyjelzo_gyalogos_piros" -> "8. § (2) c)"
        "fenyjelzo_gyalogos_zold" -> "8. § (2) a)"
        "fenyjelzo_gyalogos_zoldvillogo" -> "8. § (2) b)"
        "fenyjelzo_veszely_jelzese" -> "9. § (4) f)"
        "fenyjelzo_veszely_sarga" -> "9. § (1) c)"
        "fenyjelzo_veszely_sargavill" -> "9. § (1) d)"
        "fenyjelzo_veszely_piros" -> "9. § (1) c)"
        "fenyjelzo_zoldj",
        "fenyjelzo_zoldjj" -> "9. § (4) b)"
        "fenyjelzo_bus" -> "9. § (6)"
        "fenyjelzo_savfoglaltsagpirosx" -> "9. § (8) c)"
        "fenyjelzo_savfoglaltsagzoldnyil" -> "9. § (8) a)"
        "fenyjelzo_savfoglaltsagsarganyil" -> "9. § (8) b)"
        "fenyjelzo_kerekparos" -> "9. § (1) b)"

        else -> when {
            id.startsWith("tajekoztato_") || id.startsWith("kulonleges_") -> "17. § (2)"
            id.startsWith("kiegeszito_") -> "10. § (2)"
            else -> error("Missing KRESZ citation for $id")
        }
    }
}
