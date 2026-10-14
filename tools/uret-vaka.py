# İstek Noktası vaka kartının üç karesini üretir (açık + koyu): bekleme → tek ekran → görünür durum.
# Sade çizim; marka, logo ya da mağaza fotoğrafı yok. Çıktı: assets/vaka/kare-{1,2,3}-{light,dark}.svg
import pathlib

KOK = pathlib.Path(__file__).resolve().parent.parent
W, H = 360, 240

TEMA = {
    "dark": dict(zemin="#111823", kart="#18212e", cizgi="#2a3442", yazi="#eef1f4", soluk="#8a97a6",
                 vurgu="#3fd0a2", ikinci="#5b7cfa", uyari="#ff7a8c", ten="#c9d2dc"),
    "light": dict(zemin="#f6f4ef", kart="#ffffff", cizgi="#ddd8cd", yazi="#14181d", soluk="#5d6773",
                  vurgu="#1f9e7a", ikinci="#3f5fd8", uyari="#d94a64", ten="#3a4350"),
}
MONO = "ui-monospace, 'SF Mono', 'Cascadia Code', Consolas, monospace"
SANS = "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"

def cerceve(t, no, baslik, ic):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{no}. {baslik}">
<title>{no}. {baslik}</title>
<style>
  .nabiz {{ animation: nabiz 2.4s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }}
  @keyframes nabiz {{ 50% {{ opacity: .35 }} }}
  @media (prefers-reduced-motion: reduce) {{ .nabiz {{ animation: none }} }}
