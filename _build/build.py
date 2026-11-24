#!/usr/bin/env python3
"""Generates the Canu and AutoMetronom landing pages in every language.

Usage: python3 _build/build.py            (writes next to this folder's parent)
Texts live in canu_strings.py and am_strings.py; the design lives in ../styles.css.
Legal pages are not generated: they are plain HTML files that only share the stylesheet.
"""
import shutil
from pathlib import Path

import am_strings
import canu_strings

ROOT = Path(__file__).resolve().parent.parent
CANU_STORE = "https://apps.apple.com/us/app/canu-sing/id6797062240"
# Written by _build/check_release.py (daily GitHub Action) once Apple lists AutoMetronom.
# With a URL the pages get a fixed App Store button and are opened to search engines.
_AM_STORE_FILE = Path(__file__).resolve().parent / "am_store_url.txt"
AM_STORE = _AM_STORE_FILE.read_text(encoding="utf-8").strip() if _AM_STORE_FILE.exists() else None
LANGS = ["de", "en", "es", "fr", "it", "nl", "pt", "ru", "sv"]
NAMES = canu_strings.NAMES
ROBOTS = '    <meta name="robots" content="noindex, nofollow" />\n'

# (folder, text language, html lang) – /international/ and /us/ are English hubs, /cn/ is Chinese.
CANU_PAGES = [(c, c, c) for c in LANGS] + [("international", "en", "en"), ("us", "en", "en-US"), ("cn", "zh", "zh-Hans")]


def head(t, lang, icon, css, index=True):
    return f'''<!doctype html>
<html lang="{lang}">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
{"" if index else ROBOTS}    <meta name="theme-color" content="#6330db" />
    <title>{t["title"]}</title>
    <meta name="description" content="{t["desc"]}" />
    <link rel="icon" type="image/png" href="{icon}" />
    <link rel="stylesheet" href="{css}?v=3" />
    <script src="{css.replace("styles.css", "assets/store.js")}" defer></script>
</head>
<body>
<a class="skip-link" href="#content">{t["skip"]}</a>'''


def switcher(current_dir, label, extra=""):
    items = ""
    for c in LANGS:
        current = ' aria-current="page"' if c == current_dir else ""
        items += f'<li><a{current} href="../{c}/index.html" lang="{c}" hreflang="{c}">{NAMES[c]}</a></li>'
    return f'<details class="locale-switcher"><summary>{label}</summary><ul class="locale-menu">{items}{extra}</ul></details>'


def legal_list(t, rows):
    out = []
    for name, privacy, terms, copy in rows:
        out.append(f'<li><strong>{t[name]}</strong><span><a href="{privacy}">{t["l_priv"]}</a>'
                   f'<a href="{terms}">{t["l_terms"]}</a><a href="{copy}">{t["l_copy"]}</a></span></li>')
    return "\n            ".join(out)


def shots(prefix, lang, label, base):
    return "\n            ".join(
        f'<img src="{base}assets/shots/{prefix}-{lang}-{n}.jpg" alt="{label} {n}" width="598" height="1300" loading="lazy" />'
        for n in range(1, 5))


