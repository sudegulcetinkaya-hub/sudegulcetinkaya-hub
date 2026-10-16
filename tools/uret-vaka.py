# İstek Noktası vaka kartının üç karesini üretir (açık + koyu): bekleyiş → tek kayıt → görünür durum.
# Moda mağazası çizgisi: siyah-beyaz, keskin köşe, ince çizgi, büyük serif başlık, aralıklı büyük harf etiket.
# Marka, logo ya da mağaza fotoğrafı yok. Süre/dakika vaadi yok (kesin karar: yalnız durum).
# Çıktı: assets/vaka/kare-{1,2,3}-{light,dark}.svg
import pathlib

KOK = pathlib.Path(__file__).resolve().parent.parent
W, H = 360, 240

TEMA = {
    "light": dict(zemin="#ffffff", yazi="#000000", soluk="#6b6b6b", cizgi="#d9d9d9", ters="#ffffff"),
    "dark": dict(zemin="#000000", yazi="#ffffff", soluk="#9a9a9a", cizgi="#333333", ters="#000000"),
}
SERIF = "Didot, 'Bodoni 72', 'Bodoni MT', 'Playfair Display', Georgia, 'Times New Roman', serif"
SANS = "'Helvetica Neue', Helvetica, Arial, sans-serif"

def etiket(t, x, y, metin, renk=None, anchor="start", boyut=8.5):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{SANS}" font-size="{boyut}" '
            f'letter-spacing="2.2" fill="{renk or t["soluk"]}">{metin}</text>')

def cerceve(t, no, baslik, ic, alt):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{no}. {baslik}">
<title>{no}. {baslik}</title>
<style>
  .nabiz {{ animation: nabiz 2.6s ease-in-out infinite; }}
  @keyframes nabiz {{ 50% {{ opacity: .25 }} }}
  @media (prefers-reduced-motion: reduce) {{ .nabiz {{ animation: none }} }}
