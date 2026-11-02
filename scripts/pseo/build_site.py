#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Builds the PlayMom programmatic SEO site (game pages, age/goal hubs,
language homes, sitemaps, robots.txt) into dist/. Run fetch_metadata.py
first. Output is static HTML, mobile first, one shared CSS file, no JS
framework. Does not touch the live git repo; copy dist/ into it
separately.
"""
import datetime
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from data_loader import build_games, load_editorial, load_ids, load_metadata, siblings_for
from slugify import short_id, slugify
from ui_strings import (
    AGE_BAND_LABEL, AGE_BANDS, AGE_WORD, CATEGORY_LABEL, CATEGORY_ORDER,
    CATEGORY_SLUG, CONTEXT_LABEL, GAMES_WORD, GOAL_WORD, LANGS, MINUTES_LABEL,
    MONTHS_LABEL, SITE_NAME, UI, YEARS_LABEL,
)
from templates import (
    SITE_ORIGIN, breadcrumb, breadcrumb_jsonld, cta_block, esc, footer,
    html_head, howto_jsonld, nav_header, page_shell,
)

DIST = HERE.parent / "dist"


def format_age(min_m, max_m, lang):
    if max_m <= 36:
        return f"{min_m}-{max_m} {MONTHS_LABEL[lang]}"
    min_y = max(min_m // 12, 0)
    max_y = max(max_m // 12, min_y + 1)
    return f"{min_y}-{max_y} {YEARS_LABEL[lang]}"


def primary_band(game):
    mid = (game["meta"]["minAgeMonths"] + game["meta"]["maxAgeMonths"]) / 2
    for key, lo, hi in AGE_BANDS:
        if lo <= mid <= hi:
            return key
    return game["bands"][0]


def write_page(path, content):
    full = DIST / path.lstrip("/") / "index.html"
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(content, encoding="utf-8")


def game_badges(lang, game, age_hub_url, goal_hub_url):
    meta = game["meta"]
    cat = meta["categoryType"]
    age_label = format_age(meta["minAgeMonths"], meta["maxAgeMonths"], lang)
    chips = [
        f'<a href="{age_hub_url}" class="badge">{esc(age_label)}</a>',
        f'<a href="{goal_hub_url}" class="badge">{esc(CATEGORY_LABEL[cat][lang])}</a>',
    ]
    for ctx in meta.get("contexts") or []:
        label = CONTEXT_LABEL.get(ctx, {}).get(lang)
        if label:
            chips.append(f'<span class="badge badge-muted">{esc(label)}</span>')
    total = meta.get("totalMinutes") or meta.get("estimatedMinutes")
    if total:
        chips.append(f'<span class="badge badge-muted">{int(total)} {MINUTES_LABEL[lang]}</span>')
    return '<div class="badges">' + "".join(chips) + "</div>\n"


def render_game_page(lang, game, url_maps):
    gid = game["id"]
    text = game["text"][lang]
    meta = game["meta"]
    title = text["title"]
    mini = text["miniDescription"]
    short_desc = text["shortDescription"]
    steps = text["quickStart"]["steps"]
    setup = text["quickStart"]["setup"]
    safety = text["quickStart"]["safety"]
    materials = text.get("materials") or []

    band = primary_band(game)
    cat = meta["categoryType"]
    age_hub_url = url_maps["age_hub"][lang][band]
    goal_hub_url = url_maps["goal_hub"][lang][cat]
    canonical = url_maps["game"][lang][gid]
    hreflang_map = {l: url_maps["game"][l][gid] for l in LANGS}

    mini_cap = mini[:1].upper() + mini[1:] if mini else mini
    mini_cap = mini_cap.rstrip(".") if mini_cap else mini_cap
    meta_description = UI["meta_description_game"][lang].format(title=title, band=format_age(meta["minAgeMonths"], meta["maxAgeMonths"], lang), mini=mini_cap)

    head = html_head(lang, f"{title} | {SITE_NAME}", meta_description, canonical, hreflang_map, og_image=meta["imageUrl"])
    header = nav_header(lang, hreflang_map)
    cat_label = CATEGORY_LABEL[cat][lang]
    crumbs = breadcrumb([
        (UI["home_breadcrumb"][lang], f"/{lang}/"),
        (cat_label, goal_hub_url),
        (title, None),
    ])
    crumb_jsonld = breadcrumb_jsonld([
        (UI["home_breadcrumb"][lang], f"/{lang}/"),
        (cat_label, goal_hub_url),
        (title, canonical),
    ])

    steps_html = "".join(f"<li>{esc(s)}</li>" for s in steps)
    materials_html = "".join(f"<li>{esc(m)}</li>" for m in materials)
    safety_html = "".join(f"<p>{esc(s)}</p>" for s in safety)

    siblings = siblings_for(game, url_maps["all_games"], limit=8)
    related_links = []
    for sib in siblings:
        sib_title = sib["text"][lang]["title"]
        sib_url = url_maps["game"][lang][sib["id"]]
        related_links.append(f'<a href="{sib_url}" class="related-card">{esc(sib_title)}</a>')
    related_html = (
        f"<h2>{esc(UI['related_games_heading'][lang])}</h2>"
        f'<div class="related-grid">{"".join(related_links)}</div>'
        if related_links else ""
    )

    main_html = f"""<article class="game">
