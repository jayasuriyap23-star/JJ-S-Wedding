from pathlib import Path
import math
import random

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "outputs" / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)


def lerp(a, b, t):
    return int(a + (b - a) * t)


def gradient(size, top, bottom):
    w, h = size
    img = Image.new("RGB", size)
    px = img.load()
    for y in range(h):
        t = y / max(1, h - 1)
        color = tuple(lerp(top[i], bottom[i], t) for i in range(3))
        for x in range(w):
            px[x, y] = color
    return img


def add_glow(draw, cx, cy, radius, color):
    for r in range(radius, 0, -8):
        alpha = int(105 * (r / radius) ** 1.8)
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=color + (alpha,))


def draw_pillar(draw, x, y, w, h):
    gold_dark = (116, 75, 20, 255)
    gold = (223, 169, 67, 255)
    gold_light = (255, 225, 137, 255)
    draw.rounded_rectangle((x, y, x + w, y + h), radius=28, fill=(157, 92, 31, 255), outline=gold_light, width=3)
    for i in range(9):
        px = x + 16 + i * (w - 32) / 8
        shade = gold_light if i % 2 == 0 else gold_dark
        draw.line((px, y + 30, px, y + h - 30), fill=shade, width=3)
    for yy in (y + 32, y + h - 58):
        draw.rounded_rectangle((x - 22, yy, x + w + 22, yy + 42), radius=12, fill=gold, outline=gold_light, width=3)
        for i in range(7):
            cx = x + 12 + i * (w - 24) / 6
            draw.ellipse((cx - 9, yy + 10, cx + 9, yy + 28), fill=(107, 29, 32, 255), outline=gold_light)
    for yy in range(y + 105, y + h - 118, 100):
        draw.arc((x + 16, yy, x + w - 16, yy + 64), 180, 360, fill=gold_light, width=3)
        draw.arc((x + 16, yy + 24, x + w - 16, yy + 88), 0, 180, fill=(96, 28, 29, 255), width=2)


def draw_bell(draw, cx, cy, scale=1):
    gold = (236, 183, 72, 255)
    dark = (104, 55, 20, 255)
    w, h = 46 * scale, 58 * scale
    draw.line((cx, cy - 50 * scale, cx, cy - 4 * scale), fill=gold, width=max(2, int(4 * scale)))
    draw.arc((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), 200, -20, fill=gold, width=max(2, int(5 * scale)))
    draw.pieslice((cx - w / 2, cy - 10 * scale, cx + w / 2, cy + h), 180, 360, fill=gold, outline=(255, 222, 135, 255))
    draw.ellipse((cx - 11 * scale, cy + 40 * scale, cx + 11 * scale, cy + 60 * scale), fill=dark)


def draw_lotus(draw, cx, cy, scale, fill, outline):
    petals = 12
    for i in range(petals):
        angle = i * math.tau / petals
        px = cx + math.cos(angle) * 20 * scale
        py = cy + math.sin(angle) * 10 * scale
        draw.ellipse((px - 11 * scale, py - 19 * scale, px + 11 * scale, py + 19 * scale), fill=fill, outline=outline)
    draw.ellipse((cx - 18 * scale, cy - 12 * scale, cx + 18 * scale, cy + 12 * scale), fill=(255, 236, 176, 230), outline=outline)


def draw_peacock_feather(draw, x, y, scale):
    stem = (36, 102, 70, 210)
    draw.line((x, y + 70 * scale, x + 26 * scale, y - 62 * scale), fill=stem, width=max(2, int(4 * scale)))
    draw.ellipse((x - 25 * scale, y - 62 * scale, x + 75 * scale, y + 26 * scale), fill=(23, 91, 85, 95), outline=(255, 216, 123, 180), width=max(1, int(2 * scale)))
    draw.ellipse((x + 2 * scale, y - 40 * scale, x + 50 * scale, y + 8 * scale), fill=(34, 139, 126, 160), outline=(255, 229, 146, 190))
    draw.ellipse((x + 15 * scale, y - 27 * scale, x + 38 * scale, y - 4 * scale), fill=(39, 74, 151, 210), outline=(255, 234, 159, 220))
    draw.ellipse((x + 22 * scale, y - 20 * scale, x + 31 * scale, y - 11 * scale), fill=(255, 214, 93, 230))


