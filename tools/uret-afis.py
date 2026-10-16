# Sude'nin GitHub profil afişini üretir (açık + koyu). Tohum aydan gelir: aynı ayda her koşu aynı
# çıktıyı verir, her ay yeni bir baskı çıkar (köşede "OCTOBER 2026 EDITION" gibi bir etiket).
# Ayı elle seçmek için: AFIS_AY=2026-11 python tools/uret-afis.py
# Çizgiler: diş minesi / eşyükselti katmanları gibi akan eğriler; yatayda periyodik, böylece
# sola kayan animasyon dikişsiz döner. Hareket azaltma tercihinde animasyon durur.
import datetime, math, os, random, pathlib

KOK = pathlib.Path(__file__).resolve().parent.parent
W, H = 1280, 400
# "Sude Gül" ve "ÇETİNKAYA" aynı sağ kenarda biter: iki satır da bu genişliğe sabitlenir
# (textLength), böylece görüntüleyicinin yazı tipi farklı olsa da hiza bozulmaz.
AD_GENISLIK = 243
# İki dil: "en" assets/afis-*.svg (ana README), "tr" assets/tr/afis-*.svg (README.tr.md).
METINLER = {
    "en": dict(aylar=["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE",
                      "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"],
               baski="EDITION", slogan="We bring a business’s entire operation under one roof.",
               rol="co-founder", klasor="assets"),
    "tr": dict(aylar=["OCAK", "ŞUBAT", "MART", "NİSAN", "MAYIS", "HAZİRAN",
                      "TEMMUZ", "AĞUSTOS", "EYLÜL", "EKİM", "KASIM", "ARALIK"],
               baski="BASKISI", slogan="İşletmelerin tüm operasyonunu tek çatı altında topluyoruz.",
               rol="kurucu ortak", klasor="assets/tr"),
}
M = METINLER["en"]

def baski_ayi():
    """(yıl, ay): AFIS_AY varsa ondan, yoksa Türkiye saatiyle (UTC+3) bugünden."""
    elle = os.environ.get("AFIS_AY", "").strip()
    if elle:
        yil, ay = (int(p) for p in elle.split("-"))
        if not 1 <= ay <= 12:
            raise SystemExit(f"AFIS_AY geçersiz: {elle} (örnek 2026-11)")
        return yil, ay
    simdi = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3)))
    return simdi.year, simdi.month

YIL, AY = baski_ayi()
TOHUM = YIL * 100 + AY

TEMA = {
    "dark": dict(zemin="#0b0f14", zemin2="#111823", yazi="#eef1f4", soluk="#8a97a6", ince="#2a3442",
                 renkler=["#3fd0a2", "#2fa7c9", "#5b7cfa", "#9b6cf0", "#ff7a8c"], opak=0.55),
    "light": dict(zemin="#fbfaf7", zemin2="#f1efe9", yazi="#14181d", soluk="#5d6773", ince="#d9d5cc",
                  renkler=["#1f9e7a", "#1f7fae", "#3f5fd8", "#7c3aed", "#d94a64"], opak=0.62),
}

def egri(r, i, n):
    """Periyodu W olan, birkaç sinüsün toplamı: yumuşak, organik bir katman çizgisi."""
    taban = 70 + i * (H - 120) / n
    harm = [(r.uniform(6, 26) * (1 - i / n * 0.4), k, r.uniform(0, 2 * math.pi)) for k in (1, 2, 3, 5)]
    noktalar = []
    for x in range(0, 2 * W + 1, 16):
        y = taban
        for gen, k, faz in harm:
            y += gen / k * math.sin(2 * math.pi * k * x / W + faz)
        # sağ yarıda katmanlar hafifçe toplanır: göz, yazıdan çizgilere akar (periyodik tümsek: dikişsiz)
        y += 26 * math.sin(math.pi * i / n) * math.exp(3.2 * (math.cos(2 * math.pi * (x - 900) / W) - 1))
        noktalar.append((x, y))
    d = f"M{noktalar[0][0]},{noktalar[0][1]:.1f}"
    for (x0, y0), (x1, y1) in zip(noktalar, noktalar[1:]):
        d += f" Q{x0},{y0:.1f} {(x0 + x1) / 2:.1f},{(y0 + y1) / 2:.1f}"
    return d

def renk_karis(a, b, t):
    pa = [int(a[j:j + 2], 16) for j in (1, 3, 5)]
    pb = [int(b[j:j + 2], 16) for j in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(pa, pb))