PITCH_SVG = '''<svg class="pitch" role="img" aria-label="{art}" viewBox="0 0 560 560">
                <defs>
                    <linearGradient id="chip" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8e63f5" /><stop offset="1" stop-color="#6330db" /></linearGradient>
                    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="12" /></filter>
                </defs>
                <path d="M0 40H560M0 96H560M0 152H560M0 208H560M0 264H560M0 320H560M0 376H560M0 432H560M0 488H560M0 544H560" stroke="#e6dafc" stroke-width="1.5" />
                <path d="M410 0V560" stroke="#8e63f5" stroke-width="3" />
                <path d="M-10 488H110C160 488 160 320 210 320H300C350 320 350 152 400 152H410" fill="none" stroke="#1fc775" stroke-width="26" stroke-linecap="round" opacity=".4" filter="url(#glow)" />
                <path d="M-10 488H110C160 488 160 320 210 320H300C350 320 350 152 400 152H410" fill="none" stroke="#1fc775" stroke-width="10" stroke-linecap="round" />
                <g font-family="'Plus Jakarta Sans', sans-serif" font-weight="700" font-size="22" text-anchor="middle">
                    <rect x="24" y="458" width="84" height="60" rx="18" fill="url(#chip)" /><text x="66" y="496" fill="#fff">sol</text>
                    <rect x="212" y="290" width="84" height="60" rx="18" fill="url(#chip)" /><text x="254" y="328" fill="#fff">ti</text>
                    <rect x="368" y="122" width="84" height="60" rx="18" fill="url(#chip)" /><text x="410" y="160" fill="#fff">re</text>
                    <rect x="470" y="122" width="84" height="60" rx="18" fill="#eadfff" /><text x="512" y="160" fill="#6330db">mi</text>
                </g>
                <circle cx="410" cy="152" r="9" fill="#f2a65a" stroke="#fff" stroke-width="3" />
            </svg>'''