<h1>{esc(title)}</h1>
{game_badges(lang, game, age_hub_url, goal_hub_url)}
<p class="lead">{esc(short_desc)}</p>
<img src="{esc(meta['imageUrl'])}" width="1008" height="1008" alt="{esc(title)}" loading="eager">
<h2>{esc(UI['setup_heading'][lang])}</h2>
<p>{esc(setup)}</p>
<h2>{esc(UI['steps_heading'][lang])}</h2>
<ol class="steps">{steps_html}</ol>
{"<h2>" + esc(UI["materials_heading"][lang]) + "</h2><ul class=\"materials\">" + materials_html + "</ul>" if materials else ""}
<h2>{esc(UI['safety_heading'][lang])}</h2>
<div class="safety">{safety_html}</div>
{related_html}
</article>
"""
    jsonld = howto_jsonld(title, short_desc, meta["imageUrl"], materials, steps, meta.get("totalMinutes") or meta.get("estimatedMinutes")) + crumb_jsonld
    cta = cta_block(lang, "seo_game")
    return page_shell(lang, head, header, crumbs, main_html, cta, footer(lang), jsonld)


def render_age_hub(lang, band_key, games_in_band, url_maps):
    band_label = AGE_BAND_LABEL[band_key][lang]
    canonical = url_maps["age_hub"][lang][band_key]
    hreflang_map = {l: url_maps["age_hub"][l][band_key] for l in LANGS}
    title = f"{UI['games_breadcrumb'][lang]}: {band_label}"
    intro = UI["hub_age_intro"][lang].format(count=len(games_in_band), band=band_label)

    head = html_head(lang, f"{title} | {SITE_NAME}", intro, canonical, hreflang_map)
    header = nav_header(lang, hreflang_map)
    crumbs = breadcrumb([
        (UI["home_breadcrumb"][lang], f"/{lang}/"),
        (title, None),
    ])

    by_cat = {}
    for g in games_in_band:
        by_cat.setdefault(g["meta"]["categoryType"], []).append(g)

    sections = []
    for cat in CATEGORY_ORDER:
        bucket = by_cat.get(cat)
        if not bucket:
            continue
        bucket.sort(key=lambda g: g["text"][lang]["title"])
        goal_url = url_maps["goal_hub"][lang][cat]
        items = "".join(
            f'<li><a href="{url_maps["game"][lang][g["id"]]}">{esc(g["text"][lang]["title"])}</a>'
            f' <span class="muted">{esc(format_age(g["meta"]["minAgeMonths"], g["meta"]["maxAgeMonths"], lang))}</span></li>'
            for g in bucket
        )
        sections.append(
            f'<h3><a href="{goal_url}">{esc(CATEGORY_LABEL[cat][lang])}</a></h3><ul class="hub-list">{items}</ul>'
        )

    other_bands = "".join(
        f'<a href="{url_maps["age_hub"][lang][k]}" class="chip">{esc(AGE_BAND_LABEL[k][lang])}</a>'
        for k, _, _ in AGE_BANDS if k != band_key
    )

    main_html = f"""<section class="hub">