def draw_ganesha(draw, cx, cy, scale):
    gold = (255, 218, 122, 230)
    deep = (74, 18, 19, 245)
    aura = (255, 204, 90, 42)
    for r in range(int(145 * scale), int(45 * scale), -16):
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=aura)
    draw.ellipse((cx - 70 * scale, cy - 78 * scale, cx + 70 * scale, cy + 62 * scale), fill=deep, outline=gold, width=max(2, int(4 * scale)))
    draw.ellipse((cx - 118 * scale, cy - 45 * scale, cx - 42 * scale, cy + 58 * scale), fill=deep, outline=gold, width=max(2, int(4 * scale)))
    draw.ellipse((cx + 42 * scale, cy - 45 * scale, cx + 118 * scale, cy + 58 * scale), fill=deep, outline=gold, width=max(2, int(4 * scale)))
    draw.polygon([(cx - 48 * scale, cy - 86 * scale), (cx, cy - 172 * scale), (cx + 48 * scale, cy - 86 * scale)], fill=(197, 125, 42, 245), outline=gold)
    draw.rounded_rectangle((cx - 22 * scale, cy + 24 * scale, cx + 28 * scale, cy + 146 * scale), radius=int(24 * scale), fill=deep, outline=gold, width=max(2, int(4 * scale)))
    draw.arc((cx - 28 * scale, cy + 82 * scale, cx + 92 * scale, cy + 178 * scale), 92, 270, fill=gold, width=max(2, int(6 * scale)))
    draw.ellipse((cx - 25 * scale, cy - 12 * scale, cx - 12 * scale, cy + 1 * scale), fill=gold)
    draw.ellipse((cx + 12 * scale, cy - 12 * scale, cx + 25 * scale, cy + 1 * scale), fill=gold)
    draw.line((cx - 20 * scale, cy + 54 * scale, cx + 20 * scale, cy + 54 * scale), fill=gold, width=max(2, int(3 * scale)))


def draw_venkateswara(draw, cx, cy, scale):
    gold = (255, 222, 137, 235)
    deep = (30, 8, 12, 250)
    maroon = (95, 18, 28, 250)
    for r in range(int(190 * scale), int(70 * scale), -18):
        draw.ellipse((cx - r, cy - r * 1.05, cx + r, cy + r * 1.05), fill=(255, 204, 82, 28))
    draw.rounded_rectangle((cx - 64 * scale, cy - 54 * scale, cx + 64 * scale, cy + 190 * scale), radius=int(52 * scale), fill=deep, outline=gold, width=max(2, int(5 * scale)))
    draw.polygon([(cx - 66 * scale, cy - 58 * scale), (cx, cy - 226 * scale), (cx + 66 * scale, cy - 58 * scale)], fill=(195, 121, 42, 250), outline=gold)
    for i in range(5):
        y = cy - 58 * scale - i * 27 * scale
        draw.line((cx - (57 - i * 9) * scale, y, cx + (57 - i * 9) * scale, y), fill=gold, width=max(1, int(3 * scale)))
    draw.ellipse((cx - 36 * scale, cy - 44 * scale, cx + 36 * scale, cy + 28 * scale), fill=deep, outline=gold, width=max(2, int(3 * scale)))
    draw.line((cx, cy - 34 * scale, cx, cy + 130 * scale), fill=(255, 238, 178, 235), width=max(2, int(5 * scale)))
    draw.line((cx - 22 * scale, cy + 30 * scale, cx + 22 * scale, cy + 30 * scale), fill=(255, 238, 178, 235), width=max(2, int(4 * scale)))
    draw.arc((cx - 152 * scale, cy - 22 * scale, cx - 58 * scale, cy + 120 * scale), 245, 70, fill=gold, width=max(2, int(7 * scale)))
    draw.arc((cx + 58 * scale, cy - 22 * scale, cx + 152 * scale, cy + 120 * scale), 110, 295, fill=gold, width=max(2, int(7 * scale)))
    draw.ellipse((cx - 176 * scale, cy - 55 * scale, cx - 118 * scale, cy + 3 * scale), outline=gold, width=max(2, int(5 * scale)))
    draw.ellipse((cx + 118 * scale, cy - 55 * scale, cx + 176 * scale, cy + 3 * scale), outline=gold, width=max(2, int(5 * scale)))
    draw.rounded_rectangle((cx - 84 * scale, cy + 140 * scale, cx + 84 * scale, cy + 198 * scale), radius=int(16 * scale), fill=maroon, outline=gold, width=max(2, int(3 * scale)))