def canu_page(folder, lang, html_lang):
    t = canu_strings.S[lang]
    shot_lang = "en" if lang == "zh" else lang
    sib_lang = "en" if lang == "zh" else lang
    copy = {"de": "../de/copyright/index.html", "zh": "../cn/copyright/index.html"}.get(lang, "../international/copyright/index.html")
    intl_copy = "../international/copyright/index.html"
    rows = [
        ("r_ch", "../ch/datenschutz/index.html", "../ch/nutzungsbedingungen/index.html", copy),
        ("r_eu", "../eu/datenschutz/index.html", "../eu/nutzungsbedingungen/index.html", copy),
        ("r_us", "../us/privacy/index.html", "../us/terms/index.html", intl_copy),
        ("r_cn", "../cn/privacy/index.html", "../cn/terms/index.html", "../cn/copyright/index.html"),
        ("r_other", "../international/privacy/index.html", "../international/terms/index.html", intl_copy),
    ]
    if lang == "zh":
        sw = switcher(folder, "简体中文", '<li><a aria-current="page" href="index.html" lang="zh-Hans">简体中文</a></li>')
    else:
        sw = switcher(folder if folder in LANGS else "en", NAMES[lang])
    stairs = "\n                ".join(
        f'<article class="stair"><span class="chip" aria-hidden="true">{chip}</span><h3>{t[f"f{i}t"]}</h3><p>{t[f"f{i}p"]}</p></article>'
        for i, chip in enumerate(["do", "re", "mi", "fa"], 1))
    more = "\n                ".join(f'<div class="fact"><h3>{t[f"m{i}t"]}</h3><p>{t[f"m{i}p"]}</p></div>' for i in range(1, 7))
    pro = "".join(f"<li>{t[f'p{i}']}</li>" for i in range(1, 6))
    faq = "\n                ".join(f'<details class="faq"><summary>{t[f"q{i}"]}</summary><p>{t[f"a{i}"]}</p></details>' for i in range(1, 5))
    return f'''{head(t, html_lang, "../assets/canu-logo.png", "../styles.css")}
<header class="site-header shell">
    <nav class="nav" aria-label="Canu">
        <a class="brand" href="index.html"><img src="../assets/canu-logo.png" alt="" width="44" height="44" />Canu</a>
        <div class="nav-actions">
            <ul class="nav-links">
                <li><a href="#features">{t["nav_features"]}</a></li>
                <li><a href="#support">{t["nav_support"]}</a></li>
                <li><a href="#legal">{t["nav_legal"]}</a></li>
            </ul>
            {sw}
            <a class="button-dark" href="{CANU_STORE}">{t["store"]}</a>
        </div>
    </nav>
</header>

<main id="content">
    <section class="hero shell" aria-labelledby="hero-title">
        <div class="hero-copy">
            <h1 id="hero-title"><span class="canu-title-a">{t["h1a"]}</span><span class="canu-title-b">{t["h1b"]}</span></h1>
            <p class="lead">{t["lead"]}</p>
            <div class="cta-row">
                <a class="button" href="{CANU_STORE}">{t["store"]}</a>
                <span class="cta-note">{t["note"]}</span>
            </div>
        </div>
        <div class="hero-art">
            {PITCH_SVG.format(art=t["art"])}
        </div>
    </section>

    <section class="band" id="features" aria-labelledby="features-title">
        <div class="shell section stack">
            <h2 class="h2 narrow" id="features-title">{t["f_title"]}</h2>
            <div class="stairs">
                {stairs}
            </div>
        </div>
    </section>

    <section class="shell section stack" aria-labelledby="more-title">
        <h2 class="h2 narrow" id="more-title">{t["m_title"]}</h2>
        <div class="facts">
                {more}
        </div>
    </section>

    <section class="band" aria-labelledby="shots-title">
        <div class="shell section stack">
            <h2 class="h2 narrow" id="shots-title">{t["s_title"]}</h2>
            <div class="shots">
            {shots("canu", shot_lang, t["shot"], "../")}
            </div>
        </div>
    </section>

    <section class="shell section" aria-labelledby="pro-title">
        <div class="pro">
            <div class="pro-copy">
                <h2 class="h2" id="pro-title">{t["p_title"]}</h2>
                <p>{t["p_sub"]}</p>
            </div>
            <ul class="pro-list">{pro}</ul>
        </div>
    </section>

    <section class="band" id="support" aria-labelledby="support-title">
        <div class="shell section two-col">
            <div>
                <h2 class="h2" id="support-title">{t["sup_title"]}</h2>
                <p>{t["sup_p"]}</p>
                <p class="hint">{t["sup_hint"]}</p>
            </div>
            <div>
                <a class="mail-card" href="mailto:support@canusing.com?subject=Canu%20Support"><strong>{t["sup1t"]}</strong>{t["sup1p"]}<em>support@canusing.com</em></a>
                <a class="mail-card" href="mailto:feedback@canusing.com?subject=Canu%20Feedback"><strong>{t["sup2t"]}</strong>{t["sup2p"]}<em>feedback@canusing.com</em></a>
            </div>
        </div>
        <div class="shell faq-block" aria-labelledby="faq-title">
            <h3 class="h2-small" id="faq-title">{t["q_title"]}</h3>
            <div class="faq-list">
                {faq}
            </div>
        </div>
    </section>

    <span class="anchor" id="rechtliches"></span>
    <section class="shell section legal" id="legal" aria-labelledby="legal-title">
        <div class="legal-intro">
            <h2 class="h2-small" id="legal-title">{t["leg_title"]}</h2>
            <p>{t["leg_p"]}</p>
        </div>
        <ul class="legal-list">
            {legal_list(t, rows)}
        </ul>
    </section>
</main>

<footer class="site-footer">
    <div class="footer-inner shell">
        <div class="footer-main">
            <a class="brand" href="index.html"><img src="../assets/canu-logo.png" alt="" width="40" height="40" />Canu</a>
            <p>© 2026 Aleksander Woichansky. {t["rights"]}</p>
            <div class="footer-links"><a href="mailto:support@canusing.com">{t["contact"]}</a><a href="#legal">{t["leg_title"]}</a></div>
        </div>
        <a class="sibling" hidden data-am-live href="../autometronom/{sib_lang}/index.html"><img src="../autometronom/assets/autometronom-icon.png" alt="" width="64" height="64" /><span><small>{t["also"]}</small><strong>AutoMetronom</strong>{t["sibling"]}</span></a>
    </div>
</footer>
</body>
</html>
'''


BAR_HEIGHTS = [16, 34, 58, 80, 46, 66, 30, 72, 52, 76, 40, 60, 26, 14]