<h1>{esc(title)}</h1>
<p class="lead">{esc(intro)}</p>
{"".join(sections)}
<h2>{esc(UI['all_ages_heading'][lang])}</h2>
<div class="chip-row">{other_bands}</div>
</section>
"""
    cta = cta_block(lang, "seo_hub")
    return page_shell(lang, head, header, crumbs, main_html, cta, footer(lang))


def render_goal_hub(lang, cat, games_in_cat, url_maps):
    cat_label = CATEGORY_LABEL[cat][lang]
    canonical = url_maps["goal_hub"][lang][cat]
    hreflang_map = {l: url_maps["goal_hub"][l][cat] for l in LANGS}
    title = f"{UI['games_breadcrumb'][lang]}: {cat_label}"
    intro = UI["hub_goal_intro"][lang].format(count=len(games_in_cat), goal=cat_label)

    head = html_head(lang, f"{title} | {SITE_NAME}", intro, canonical, hreflang_map)
    header = nav_header(lang, hreflang_map)
    crumbs = breadcrumb([
        (UI["home_breadcrumb"][lang], f"/{lang}/"),
        (title, None),
    ])

    by_band = {}
    for g in games_in_cat:
        by_band.setdefault(primary_band(g), []).append(g)

    sections = []
    for key, _, _ in AGE_BANDS:
        bucket = by_band.get(key)
        if not bucket:
            continue
        bucket.sort(key=lambda g: g["text"][lang]["title"])
        age_url = url_maps["age_hub"][lang][key]
        items = "".join(
            f'<li><a href="{url_maps["game"][lang][g["id"]]}">{esc(g["text"][lang]["title"])}</a></li>'
            for g in bucket
        )
        sections.append(
            f'<h3><a href="{age_url}">{esc(AGE_BAND_LABEL[key][lang])}</a></h3><ul class="hub-list">{items}</ul>'
        )

    other_goals = "".join(
        f'<a href="{url_maps["goal_hub"][lang][c]}" class="chip">{esc(CATEGORY_LABEL[c][lang])}</a>'
        for c in CATEGORY_ORDER if c != cat
    )

    main_html = f"""<section class="hub">
<h1>{esc(title)}</h1>
<p class="lead">{esc(intro)}</p>
{"".join(sections)}
<h2>{esc(UI['all_goals_heading'][lang])}</h2>
<div class="chip-row">{other_goals}</div>
</section>
"""
    cta = cta_block(lang, "seo_hub")
    return page_shell(lang, head, header, crumbs, main_html, cta, footer(lang))


def render_home(lang, all_games, url_maps):
    canonical = f"/{lang}/"
    hreflang_map = {l: f"/{l}/" for l in LANGS}
    title = UI["home_title"][lang]
    intro = UI["home_intro"][lang].format(count=len(all_games))

    head = html_head(lang, f"{title} | {SITE_NAME}", intro, canonical, hreflang_map)
    header = nav_header(lang, hreflang_map)

    age_links = "".join(
        f'<a href="{url_maps["age_hub"][lang][k]}" class="chip">{esc(AGE_BAND_LABEL[k][lang])}</a>'
        for k, _, _ in AGE_BANDS
    )
    goal_links = "".join(
        f'<a href="{url_maps["goal_hub"][lang][c]}" class="chip">{esc(CATEGORY_LABEL[c][lang])}</a>'
        for c in CATEGORY_ORDER
    )

    main_html = f"""<section class="home">