def draw_shiva_parvati(draw, cx, cy, scale):
    gold = (255, 220, 134, 220)
    deep = (50, 12, 18, 250)
    blue = (57, 93, 123, 210)
    rose = (135, 36, 58, 225)
    for r in range(int(170 * scale), int(55 * scale), -17):
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 211, 101, 31))
    draw.ellipse((cx - 88 * scale, cy - 78 * scale, cx - 2 * scale, cy + 8 * scale), fill=blue, outline=gold, width=max(2, int(4 * scale)))
    draw.ellipse((cx + 4 * scale, cy - 68 * scale, cx + 86 * scale, cy + 14 * scale), fill=rose, outline=gold, width=max(2, int(4 * scale)))
    draw.rounded_rectangle((cx - 105 * scale, cy + 2 * scale, cx - 4 * scale, cy + 165 * scale), radius=int(42 * scale), fill=deep, outline=gold, width=max(2, int(4 * scale)))
    draw.rounded_rectangle((cx + 2 * scale, cy + 10 * scale, cx + 102 * scale, cy + 170 * scale), radius=int(42 * scale), fill=deep, outline=gold, width=max(2, int(4 * scale)))
    draw.arc((cx - 103 * scale, cy - 112 * scale, cx - 34 * scale, cy - 42 * scale), 110, 330, fill=gold, width=max(2, int(5 * scale)))
    draw.polygon([(cx + 25 * scale, cy - 70 * scale), (cx + 45 * scale, cy - 132 * scale), (cx + 67 * scale, cy - 70 * scale)], fill=(205, 127, 44, 240), outline=gold)
    draw.line((cx - 142 * scale, cy - 112 * scale, cx - 142 * scale, cy + 158 * scale), fill=gold, width=max(2, int(5 * scale)))
    for dy in (-95, -76, -57):
        draw.line((cx - 178 * scale, cy + dy * scale, cx - 106 * scale, cy + dy * scale), fill=gold, width=max(2, int(4 * scale)))
    draw.ellipse((cx - 23 * scale, cy - 35 * scale, cx - 11 * scale, cy - 23 * scale), fill=gold)
    draw.ellipse((cx + 25 * scale, cy - 30 * scale, cx + 37 * scale, cy - 18 * scale), fill=gold)


def draw_carving_panel(draw, x, y, w, h):
    draw.rounded_rectangle((x, y, x + w, y + h), radius=18, fill=(87, 24, 24, 120), outline=(255, 219, 136, 165), width=2)
    for i in range(4):
        cx = x + (i + 0.5) * w / 4
        draw_lotus(draw, cx, y + h * 0.32, 0.55, (169, 50, 59, 210), (255, 218, 132, 205))
        draw.arc((cx - 36, y + h * 0.48, cx + 36, y + h * 0.86), 190, 350, fill=(255, 220, 133, 150), width=3)