def am_page(lang):
    common = canu_strings.S[lang]
    t = {**common, **am_strings.S[lang]}
    anchors = [("r_ch", "switzerland", "ch/nutzungsbedingungen"), ("r_eu", "europe", "eu/nutzungsbedingungen"),
               ("r_us", "united-states", "us/terms"), ("r_cn", "china", "cn/terms"), ("r_other", "other-regions", "international/terms")]
    rows = [(name, f"privacy/index.html#{anchor}", f"../{terms}/index.html", "copyright/index.html") for name, anchor, terms in anchors]
    cta = f'<a class="button" href="{AM_STORE}">{t["store"]}</a>' if AM_STORE else f'<span class="button is-soon" data-am-store="{t["store"]}">{t["soon"]}</span>'
    bars = ""
    for i, h in enumerate(BAR_HEIGHTS):
        motion = f"animation-delay: {(i - 1) / 10:g}s" if 0 < i < 12 else "animation: none"
        bars += f'<span style="height: {h}px; {motion}"></span>'
    steps = "\n            ".join(
        f'<li><span class="step-no" aria-hidden="true">{i}</span><h3>{t[f"s{i}t"]}</h3><p>{t[f"s{i}p"]}</p></li>' for i in range(1, 4))
    facts = "\n                ".join(f'<div class="fact"><h3>{t[f"f{i}t"]}</h3><p>{t[f"f{i}p"]}</p></div>' for i in range(1, 7))
    privacy = "".join(f'<div><dt>{t[f"pv{i}t"]}</dt><dd>{t[f"pv{i}p"]}</dd></div>' for i in range(1, 4))
    icon = "../assets/autometronom-icon.png"
    return f'''{head(t, lang, icon, "../../styles.css", index=AM_STORE is not None)}
<div class="am-top">
    <header class="site-header shell">
        <nav class="nav" aria-label="AutoMetronom">
            <a class="brand" href="index.html"><img src="{icon}" alt="" width="44" height="44" />AutoMetronom</a>
            <div class="nav-actions">
                <ul class="nav-links">
                    <li><a href="#how">{t["nav_how"]}</a></li>
                    <li><a href="#support">{t["nav_support"]}</a></li>
                    <li><a href="#legal">{t["nav_legal"]}</a></li>
                </ul>
                {switcher(lang, NAMES[lang])}
            </div>
        </nav>
    </header>

    <section class="hero shell" aria-labelledby="hero-title">
        <div class="hero-copy">
            <h1 class="am-title" id="hero-title">{t["h1"]}</h1>
            <p class="lead">{t["lead"]}</p>
            <div class="cta-row">
                {cta}
                <div class="beats" role="img" aria-label="111 BPM · 4/4">
                    <span class="beat is-one">1</span><span class="beat">2</span><span class="beat">3</span><span class="beat">4</span>
                    <span class="beats-label">111 BPM · 4/4</span>
                </div>
            </div>
        </div>
        <div class="hero-art">
            <div class="stage" aria-hidden="true">
                <svg class="stage-wave" viewBox="0 0 540 540">
                    <path d="M-20 330C70 250 130 250 220 330S380 430 470 350S560 300 580 300" fill="none" stroke="#fff" stroke-width="3" />
                    <circle cx="-20" cy="330" r="13" fill="#7c4df0" />
                    <circle cx="560" cy="304" r="13" fill="#7c4df0" />
                    <circle cx="220" cy="330" r="6" fill="#faf5ff" stroke="#d5c6f7" stroke-width="2" />
                    <circle cx="400" cy="398" r="6" fill="#faf5ff" stroke="#d5c6f7" stroke-width="2" />
                </svg>
                <div class="float float-wave"><span class="pill-auto">Auto</span><div class="bars">{bars}</div></div>
                <div class="float float-song">
                    <span class="song-icon"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#6330db" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18V5l10-2v13" /><circle cx="6.5" cy="18" r="2.5" fill="#6330db" /><circle cx="16.5" cy="16" r="2.5" fill="#6330db" /></svg></span>
                    <span class="song-text"><strong>{t["song"]}</strong>{t["song_sub"]}<em>{t["last"]}: 111 BPM · 4/4</em></span>
                </div>
                <div class="float float-tempo">Tempo<span><strong>111</strong>BPM</span></div>
            </div>
        </div>
    </section>
</div>

<main id="content">
    <section class="shell section stack" id="how" aria-labelledby="steps-title">
        <h2 class="h2" id="steps-title">{t["how_title"]}</h2>
        <ol class="steps">
            {steps}
        </ol>
    </section>

    <section class="band" aria-labelledby="features-title">
        <div class="shell section stack">
            <h2 class="h2 narrow" id="features-title">{t["f_title"]}</h2>
            <div class="facts">
                {facts}
            </div>
        </div>
    </section>

    <section class="shell section stack" aria-labelledby="shots-title">
        <div class="split-head">
            <h2 class="h2 narrow" id="shots-title">{t["shots_title"]}</h2>
            <p>{t["shots_p"]}</p>
        </div>
        <div class="shots">
            {shots("am", lang, t["shot"], "../../")}
        </div>
    </section>

    <section class="shell" aria-labelledby="privacy-title" style="padding-bottom: 96px">
        <div class="privacy">
            <div class="privacy-copy">
                <h2 class="h2" id="privacy-title">{t["pv_title"]}</h2>
                <a href="privacy/index.html">{t["pv_link"]}</a>
            </div>
            <dl>{privacy}</dl>
        </div>
    </section>

    <section class="band" id="support" aria-labelledby="support-title">
        <div class="shell section two-col">
            <div>
                <h2 class="h2" id="support-title">{t["sup_title"]}</h2>
                <p>{t["sup_p"]}</p>
            </div>
            <div>
                <a class="mail-card" href="mailto:support@canusing.com?subject=AutoMetronom%20Support"><strong>{t["sup1t"]}</strong>{t["sup1p"]}<em>support@canusing.com</em></a>
                <p class="hint">{t["sup_hint"]}</p>
            </div>
        </div>
    </section>

    <section class="shell section legal" id="legal" aria-labelledby="legal-title">
        <div class="legal-intro">
            <h2 class="h2-small" id="legal-title">{t["leg_title"]}</h2>
            <p>{t["leg_p"]}</p>
        </div>
        <ul class="legal-list">
            {legal_list(t, rows)}
        </ul>
    </section>
</main>

<footer class="site-footer">
    <div class="footer-inner shell">
        <div class="footer-main">
            <a class="brand" href="index.html"><img src="{icon}" alt="" width="40" height="40" />AutoMetronom</a>
            <p>© 2026 Aleksander Woichansky. {t["rights"]}</p>
            <p>{t["cr_tempo"]}: <a href="https://getsongbpm.com">GetSongBPM.com</a> · {t["cr_song"]}: Shazam (Apple)</p>
            <div class="footer-links"><a href="mailto:support@canusing.com">{t["contact"]}</a><a href="#legal">{t["leg_title"]}</a></div>
        </div>
        <a class="sibling" href="../../{lang}/index.html"><img src="../../assets/canu-logo.png" alt="" width="64" height="64" /><span><small>{t["also"]}</small><strong>Canu</strong>{t["sibling"]}</span></a>
    </div>
</footer>
</body>
</html>
'''


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main():
    for folder, lang, html_lang in CANU_PAGES:
        write(ROOT / folder / "index.html", canu_page(folder, lang, html_lang))
    am = ROOT / "autometronom"
    for lang in LANGS:
        write(am / lang / "index.html", am_page(lang))
        # The app opens /autometronom/<language>/privacy/. Languages without their own legal
        # translation get the English text so that the link never ends in a 404.
        for sub in ("privacy", "copyright"):
            target = am / lang / sub / "index.html"
            if not target.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(am / "en" / sub / "index.html", target)
    print(f"built {len(CANU_PAGES)} Canu pages and {len(LANGS)} AutoMetronom pages in {ROOT}")


if __name__ == "__main__":
    main()