<h1>{esc(title)}</h1>
<p class="lead">{esc(intro)}</p>
<h2>{esc(UI['by_age_heading'][lang])}</h2>
<div class="chip-row">{age_links}</div>
<h2>{esc(UI['by_goal_heading'][lang])}</h2>
<div class="chip-row">{goal_links}</div>
</section>
"""
    cta = cta_block(lang, "seo_home")
    return page_shell(lang, head, header, "", main_html, cta, footer(lang))


def build_url_maps(all_games):
    game_url = {lang: {} for lang in LANGS}
    used = {lang: set() for lang in LANGS}
    for lang in LANGS:
        for g in all_games:
            t = g["text"][lang]["title"]
            base_slug = slugify(t)
            sid = short_id(g["id"])
            path = f"/{lang}/{GAMES_WORD[lang]}/{base_slug}-{sid}/"
            if path in used[lang]:
                sid = g["id"]  # fall back to full id, guaranteed unique
                path = f"/{lang}/{GAMES_WORD[lang]}/{base_slug}-{sid}/"
            used[lang].add(path)
            game_url[lang][g["id"]] = path

    age_hub_url = {lang: {} for lang in LANGS}
    for lang in LANGS:
        for key, _, _ in AGE_BANDS:
            age_hub_url[lang][key] = f"/{lang}/{GAMES_WORD[lang]}/{AGE_WORD[lang]}/{key}/"

    goal_hub_url = {lang: {} for lang in LANGS}
    for lang in LANGS:
        for cat in CATEGORY_ORDER:
            goal_hub_url[lang][cat] = f"/{lang}/{GAMES_WORD[lang]}/{GOAL_WORD[lang]}/{CATEGORY_SLUG[cat][lang]}/"

    return {"game": game_url, "age_hub": age_hub_url, "goal_hub": goal_hub_url, "all_games": all_games}


def write_sitemaps(all_games, url_maps):
    today = datetime.date.today().isoformat()
    sitemap_files = []
    for lang in LANGS:
        urls = [f"/{lang}/"]
        for key, _, _ in AGE_BANDS:
            urls.append(url_maps["age_hub"][lang][key])
        for cat in CATEGORY_ORDER:
            urls.append(url_maps["goal_hub"][lang][cat])
        for g in all_games:
            urls.append(url_maps["game"][lang][g["id"]])
        entries = "".join(f"<url><loc>{SITE_ORIGIN}{u}</loc><lastmod>{today}</lastmod></url>" for u in urls)
        xml = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{entries}</urlset>\n'
        fname = f"sitemap-{lang}.xml"
        (DIST / fname).write_text(xml, encoding="utf-8")
        sitemap_files.append(fname)
        print(f"  sitemap-{lang}.xml: {len(urls)} urls")

    index_entries = "".join(
        f"<sitemap><loc>{SITE_ORIGIN}/{f}</loc><lastmod>{today}</lastmod></sitemap>" for f in sitemap_files
    )
    index_xml = f'<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{index_entries}</sitemapindex>\n'
    (DIST / "sitemap.xml").write_text(index_xml, encoding="utf-8")


def write_robots():
    (DIST / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\nSitemap: https://playmom.app/sitemap.xml\n",
        encoding="utf-8",
    )


def main():
    ids = load_ids()
    editorial = load_editorial()
    metadata = load_metadata()
    all_games = build_games(ids, editorial, metadata)
    print(f"loaded {len(all_games)} games")

    url_maps = build_url_maps(all_games)

    counts = {lang: 0 for lang in LANGS}
    for lang in LANGS:
        for g in all_games:
            html_out = render_game_page(lang, g, url_maps)
            write_page(url_maps["game"][lang][g["id"]], html_out)
            counts[lang] += 1

        games_by_band = {}
        for g in all_games:
            for band in g["bands"]:
                games_by_band.setdefault(band, []).append(g)
        for key, _, _ in AGE_BANDS:
            bucket = games_by_band.get(key, [])
            html_out = render_age_hub(lang, key, bucket, url_maps)
            write_page(url_maps["age_hub"][lang][key], html_out)
            counts[lang] += 1

        games_by_cat = {}
        for g in all_games:
            games_by_cat.setdefault(g["meta"]["categoryType"], []).append(g)
        for cat in CATEGORY_ORDER:
            bucket = games_by_cat.get(cat, [])
            html_out = render_goal_hub(lang, cat, bucket, url_maps)
            write_page(url_maps["goal_hub"][lang][cat], html_out)
            counts[lang] += 1

        html_out = render_home(lang, all_games, url_maps)
        write_page(f"/{lang}/", html_out)
        counts[lang] += 1

    write_sitemaps(all_games, url_maps)
    write_robots()

    print("pages per language:")
    for lang in LANGS:
        print(f"  {lang}: {counts[lang]} ({len(all_games)} games + 6 age hubs + 9 goal hubs + 1 home)")
    print(f"total pages: {sum(counts.values())}")


if __name__ == "__main__":
    main()