def afis(ad):
    t = TEMA[ad]
    r = random.Random(TOHUM)
    n = 26
    yollar = []
    for i in range(n):
        u = i / (n - 1)
        seg = u * (len(t["renkler"]) - 1)
        k = min(int(seg), len(t["renkler"]) - 2)
        renk = renk_karis(t["renkler"][k], t["renkler"][k + 1], seg - k)
        kalin = 1.6 if i % 6 == 0 else 0.9
        op = t["opak"] * (0.55 + 0.45 * math.sin(math.pi * u))
        yollar.append(f'<path d="{egri(r, i, n)}" stroke="{renk}" stroke-width="{kalin}" stroke-opacity="{op:.2f}"/>')
    # küçük "veri" noktaları: çizgilerin üstünde seyrek parıltı
    noktalar = []
    for _ in range(18):
        x, y = r.uniform(560, 1240), r.uniform(60, 360)
        noktalar.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.choice([1.2, 1.6, 2.2])}" fill="{r.choice(t["renkler"])}" class="pirilti" style="animation-delay:{r.uniform(0, 6):.1f}s"/>')
    serif = "Georgia, 'Iowan Old Style', 'Palatino Linotype', 'Times New Roman', serif"
    mono = "ui-monospace, 'SF Mono', 'Cascadia Code', Consolas, 'Liberation Mono', monospace"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Sude Gül Çetinkaya — {M["rol"]}, OpOne · DentAI · HotelAI · SocialAI · AgentAI">
<title>Sude Gül Çetinkaya — kurucu ortak, OpOne · DentAI · HotelAI · SocialAI · AgentAI</title>
<defs>
  <linearGradient id="zemin" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t["zemin"]}"/><stop offset="1" stop-color="{t["zemin2"]}"/></linearGradient>
  <linearGradient id="perde" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t["zemin"]}" stop-opacity="1"/><stop offset=".34" stop-color="{t["zemin"]}" stop-opacity=".92"/><stop offset=".55" stop-color="{t["zemin"]}" stop-opacity="0"/></linearGradient>
  <clipPath id="kirp"><rect width="{W}" height="{H}" rx="18"/></clipPath>
</defs>
<style>
  .akis {{ animation: kay 48s linear infinite; }}
  @keyframes kay {{ from {{ transform: translateX(0) }} to {{ transform: translateX(-{W}px) }} }}
  .pirilti {{ opacity: 0; animation: parla 7s ease-in-out infinite; }}
  @keyframes parla {{ 0%, 100% {{ opacity: 0 }} 45% {{ opacity: .9 }} }}
  .imlec {{ animation: yanip 1.1s steps(1) infinite; }}
  @keyframes yanip {{ 50% {{ opacity: 0 }} }}
  @media (prefers-reduced-motion: reduce) {{ .akis, .pirilti, .imlec {{ animation: none }} .pirilti {{ opacity: .6 }} }}
</style>
<g clip-path="url(#kirp)">
  <rect width="{W}" height="{H}" fill="url(#zemin)"/>
  <g fill="none" stroke-linecap="round"><g class="akis">{"".join(yollar)}</g></g>
  <g>{"".join(noktalar)}</g>
  <rect width="{W}" height="{H}" fill="url(#perde)"/>
  <g font-family="{mono}" font-size="12" fill="{t["soluk"]}" letter-spacing="2.4">
    <text x="64" y="74">N° 01 · OPONE</text>
    <text x="{W - 64}" y="74" text-anchor="end" font-size="11">{M["aylar"][AY - 1]} {YIL} {M["baski"]}</text>
    <text x="{W - 64}" y="{H - 38}" text-anchor="end">dent · hotel · social · agent · {YIL}</text>
  </g>
  <line x1="64" y1="92" x2="148" y2="92" stroke="{t["renkler"][0]}" stroke-width="2"/>
  <text x="60" y="194" font-family="{serif}" font-size="63" fill="{t["yazi"]}" textLength="{AD_GENISLIK}" lengthAdjust="spacing">Sude Gül</text>
  <text x="64" y="242" font-family="{mono}" font-size="26" fill="{t["yazi"]}" textLength="{AD_GENISLIK - 4}" lengthAdjust="spacing">ÇETİNKAYA</text>
  <text x="64" y="304" font-family="{serif}" font-size="21" font-style="italic" fill="{t["soluk"]}">{M["slogan"]}</text>
  <g font-family="{mono}" font-size="13" fill="{t["soluk"]}">
    <text x="64" y="346"><tspan fill="{t["renkler"][0]}">›</tspan> {M["rol"]} — OpOne · DentAI · HotelAI · SocialAI · AgentAI<tspan class="imlec" fill="{t["renkler"][0]}"> ▍</tspan></text>
  </g>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{t["ince"]}"/>
</svg>
'''

for dil, M in METINLER.items():
    klasor = KOK / M["klasor"]
    klasor.mkdir(parents=True, exist_ok=True)
    for ad in TEMA:
        (klasor / f"afis-{ad}.svg").write_text(afis(ad), encoding="utf-8")
        print("yazildi:", f"{M['klasor']}/afis-{ad}.svg", "·", M["aylar"][AY - 1], YIL, "· tohum", TOHUM)