</style>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" fill="{t["zemin"]}" stroke="{t["cizgi"]}"/>
{etiket(t, 22, 30, f"0{no}", t["yazi"])}
<text x="46" y="31" font-family="{SERIF}" font-size="19" fill="{t["yazi"]}">{baslik}</text>
<path d="M22 44 H{W - 22}" stroke="{t["yazi"]}" stroke-width=".75"/>
{ic}
<path d="M22 {H - 34} H{W - 22}" stroke="{t["cizgi"]}" stroke-width=".75"/>
{etiket(t, 22, H - 16, alt)}
</svg>
'''

def askili(t, x, y, s=1.0, dolu=False):
    # askıda tek elbise silueti, ince çizgi
    f = t["yazi"] if dolu else "none"
    return (f'<g transform="translate({x} {y}) scale({s})" fill="none" stroke="{t["yazi"]}" stroke-width="1.1" stroke-linejoin="round">'
            f'<path d="M0 -30 q0 -6 5 -6 q5 0 5 5"/><path d="M-26 -14 L0 -26 L26 -14"/>'
            f'<path d="M-9 -22 L-14 4 L-24 44 H24 L14 4 L9 -22" fill="{f}" fill-opacity="{.9 if dolu else 0}"/>'
            f'<path d="M-14 4 H14"/></g>')

def kare1(t):
    ic = askili(t, 76, 120)
    # müşteri ile depo arasındaki görünmeyen yol: kesikli çizgi, sonunda büyük soru işareti
    ic += f'<path d="M118 132 H262" stroke="{t["soluk"]}" stroke-width=".9" stroke-dasharray="2 5"/>'
    ic += (f'<g transform="translate(284 104)" fill="none" stroke="{t["yazi"]}" stroke-width=".9">'
           f'<rect x="0" y="0" width="48" height="56"/><path d="M0 18.7 H48 M0 37.3 H48"/></g>')
    ic += etiket(t, 308, 176, "STOCKROOM", anchor="middle")
    ic += f'<text x="190" y="122" text-anchor="middle" font-family="{SERIF}" font-size="44" fill="{t["yazi"]}" class="nabiz">?</text>'
    ic += etiket(t, 76, 180, "REQUESTED SIZE", anchor="middle")
    return cerceve(t, 1, "The wait", ic, "IS MY SIZE IN, WHERE IS IT, WHAT HAPPENED?")

def kare2(t):
    ic = askili(t, 72, 118, 0.95)
    ic += etiket(t, 128, 70, "ITEM · REQUEST W-47", t["soluk"])
    ic += f'<text x="128" y="92" font-family="{SERIF}" font-size="17" fill="{t["yazi"]}">Satin midi dress</text>'
    for i, b in enumerate(("XS", "S", "M", "L", "XL")):
        x, sec = 128 + i * 38, b == "M"
        ic += (f'<rect x="{x}" y="104" width="32" height="22" fill="{t["yazi"] if sec else "none"}" stroke="{t["yazi"] if sec else t["cizgi"]}" stroke-width=".9"/>'
               f'<text x="{x + 16}" y="119" text-anchor="middle" font-family="{SANS}" font-size="9.5" letter-spacing="1" '
               f'fill="{t["ters"] if sec else t["soluk"]}">{b}</text>')
    for i, (ad, deger) in enumerate((("STORE", "1"), ("STOCKROOM", "6"), ("LOCATION", "SHELF B-3"))):
        y = 152 + i * 18
        ic += etiket(t, 128, y, ad)
        ic += (f'<text x="{W - 22}" y="{y}" text-anchor="end" font-family="{SANS}" font-size="10" letter-spacing="1.5" '
               f'fill="{t["yazi"]}">{deger}</text>')
        ic += f'<path d="M128 {y + 6} H{W - 22}" stroke="{t["cizgi"]}" stroke-width=".6"/>'
    return cerceve(t, 2, "One record", ic, "STOCK, SIZE AND SHELF ON ONE SCREEN")

def kare3(t):
    ic = etiket(t, 22, 70, "REQUEST CODE")
    ic += f'<text x="22" y="112" font-family="{SERIF}" font-size="46" fill="{t["yazi"]}">W-47</text>'
    adimlar = ("RECEIVED", "SEARCHING STOCKROOM", "ON THE NEXT RUN", "AT THE REQUEST POINT")
    aktif = 2
    for i, ad in enumerate(adimlar):
        y = 66 + i * 24
        x = 168
        if i < aktif:
            ic += f'<rect x="{x}" y="{y - 7}" width="7" height="7" fill="{t["yazi"]}"/>'
        elif i == aktif:
            ic += (f'<rect x="{x}" y="{y - 7}" width="7" height="7" fill="{t["yazi"]}" class="nabiz"/>'
                   f'<rect x="{x - 3}" y="{y - 10}" width="13" height="13" fill="none" stroke="{t["yazi"]}" stroke-width=".8"/>')
        else:
            ic += f'<rect x="{x}" y="{y - 7}" width="7" height="7" fill="none" stroke="{t["soluk"]}" stroke-width=".8"/>'
        renk = t["yazi"] if i <= aktif else t["soluk"]
        ic += etiket(t, x + 18, y, ad, renk)
    ic += etiket(t, 22, 186, "NO TIME PROMISES · ONLY THE REAL STATUS")
    return cerceve(t, 3, "Visible status", ic, "THE CUSTOMER FOLLOWS THEIR OWN REQUEST")

(KOK / "assets" / "vaka").mkdir(parents=True, exist_ok=True)
for ad, t in TEMA.items():
    for no, f in enumerate((kare1, kare2, kare3), 1):
        yol = KOK / "assets" / "vaka" / f"kare-{no}-{ad}.svg"
        yol.write_text(f(t), encoding="utf-8")
        print("yazildi:", yol.relative_to(KOK).as_posix())
