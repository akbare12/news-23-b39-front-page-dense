#!/usr/bin/env python3
"""news-23 b39 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026.
1024x1024 front page, 31 stories. Run: python3 draw.py -> entry.png
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FD = "/usr/share/fonts/truetype/dejavu/"

def F(size, bold=False):
    return ImageFont.truetype(FD + ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"), size)

def tw(draw, text, font):
    return draw.textlength(text, font=font)

def wrap(draw, text, font, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

# palette
BLACK = (10, 10, 10)
WHITE = (255, 255, 255)
CREAM = (250, 246, 236)
GOLD = (212, 175, 55)
GOLDD = (176, 141, 30)
RED = (198, 32, 32)
REDL = (220, 60, 60)
NAVY = (16, 32, 80)
NAVY2 = (24, 48, 110)
TEAL = (0, 128, 128)
TEALD = (0, 96, 96)
GREEN = (34, 139, 34)
BLUE = (30, 90, 180)
PURPLE = (128, 0, 128)
GRAY = (90, 90, 90)
LGRAY = (230, 230, 230)
SKY = (214, 232, 244)
LEAF = (139, 195, 110)

img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)

# ---------- masthead ----------
d.rectangle([0, 0, W, 58], fill=BLACK)
d.text((16, 8), "THE WORLD TODAY", font=F(40, True), fill=WHITE)
d.text((W - 16 - tw(d, "MONDAY 23 NOVEMBER 2026", F(19, True)), 18),
       "MONDAY 23 NOVEMBER 2026", font=F(19, True), fill=GOLD)

# ---------- kicker ----------
d.text((16, 62), "AI rout hits Asia  \u00b7  UN chief urges AI rules  \u00b7  US lead over China at record low  \u00b7  Anthropic IPO $107.3B",
       font=F(15, True), fill=RED)

# ---------- number strip: 2 rows x 5 cols ----------
nums = [
    ("-3.3%", "KOSPI", RED),
    ("5.3", "US-CHINA POWER GAP", NAVY),
    ("11,762", "EBOLA CASES, DRC", GREEN),
    ("10T won", "SEOUL STABILISATION FUND", GOLDD),
    ("2%", "BILLIONAIRE TAX IN PARIS", PURPLE),
    ("$450M", "SKUBAL DEAL", PURPLE),
    ("165", "RUSSIAN MISSILES IN A WEEK", RED),
    ("12,000", "CLEARED IN MANCHESTER", BLUE),
    ("264 kg", "EXPLOSIVES SEIZED IN LEBANON", GOLDD),
    ("$107.3B", "ANTHROPIC IPO \u2014 LARGEST", PURPLE),
]
for i, (num, lab, col) in enumerate(nums):
    r, c = divmod(i, 5)
    x = int(c * 204.8) + 8
    y = 78 + r * 32
    d.text((x, y), num, font=F(21, True), fill=col)
    d.text((x, y + 22), lab, font=F(10, True), fill=BLACK)

# ---------- region bar ----------
regions = [("ASIA-PACIFIC 7", 7, TEAL), ("AMERICAS 8", 8, NAVY2),
           ("MIDDLE EAST 6", 6, (176, 124, 30)), ("EUROPE 5", 5, PURPLE),
           ("AFRICA 3", 3, RED), ("WORLD 2", 2, (110, 110, 110))]
x = 0
for j, (name, n, col) in enumerate(regions):
    wseg = int(round(n / 31 * W))
    if j == len(regions) - 1:
        wseg = W - x  # last segment takes the remainder so nothing clips
    d.rectangle([x, 148, x + wseg - 1, 165], fill=col)
    t = name
    if j == len(regions) - 1:
        tx = x + wseg - 8 - tw(d, t, F(12, True))
    else:
        tx = x + (wseg - tw(d, t, F(12, True))) / 2
    d.text((tx, 151), t, font=F(12, True), fill=WHITE)
    x += wseg

# ---------- UTC strip ----------
d.rectangle([0, 166, W, 181], fill=NAVY)
d.text((10, 169), "THE DAY IN UTC", font=F(11, True), fill=GOLD)
utc_items = ["~00:00 Kospi dives", "~06:30 Guterres opens", "~09:00 Power Index",
             "~12:00 Paris 2% tax", "~15:00 Kyiv missiles", "~18:00 IPO $97.17"]
ux = 128
for it in utc_items:
    if ux + tw(d, it, F(11)) > W - 78:
        break
    d.text((ux, 169), it, font=F(11), fill=WHITE)
    ux += tw(d, it, F(11)) + 22
d.text((W - 8 - tw(d, "~ APPROX", F(11)), 169), "~ APPROX", font=F(11), fill=(180, 190, 220))

# ---------- heroes ----------
HX = [8, 348, 688]
HW = 328

def chip(x, y, label):
    f = F(9, True)
    wch = tw(d, label, f) + 10
    col = RED if label == "CLAIM" else NAVY
    d.rectangle([x - wch, y, x, y + 13], fill=col)
    d.text((x - wch + 5, y + 1), label, font=f, fill=WHITE)
    return wch

def hero_scene_kospi(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(12, 20, 52))
    d.text((x + 10, y + 6), "-3.3%", font=F(34, True), fill=REDL)
    # skyline
    import random
    rnd = random.Random(7)
    bx = x + 8
    while bx < x + w - 18:
        bw = rnd.randint(16, 26)
        bh = rnd.randint(28, 62)
        by = y + h - 8 - bh
        d.rectangle([bx, by, bx + bw, y + h - 8], fill=(30, 48, 96))
        for wy in range(by + 5, y + h - 12, 9):
            for wx in range(bx + 3, bx + bw - 3, 7):
                if rnd.random() < 0.55:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 90))
        bx += bw + 4
    # descending chart line
    pts = [(x + 14 + i * 34, y + 62 + i * 5 + (0 if i % 2 == 0 else 3)) for i in range(9)]
    d.line(pts, fill=(255, 80, 60), width=3)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 200, 60))

def hero_scene_guterres(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=TEAL)
    # globe top-right, clear of text
    gx, gy, gr = x + w - 34, y + 16, 20
    d.ellipse([gx - gr, gy, gx + gr, gy + 2 * gr], fill=(190, 235, 220))
    d.ellipse([gx - gr + 4, gy + 4, gx + gr - 4, gy + 2 * gr - 4], outline=(0, 90, 90), width=2)
    d.arc([gx - gr + 2, gy + 8, gx + gr - 2, gy + 2 * gr - 8], 200, 340, fill=(0, 90, 90), width=2)
    d.line([gx - gr, gy + gr, gx + gr, gy + gr], fill=(0, 90, 90), width=2)
    d.text((x + 10, y + 8), "150 DELEGATES", font=F(29, True), fill=(255, 220, 60))
    d.text((x + 10, y + 40), "BACK A RISK", font=F(29, True), fill=WHITE)
    d.text((x + 10, y + 72), "FRAMEWORK", font=F(29, True), fill=WHITE)

def hero_scene_power(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 240, 210))
    d.text((x + 10, y + 6), "NARROWEST SINCE 2018", font=F(11, True), fill=BLACK)
    d.text((x + w - 10 - tw(d, "GAP 5.3", F(11, True)), y + 6), "GAP 5.3", font=F(11, True), fill=GOLDD)
    base = y + h - 26
    bars = [("US", 78.9, NAVY, 66), ("CHINA", 73.6, RED, 61), ("INDIA", 40.5, GOLDD, 34)]
    bx = x + 22
    for name, val, col, bh in bars:
        d.rectangle([bx, base - bh, bx + 62, base], fill=col)
        vt = f"{val}"
        d.text((bx + 31 - tw(d, vt, F(15, True)) / 2, base - bh + 6), vt, font=F(15, True), fill=WHITE)
        d.text((bx + 31 - tw(d, name, F(11, True)) / 2, base + 4), name, font=F(11, True), fill=BLACK)
        bx += 96

heroes = [
    ("AI ROUT HITS ASIA",
     "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5.",
     "KOREA EXCHANGE", "REPORTED", "KOSPI 4,708.54  \u00b7  -161 PTS", hero_scene_kospi),
    ("GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "UN chief urges global AI safety rules at the Bridgetown summit; 150 delegates back a risk framework.",
     "UNITED NATIONS", "REPORTED", "UN  \u00b7  BRIDGETOWN", hero_scene_guterres),
    ("US LEAD OVER CHINA AT RECORD LOW",
     "Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, narrowest since 2018. India third at 40.5.",
     "LOWY INSTITUTE", "REPORTED", "ASIA POWER INDEX 2026", hero_scene_power),
]
for i, (head, body, src, ch, cap, scene_fn) in enumerate(heroes):
    x = HX[i]
    scene_fn(x, 182, HW, 110)
    d.rectangle([x, 292, x + HW, 308], fill=BLACK)
    d.text((x + 8, 295), cap, font=F(11, True), fill=WHITE)
    # badge + headline (headline indented 28px so badge never covers first letter)
    d.ellipse([x + 2, 314, x + 22, 334], fill=RED)
    d.text((x + 9, 316), str(i + 1), font=F(13, True), fill=WHITE)
    hl = wrap(d, head, F(17, True), HW - 30)
    hy = 312
    for ln in hl[:2]:
        d.text((x + 28, hy), ln, font=F(17, True), fill=BLACK)
        hy += 19
    bl = wrap(d, body, F(11), HW)
    by = 350
    for ln in bl[:2]:
        d.text((x, by), ln, font=F(11), fill=BLACK)
        by += 12
    d.text((x, 378), src, font=F(9), fill=GRAY)
    chip(x + HW, 376, ch)

# ---------- MORE header ----------
d.rectangle([0, 390, W, 408], fill=BLACK)
d.text((10, 393), "MORE OF THE DAY  \u2014  10 STORIES", font=F(14, True), fill=WHITE)

# ---------- cards ----------
cards = [
    ("AMERICAS", TEAL, "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.", "Reuters", "REPORTED"),
    ("FBI", PURPLE, "FBI PROBES NCIC HACK", "Hackers hit police database.", "AP", "REPORTED"),
    ("WHITE HOUSE", (176, 124, 30), "TRUMP: IRAN STRIKES MAY RESUME", "May resume in New Year.", "Reuters", "REPORTED"),
    ("MARKETS", GREEN, "US FUTURES JUMP 3%", "Holiday rally lifts futures 3%.", "Bloomberg", "REPORTED"),
    ("SPORT", RED, "SKUBAL'S $450M METS DEAL", "Largest ever deal.", "AP", "REPORTED"),
    ("SPORT", RED, "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice, dies.", "ESPN", "REPORTED"),
    ("LEGAL", PURPLE, "STATES SUE SPACEX", "Ten states challenge AI claims.", "AP", "REPORTED"),
    ("TECH", NAVY2, "ANTHROPIC IPO: $107.3B", "Raised at $83; closes $97.17.", "WSJ", "REPORTED"),
    ("EUROPE", (176, 124, 30), "POLAND: 3 MISSILES CROSSED AIRSPACE", "Three Kh-101s crossed.", "AP", "CLAIM"),
    ("SPACE", (110, 110, 110), "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.", "Reuters", "CLAIM"),
]
for i, (cat, col, head, body, src, ch) in enumerate(cards):
    r, c = divmod(i, 5)
    x = 8 + c * 204
    y = 412 + r * 78
    cw = 196
    d.rectangle([x, y, x + cw, y + 15], fill=col)
    d.text((x + 4, y + 1), cat, font=F(10, True), fill=WHITE)
    d.text((x + cw - 4 - tw(d, str(i + 1), F(10, True)), y + 1), str(i + 1), font=F(10, True), fill=WHITE)
    hl = wrap(d, head, F(12, True), cw)
    hy = y + 19
    for ln in hl[:2]:
        d.text((x, hy), ln, font=F(12, True), fill=BLACK)
        hy += 15
    d.text((x, y + 51), body, font=F(10), fill=BLACK)
    d.text((x, y + 64), src, font=F(9), fill=GRAY)
    chip(x + cw, y + 62, ch)

# ---------- map + ALSO ----------
d.rectangle([0, 568, 340, 586], fill=BLACK)
d.text((10, 571), "WHERE IT HAPPENED", font=F(13, True), fill=WHITE)
d.rectangle([348, 568, W, 586], fill=BLACK)
d.text((356, 571), "ALSO ON MONDAY", font=F(13, True), fill=WHITE)

# stylized map
mx, my, mw, mh = 8, 590, 332, 196
d.rectangle([mx, my, mx + mw, my + mh], fill=SKY)
for gx in range(mx, mx + mw, 22):
    d.line([gx, my, gx, my + mh], fill=(200, 220, 235), width=1)
for gy in range(my, my + mh, 22):
    d.line([mx, gy, mx + mw, gy], fill=(200, 220, 235), width=1)
# continents (blobs)
d.ellipse([mx + 8, my + 18, mx + 130, my + 130], fill=LEAF)      # N America
d.ellipse([mx + 60, my + 110, mx + 130, my + 180], fill=LEAF)    # S America
d.ellipse([mx + 150, my + 30, mx + 215, my + 105], fill=LEAF)    # Europe
d.ellipse([mx + 190, my + 95, mx + 235, my + 165], fill=LEAF)    # Africa
d.ellipse([mx + 235, my + 25, mx + 325, my + 105], fill=LEAF)    # Asia
d.ellipse([mx + 255, my + 140, mx + 300, my + 175], fill=LEAF)   # Australia
pins = [(300, 640, 1), (125, 748, 2), (315, 625, 3), (75, 665, 4), (105, 650, 5),
        (200, 675, 6), (60, 620, 7), (40, 660, 8), (80, 700, 9), (95, 720, 10),
        (205, 625, 11), (225, 640, 12), (245, 620, 13)]
for px, py, n in pins:
    d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED, outline=WHITE, width=1)
    t = str(n)
    d.text((px - tw(d, t, F(9, True)) / 2, py - 7), t, font=F(9, True), fill=WHITE)
d.text((mx, 790), "Pins 1\u201313: 1 Seoul \u00b7 2 Bridgetown \u00b7 3 Beijing \u00b7 4 Washington \u00b7 5 New York \u00b7 6 Tehran",
       font=F(8), fill=BLACK)
d.text((mx, 802), "7 Chicago \u00b7 8 San Francisco \u00b7 9 Denver \u00b7 10 Austin \u00b7 11 Warsaw \u00b7 12 Kyiv \u00b7 13 Moscow",
       font=F(8), fill=BLACK)

also = [
    "14. Paris: 100+ back 2% billionaire tax", "15. Manchester: 12,000 cleared",
    "16. Zelenskyy: 165 missiles in a week", "17. COP31: the day after pact rejected",
    "18. Benghazi: UN demands port probe", "19. Israel unity talks resume",
    "20. Gaza: two killed in Israeli strike", "21. West Bank settler attacks",
    "22. Iran war: no deal in sight",
    "23. Lebanon seizes 264 kg explosives", "24. Bahrain: strike hits plant, 2 hurt",
    "25. Sudan: defences down drones", "26. DRC: fighting traps Ebola teams",
    "27. Bangladesh: Hasina jailed if she returns", "28. Seoul minister quits in exam row",
    "29. SK Telecom -7.3% as hype cools", "30. China eases margin rules",
    "31. Seoul readies 10T-won fund",
]
for i, a in enumerate(also):
    col = 0 if i < 9 else 1
    row = i % 9
    ax = 356 + col * 334
    ay = 594 + row * 22
    d.text((ax, ay), a, font=F(11), fill=BLACK)

# ---------- DATE CHECK ----------
d.rectangle([8, 818, W - 8, 902], outline=RED, width=2)
d.text((16, 824), "DATE CHECK", font=F(13, True), fill=RED)
d.text((W - 16 - tw(d, "READ 23 NOV 2026, 23:59 UTC \u2014 STORIES DATED 23 NOV ONLY", F(10, True)), 826),
       "READ 23 NOV 2026, 23:59 UTC \u2014 STORIES DATED 23 NOV ONLY", font=F(10, True), fill=RED)
d.text((16, 844), "LEFT OUT \u2014 NOT 23 NOV: Democrats reach 258 seats (22 Nov) \u00b7 Sparta II fire (22 Nov) \u00b7 El Chapo Isidro",
       font=F(11), fill=BLACK)
d.text((16, 860), "captured (22 Nov) \u00b7 EU-Indonesia pact (21 Nov) \u00b7 Nigeria boat (21 Nov) \u00b7 ICJ Myanmar ruling (19 Nov)",
       font=F(11), fill=BLACK)
d.text((16, 876), "NOT YET: Dymer search continues (14 missing) \u00b7 4 House races uncalled \u00b7 COP32 venue not set \u00b7 WHO evacuating trapped Ebola staff",
       font=F(11), fill=BLACK)

# ---------- footer ----------
d.text((16, 910), "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap \u00b7 BBC \u00b7 WSJ \u00b7 NYT \u00b7 ESPN \u00b7 Lowy Institute (Asia Power Index 2026).",
       font=F(10), fill=GRAY)
d.text((16, 924), "CHIPS: REPORTED = confirmed by wires \u00b7 CLAIM = one side's claim, not independently confirmed \u00b7 ONGOING = still developing",
       font=F(10), fill=GRAY)

# ---------- bottom bar ----------
d.rectangle([0, 944, W, H], fill=BLACK)
bt = "Scenes are drawn illustrations, not photographs.  \u00b7  THE WORLD TODAY \u2014 Monday 23 November 2026  \u00b7  31 stories  \u00b7  6 regions"
d.text(((W - tw(d, bt, F(13, True))) / 2, 972), bt, font=F(13, True), fill=GOLD)

img.save("entry.png")
print("saved entry.png", img.size)
