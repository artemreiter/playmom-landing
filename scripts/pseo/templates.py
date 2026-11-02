# -*- coding: utf-8 -*-
"""Shared HTML fragments for the PlayMom pSEO site: head/meta, nav, CTA,
breadcrumbs, footer, JSON-LD builders. Pure string templates, no framework.
"""
import html
import json

from ui_strings import HTML_LANG, LANG_NAME, SITE_NAME, UI

SITE_ORIGIN = "https://playmom.app"
APP_STORE_URL = "https://apps.apple.com/app/id6759934367"
APP_ID = "6759934367"


def esc(s):
    return html.escape(str(s), quote=True)


def html_head(lang, title, description, canonical_path, hreflang_map, og_image=None):
    """hreflang_map: {lang: path} for every language this content exists in.
    canonical_path and hreflang paths are site-root-relative, e.g. '/en/games/...'.
    """
    alt_links = []
    for alt_lang, path in sorted(hreflang_map.items()):
        alt_links.append(
            f'<link rel="alternate" hreflang="{HTML_LANG[alt_lang]}" href="{SITE_ORIGIN}{path}">'
        )
    if "en" in hreflang_map:
        alt_links.append(
            f'<link rel="alternate" hreflang="x-default" href="{SITE_ORIGIN}{hreflang_map["en"]}">'
        )
    og_image_tag = f'<meta property="og:image" content="{esc(og_image)}">' if og_image else ""
    return f"""<!DOCTYPE html>
<html lang="{HTML_LANG[lang]}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{SITE_ORIGIN}{canonical_path}">
{chr(10).join(alt_links)}
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
{og_image_tag}
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE_ORIGIN}{canonical_path}">
<meta name="twitter:card" content="summary_large_image">
<meta name="apple-itunes-app" content="app-id={APP_ID}">
<link rel="icon" href="/logo.png" type="image/png">
<link rel="stylesheet" href="/assets/style.css">
</head>
"""


def nav_header(lang, lang_switch_map):
    """lang_switch_map: {lang: path} equivalent content in other languages."""
    options = []
    for alt_lang in sorted(lang_switch_map):
        path = lang_switch_map[alt_lang]
        cls = "lang-current" if alt_lang == lang else ""
        options.append(f'<a href="{path}" class="{cls}">{LANG_NAME[alt_lang]}</a>')
    return f"""<header class="site-header">
  <a href="/{lang}/" class="brand"><img src="/logo.png" alt="{SITE_NAME}" width="32" height="32">{SITE_NAME}</a>
  <nav class="lang-switch">{"".join(options)}</nav>
</header>
"""


def breadcrumb(items):
    """items: list of (label, path_or_None). None path means current page."""
    parts = []
    for label, path in items:
        if path:
            parts.append(f'<a href="{path}">{esc(label)}</a>')
        else:
            parts.append(f'<span aria-current="page">{esc(label)}</span>')
    return f'<nav class="breadcrumb" aria-label="Breadcrumb">{" &rsaquo; ".join(parts)}</nav>\n'


def cta_block(lang, ct_token, heading=None):
    heading_html = f"<h2>{esc(heading)}</h2>" if heading else ""
    url = f"{APP_STORE_URL}?ct={ct_token}"
    return f"""<section class="cta-block">
  {heading_html}
  <a href="{url}" class="cta-button">{esc(UI['cta_button'][lang])}</a>
  <p class="cta-sub">{esc(UI['cta_sub'][lang])}</p>
</section>
"""


def locked_card(lang, more_steps_text, subscription_line, ct_token):
    url = f"{APP_STORE_URL}?ct={ct_token}"
    return f"""<div class="locked-card">
  <p class="locked-steps">{esc(more_steps_text)}</p>
  <p class="locked-sub">{esc(subscription_line)}</p>
  <a href="{url}" class="cta-button">{esc(UI['cta_button'][lang])}</a>
</div>
"""


def footer(lang):
    return f"""<footer class="site-footer">
  <p>&copy; 2026 {SITE_NAME} &middot; <a href="https://artemreiter.github.io/playmom-legal/">Privacy</a> &middot; <a href="/">playmom.app</a></p>
</footer>
"""


def jsonld_script(data):
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>\n'


def howto_jsonld(title, description, image_url, materials, steps, total_minutes):
    data = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": title,
        "description": description,
        "image": image_url,
        "step": [
            {"@type": "HowToStep", "position": i + 1, "text": s}
            for i, s in enumerate(steps)
        ],
    }
    if materials:
        data["supply"] = [{"@type": "HowToSupply", "name": m} for m in materials]
    if total_minutes:
        data["totalTime"] = f"PT{int(total_minutes)}M"
    return jsonld_script(data)


def breadcrumb_jsonld(items):
    """items: list of (label, absolute_url_or_None)."""
    elements = []
    for i, (label, path) in enumerate(items, 1):
        entry = {"@type": "ListItem", "position": i, "name": label}
        if path:
            entry["item"] = f"{SITE_ORIGIN}{path}"
        elements.append(entry)
    return jsonld_script({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": elements,
    })


def page_shell(lang, head, header, breadcrumb_html, main_html, cta_html, footer_html, jsonld_blocks=""):
    return f"""{head}{jsonld_blocks}<body>
{header}
<main>
{breadcrumb_html}{main_html}
{cta_html}
</main>
{footer_html}
</body>
</html>
"""