</style>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="{t["zemin"]}" stroke="{t["cizgi"]}"/>
<text x="22" y="34" font-family="{MONO}" font-size="12" letter-spacing="2" fill="{t["soluk"]}">0{no}</text>
<text x="52" y="34" font-family="{SANS}" font-size="15" font-weight="600" fill="{t["yazi"]}">{baslik}</text>
{ic}
</svg>
'''

def kisi(t, x, y, renk):
    return (f'<circle cx="{x}" cy="{y}" r="11" fill="{renk}"/>'
            f'<path d="M{x - 19} {y + 46} Q{x - 19} {y + 16} {x} {y + 16} Q{x + 19} {y + 16} {x + 19} {y + 46} Z" fill="{renk}"/>')

def kare1(t):
    # müşteri bekliyor; saat dönüyor; danışman depoya gidip geliyor (kesikli yol)
    ic = kisi(t, 70, 118, t["ten"])
    ic += (f'<g transform="translate(70 82)"><circle r="17" fill="{t["kart"]}" stroke="{t["uyari"]}" stroke-width="2.5"/>'
           f'<path d="M0 -9 V0 L7 5" fill="none" stroke="{t["uyari"]}" stroke-width="2.5" stroke-linecap="round"/></g>')
    ic += f'<path d="M110 160 C160 120 220 200 270 150" fill="none" stroke="{t["soluk"]}" stroke-width="2" stroke-dasharray="5 7"/>'
    ic += f'<path d="M270 150 C220 210 160 120 110 172" fill="none" stroke="{t["soluk"]}" stroke-width="2" stroke-dasharray="5 7" opacity=".55"/>'
    ic += (f'<g transform="translate(272 98)"><rect x="0" y="0" width="64" height="58" rx="6" fill="{t["kart"]}" stroke="{t["cizgi"]}"/>'
           f'<path d="M0 20 H64 M0 39 H64" stroke="{t["cizgi"]}"/>'
           f'<rect x="8" y="6" width="14" height="10" rx="2" fill="{t["soluk"]}" opacity=".5"/><rect x="28" y="25" width="20" height="10" rx="2" fill="{t["soluk"]}" opacity=".5"/>'
           f'<text x="32" y="78" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{t["soluk"]}">depo</text></g>')
    ic += f'<text x="182" y="128" text-anchor="middle" font-family="{SANS}" font-size="28" font-weight="700" fill="{t["uyari"]}" class="nabiz">?</text>'
    ic += f'<text x="22" y="216" font-family="{SANS}" font-size="13" fill="{t["soluk"]}">Ürün var mı, nerede, ne kadar sürer?</text>'
    return cerceve(t, 1, "Müşteri bekliyor", ic)

def kare2(t):
    # tek ekran: ürün, beden, stok ve konum
    ic = f'<rect x="40" y="52" width="280" height="148" rx="12" fill="{t["kart"]}" stroke="{t["cizgi"]}"/>'
    ic += (f'<rect x="56" y="68" width="44" height="44" rx="8" fill="{t["zemin"]}" stroke="{t["cizgi"]}"/>'
           f'<path d="M66 80 L73 74 H83 L90 80 L86 86 L84 84 V104 H72 V84 L70 86 Z" fill="none" stroke="{t["yazi"]}" stroke-width="1.6" stroke-linejoin="round"/>')
    ic += f'<rect x="112" y="72" width="110" height="9" rx="4.5" fill="{t["yazi"]}" opacity=".8"/><rect x="112" y="89" width="70" height="7" rx="3.5" fill="{t["soluk"]}" opacity=".6"/>'
    for i, (b, var) in enumerate((("S", False), ("M", True), ("L", True), ("XL", False))):
        x = 112 + i * 40
        ic += (f'<rect x="{x}" y="102" width="32" height="20" rx="10" fill="{t["vurgu"] if var else "none"}" fill-opacity="{.18 if var else 0}" stroke="{t["vurgu"] if var else t["cizgi"]}"/>'
               f'<text x="{x + 16}" y="116" text-anchor="middle" font-family="{MONO}" font-size="10" fill="{t["yazi"] if var else t["soluk"]}">{b}</text>')
    satirlar = (("Mağaza", "1", t["vurgu"], 0.25), ("Depo", "6", t["ikinci"], 1.0))
    for i, (ad, adet, renk, oran) in enumerate(satirlar):
        y = 144 + i * 24
        ic += (f'<text x="56" y="{y + 4}" font-family="{SANS}" font-size="12" fill="{t["soluk"]}">{ad}</text>'
               f'<rect x="112" y="{y - 5}" width="120" height="8" rx="4" fill="{t["cizgi"]}"/><rect x="112" y="{y - 5}" width="{120 * oran:.0f}" height="8" rx="4" fill="{renk}"/>'
               f'<text x="242" y="{y + 4}" font-family="{MONO}" font-size="12" fill="{t["yazi"]}">{adet}</text>')
    ic += (f'<g transform="translate(272 152)"><path d="M0 -14 C-9 -14 -12 -7 -12 -3 C-12 5 0 16 0 16 C0 16 12 5 12 -3 C12 -7 9 -14 0 -14 Z" fill="{t["ikinci"]}"/>'
           f'<circle cy="-3" r="4" fill="{t["kart"]}"/><text y="32" text-anchor="middle" font-family="{MONO}" font-size="10" fill="{t["soluk"]}">raf B-3</text></g>')
    ic += f'<text x="22" y="222" font-family="{SANS}" font-size="13" fill="{t["soluk"]}">Stok ve konum tek ekranda.</text>'
    return cerceve(t, 2, "Tek ekran", ic)

def kare3(t):
    # isteğin durumu: alındı → hazırlanıyor → yolda → teslim
    adimlar = ("alındı", "hazırlanıyor", "yolda", "teslim")
    ic, x0, ara, y = "", 52, 85, 110
    ic += f'<path d="M{x0} {y} H{x0 + 3 * ara}" stroke="{t["cizgi"]}" stroke-width="4" stroke-linecap="round"/>'
    ic += f'<path d="M{x0} {y} H{x0 + 2 * ara}" stroke="{t["vurgu"]}" stroke-width="4" stroke-linecap="round"/>'
    for i, ad in enumerate(adimlar):
        x = x0 + i * ara
        if i < 2:
            ic += (f'<circle cx="{x}" cy="{y}" r="12" fill="{t["vurgu"]}"/>'
                   f'<path d="M{x - 5} {y} L{x - 1} {y + 4} L{x + 6} {y - 4}" fill="none" stroke="{t["kart"]}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>')
        elif i == 2:
            ic += (f'<circle cx="{x}" cy="{y}" r="17" fill="{t["vurgu"]}" opacity=".25" class="nabiz"/>'
                   f'<circle cx="{x}" cy="{y}" r="12" fill="{t["kart"]}" stroke="{t["vurgu"]}" stroke-width="3"/><circle cx="{x}" cy="{y}" r="4" fill="{t["vurgu"]}"/>')
        else:
            ic += f'<circle cx="{x}" cy="{y}" r="12" fill="{t["kart"]}" stroke="{t["cizgi"]}" stroke-width="3"/>'
        renk = t["yazi"] if i <= 2 else t["soluk"]
        ic += f'<text x="{x}" y="{y + 34}" text-anchor="middle" font-family="{SANS}" font-size="11.5" fill="{renk}">{ad}</text>'
    ic += (f'<rect x="70" y="162" width="220" height="32" rx="16" fill="{t["vurgu"]}" fill-opacity=".14" stroke="{t["vurgu"]}"/>'
           f'<text x="180" y="184" text-anchor="middle" font-family="{SANS}" font-size="12.5" fill="{t["yazi"]}">yaklaşık 3 dk · danışman yolda</text>')
    ic += f'<text x="22" y="222" font-family="{SANS}" font-size="13" fill="{t["soluk"]}">İsteğin durumu herkese görünür.</text>'
    return cerceve(t, 3, "Durum görünür", ic)

(KOK / "assets" / "vaka").mkdir(parents=True, exist_ok=True)
for ad, t in TEMA.items():
    for no, f in enumerate((kare1, kare2, kare3), 1):
        yol = KOK / "assets" / "vaka" / f"kare-{no}-{ad}.svg"
        yol.write_text(f(t), encoding="utf-8")
        print("yazildi:", yol.relative_to(KOK).as_posix())