def hero():
    w, h = 1800, 1200
    base = gradient((w, h), (47, 8, 18), (12, 5, 9)).convert("RGBA")
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow, "RGBA")
    add_glow(gd, w // 2, 350, 560, (255, 202, 94))
    add_glow(gd, w // 2, 930, 440, (185, 25, 28))
    base = Image.alpha_composite(base, glow.filter(ImageFilter.GaussianBlur(16)))
    draw = ImageDraw.Draw(base, "RGBA")

    for i in range(22):
        x = int(i * w / 21)
        draw.line((x, 0, w // 2, 720), fill=(255, 226, 148, 18), width=5)

    draw.rectangle((0, 930, w, h), fill=(92, 24, 24, 230))
    for y in range(930, h, 42):
        draw.line((0, y, w, y), fill=(239, 189, 86, 34), width=2)
    for x in range(0, w, 80):
        draw.line((x, 930, x + 240, h), fill=(255, 235, 159, 22), width=2)

    # Temple tiers and sanctum.
    draw.rectangle((220, 180, 1580, 980), fill=(72, 17, 23, 205), outline=(239, 191, 93, 220), width=5)
    for level in range(6):
        y = 160 - level * 28
        inset = level * 90
        draw.rounded_rectangle((210 + inset, y, 1590 - inset, y + 42), radius=10, fill=(176, 105, 38, 255), outline=(255, 222, 132, 255), width=3)
        for x in range(250 + inset, 1550 - inset, 76):
            draw.polygon([(x, y + 42), (x + 28, y + 5), (x + 56, y + 42)], fill=(111, 34, 32, 255), outline=(225, 169, 76, 255))

    draw.rounded_rectangle((560, 295, 1240, 990), radius=340, fill=(29, 8, 13, 245), outline=(255, 214, 118, 255), width=7)
    for r in range(310, 430, 28):
        draw.arc((900 - r, 285, 900 + r, 285 + r * 1.6), 180, 360, fill=(218, 159, 58, 170), width=4)
    draw.rectangle((635, 590, 1165, 990), fill=(35, 10, 14, 250), outline=(207, 143, 50, 255), width=4)
    draw.line((900, 590, 900, 990), fill=(207, 143, 50, 255), width=4)
    for x in (705, 1095):
        draw.ellipse((x - 16, 775, x + 16, 807), fill=(246, 201, 93, 255))

    for x in (260, 430, 1280, 1450):
        draw_pillar(draw, x, 255, 110, 730)

    # Intricate carved friezes, lotus panels, peacock feathers, and divine sanctum motifs.
    draw_carving_panel(draw, 520, 210, 760, 88)
    draw_carving_panel(draw, 520, 870, 760, 72)
    for x in range(585, 1220, 90):
        draw_lotus(draw, x, 252, 0.48, (244, 145, 64, 205), (255, 225, 148, 210))
    draw_peacock_feather(draw, 505, 522, 1.0)
    draw_peacock_feather(draw, 1240, 522, 1.0)
    draw_ganesha(draw, 500, 610, 0.72)
    draw_venkateswara(draw, 900, 585, 0.74)
    draw_shiva_parvati(draw, 1300, 615, 0.72)

    for x in range(330, 1500, 95):
        draw.ellipse((x - 20, 238, x + 20, 278), fill=(238, 126, 32, 255))
        draw.ellipse((x + 16, 248, x + 44, 278), fill=(255, 244, 216, 255))
        draw.line((x, 282, x + 24, 320), fill=(47, 118, 55, 255), width=7)

    for x in (520, 680, 1120, 1280):
        draw_bell(draw, x, 295, 1.05)

    # Rangoli and diyas.
    cx, cy = 900, 1010
    for r, color in [(170, (255, 223, 123, 200)), (124, (244, 127, 43, 210)), (82, (255, 246, 221, 220)), (42, (151, 34, 45, 230))]:
        draw.ellipse((cx - r, cy - r * 0.42, cx + r, cy + r * 0.42), outline=color, width=5)
    for i in range(16):
        a = i * math.tau / 16
        px = cx + math.cos(a) * 128
        py = cy + math.sin(a) * 54
        draw.ellipse((px - 16, py - 16, px + 16, py + 16), fill=(255, 236, 167, 210))

    for x in (360, 500, 1300, 1440):
        draw.ellipse((x - 52, 1018, x + 52, 1060), fill=(148, 49, 27, 255), outline=(246, 178, 69, 255), width=3)
        draw.polygon([(x, 980), (x - 18, 1024), (x + 20, 1024)], fill=(255, 205, 69, 245))
        add_glow(draw, x, 1012, 76, (255, 187, 74))

    random.seed(9)
    for _ in range(360):
        x = random.randint(0, w - 1)
        y = random.randint(0, h - 1)
        r = random.choice([1, 1, 2, 3])
        a = random.randint(30, 145)
        draw.ellipse((x - r, y - r, x + r, y + r), fill=(255, 224, 137, a))

    vignette = Image.new("L", (w, h), 0)
    vd = ImageDraw.Draw(vignette)
    vd.ellipse((-220, -130, w + 220, h + 180), fill=255)
    vignette = vignette.filter(ImageFilter.GaussianBlur(90))
    dark = Image.new("RGBA", (w, h), (0, 0, 0, 115))
    base = Image.composite(base, Image.alpha_composite(base, dark), vignette)
    base.convert("RGB").save(ASSETS / "temple-entrance.png", quality=92, optimize=True)


def silk_texture():
    w, h = 1200, 900
    img = gradient((w, h), (86, 10, 25), (35, 6, 15)).convert("RGBA")
    draw = ImageDraw.Draw(img, "RGBA")
    random.seed(4)
    for y in range(-h, h * 2, 18):
        color = (255, 213, 128, random.randint(10, 26))
        draw.line((-80, y, w + 80, y + 420), fill=color, width=random.choice([1, 2]))
    for x in range(-50, w + 50, 64):
        draw.arc((x, 90, x + 180, 350), 210, 330, fill=(255, 218, 137, 36), width=2)
        draw.arc((x, 460, x + 180, 720), 30, 150, fill=(255, 218, 137, 24), width=2)
    img = img.filter(ImageFilter.GaussianBlur(0.35))
    img.convert("RGB").save(ASSETS / "silk-texture.png", quality=86, optimize=True)


hero()
silk_texture()
