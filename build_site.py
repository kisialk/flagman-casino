# -*- coding: utf-8 -*-
"""Generate all Flagman Casino HTML pages."""
import copy
import json
from pathlib import Path

from pages_data import PAGES
from pages_expand import EXPAND_BY_SLUG

ROOT = Path(__file__).parent
DOMAIN = "https://flagman-casino.vercel.app"
AFF = "https://lkga.cc/0b02c9ea"
AFF_REL = "nofollow sponsored noopener"
OG_IMAGE = f"{DOMAIN}/assets/img/flagman-banner.png"
LOGO_URL = f"{DOMAIN}/assets/img/logo.png"
ORG_NAME = "Flagman Casino"
DATE = "2026-05-17"

NAV = [
    ("official-site", "Официальный сайт"),
    ("casino", "Казино"),
    ("bonus", "Бонусы"),
    ("registration", "Регистрация"),
    ("zerkalo", "Зеркало"),
    ("bets", "Ставки"),
    ("download", "Скачать"),
    ("login", "Вход"),
    ("reviews", "Отзывы"),
]

RELATED = [
    ("official-site", "Официальный сайт"),
    ("login", "Вход"),
    ("registration", "Регистрация"),
    ("zerkalo", "Зеркало"),
    ("bonus", "Бонусы"),
    ("casino", "Казино"),
    ("download", "Скачать"),
    ("bets", "Ставки"),
    ("reviews", "Отзывы"),
]

FAVICON = """
<link rel="icon" href="/favicon.ico?v=2" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png?v=2">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png?v=2">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v=2">
<link rel="manifest" href="/site.webmanifest">
"""


def path_for(slug: str) -> str:
    return "/" if not slug else f"/{slug}/"


def schema_graph(page: dict) -> str:
    url = DOMAIN + path_for(page["slug"])
    crumbs = [
        {"@type": "ListItem", "position": 1, "name": "Главная", "item": DOMAIN + "/"},
    ]
    if page["slug"]:
        crumbs.append(
            {
                "@type": "ListItem",
                "position": 2,
                "name": page["breadcrumb"],
                "item": url,
            }
        )
    graph = [
        {
            "@type": "WebSite",
            "@id": f"{DOMAIN}/#website",
            "url": DOMAIN + "/",
            "name": ORG_NAME,
            "inLanguage": "ru-RU",
        },
        {
            "@type": "Organization",
            "@id": f"{DOMAIN}/#organization",
            "name": ORG_NAME,
            "url": DOMAIN + "/",
            "logo": LOGO_URL,
        },
        {
            "@type": "WebPage",
            "@id": f"{url}#webpage",
            "url": url,
            "name": page["title"],
            "description": page["description"],
            "isPartOf": {"@id": f"{DOMAIN}/#website"},
            "inLanguage": "ru-RU",
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": crumbs,
        },
    ]
    if page.get("article"):
        graph.append(
            {
                "@type": "Article",
                "headline": page["h1"],
                "description": page["description"],
                "author": {"@type": "Organization", "name": ORG_NAME},
                "publisher": {"@type": "Organization", "name": ORG_NAME, "logo": LOGO_URL},
                "datePublished": DATE,
                "dateModified": DATE,
                "inLanguage": "ru-RU",
                "mainEntityOfPage": {"@id": f"{url}#webpage"},
            }
        )
    if page.get("faq"):
        graph.append(
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": item["q"],
                        "acceptedAnswer": {"@type": "Answer", "text": item["a"]},
                    }
                    for item in page["faq"]
                ],
            }
        )
    payload = {"@context": "https://schema.org", "@graph": graph}
    return f'<script type="application/ld+json">{json.dumps(payload, ensure_ascii=False)}</script>'


def header(active: str) -> str:
    nav_items = "".join(
        f'<li><a href="{path_for(slug)}"{" class=\"active\"" if slug == active else ""}>{label}</a></li>'
        for slug, label in NAV
    )
    return f"""<header class="site-header">
  <div class="container header-inner">
    <div class="brand-wrap">
      <a href="/"><img src="/assets/img/logo.png" alt="Flagman Casino логотип" class="logo" width="140" height="40" decoding="async"></a>
      <a class="bonus-btn" href="{AFF}" target="_blank" rel="{AFF_REL}">Бонус</a>
    </div>
    <button class="menu-toggle" type="button" data-menu-toggle aria-label="Открыть меню" aria-expanded="false">☰</button>
    <nav class="main-nav" data-main-nav aria-label="Основное меню">
      <ul class="nav-list">{nav_items}</ul>
    </nav>
  </div>
</header>"""


def footer() -> str:
    return f"""<footer class="site-footer">
  <div class="container footer-inner">
    <img src="/assets/img/logo.png" alt="Флагман казино" class="footer-logo" width="130" height="38" loading="lazy" decoding="async">
    <div class="footer-links">
      <a href="{path_for('official-site')}">Официальный сайт</a>
      <a href="{path_for('casino')}">Казино</a>
      <a href="{path_for('bonus')}">Бонусы</a>
      <a href="{path_for('registration')}">Регистрация</a>
      <a href="{path_for('zerkalo')}">Зеркало</a>
      <a href="{path_for('bets')}">Ставки</a>
      <a href="{path_for('download')}">Скачать</a>
      <a href="{path_for('login')}">Вход</a>
      <a href="{path_for('reviews')}">Отзывы</a>
    </div>
    <div class="footer-trust">
      <span class="badge-18">18+</span>
      <a href="/responsible-gaming/">Ответственная игра</a>
      <a href="/privacy-policy/">Политика конфиденциальности</a>
      <a href="/terms/">Условия использования</a>
      <a href="/contacts/">Контакты</a>
    </div>
    <p class="footer-updated">Updated: May 2026</p>
    <p class="copyright">© 2026 Flagman Casino. Информационный сайт о бренде флагман казино.</p>
  </div>
</footer>"""


def related_block(exclude: str) -> str:
    links = "".join(
        f'<a href="{path_for(slug)}">{label}</a>'
        for slug, label in RELATED
        if slug != exclude
    )
    return f"""<section class="section-card">
  <h2>Полезные разделы флагман казино</h2>
  <div class="links-grid">{links}</div>
</section>"""


def render_page(page: dict) -> str:
    slug = page["slug"]
    url = DOMAIN + path_for(slug)
    active = slug
    cta_href = page.get("cta_href", AFF)
    cta_external = cta_href == AFF
    cta_rel = f' rel="{AFF_REL}"' if cta_external else ""
    cta_target = ' target="_blank"' if cta_external else ""
    toc = page.get("toc", [])
    toc_html = ""
    if toc:
        items = "".join(f'<li><a href="#{aid}">{title}</a></li>' for aid, title in toc)
        toc_html = f'<nav class="page-toc" aria-label="Содержание страницы"><h2 class="toc-title">Содержание страницы</h2><ol>{items}</ol></nav>'

    intro = "".join(f"<p>{p}</p>" for p in page.get("intro", []))
    sections_html = ""
    for sec in page.get("sections", []):
        sid = sec.get("id", "")
        id_attr = f' id="{sid}"' if sid else ""
        paras = "".join(f"<p>{p}</p>" for p in sec["paragraphs"])
        sections_html += f'<section class="section-card"{id_attr}><h2>{sec["h2"]}</h2>{paras}</section>\n'

    faq_html = ""
    if page.get("faq"):
        items = "".join(
            f'<div class="faq-item"><h3>{f["q"]}</h3><p>{f["a"]}</p></div>'
            for f in page["faq"]
        )
        faq_title = page.get("faq_title", "Частые вопросы о флагман казино")
        faq_html = f'<section class="section-card" id="faq"><h2>{faq_title}</h2>{items}</section>'

    practice = page.get("practice")
    practice_html = ""
    if practice:
        practice_html = f'<section class="section-card practice-block"><h2>{practice["h2"]}</h2>{"".join(f"<p>{p}</p>" for p in practice["paragraphs"])}<p><a class="cta-btn" href="{cta_href}"{cta_target}{cta_rel}>{page["cta"]}</a></p></section>'

    mid_cta = f'<p class="cta-mid"><a class="cta-btn" href="{cta_href}"{cta_target}{cta_rel}>{page["cta"]}</a></p>' if page.get("mid_cta") else ""

    og = f"""
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{page['title']}">
<meta property="og:description" content="{page['description']}">
<meta property="og:image" content="{OG_IMAGE}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{page['title']}">
<meta name="twitter:description" content="{page['description']}">
<meta name="twitter:image" content="{OG_IMAGE}">
"""

    return f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <title>{page['title']}</title>
  <meta name="description" content="{page['description']}">
  <link rel="canonical" href="{url}">
  <meta name="theme-color" content="#1f2937">
  {FAVICON}
  {og}
  <link rel="stylesheet" href="/style.css">
  {schema_graph(page)}
</head>
<body>
{header(active)}
<main>
  <div class="container">
    <section class="hero">
      <div class="hero-grid">
        <div>
          <h1>{page['h1']}</h1>
          {intro}
          <div class="hero-actions">
            <a class="cta-btn" href="{cta_href}"{cta_target}{cta_rel}>{page['cta']}</a>
          </div>
        </div>
        <a class="banner-link" href="{AFF}" target="_blank" rel="{AFF_REL}">
          <img src="/assets/img/flagman-banner.png" alt="{page['banner_alt']}" width="520" height="320" loading="eager" fetchpriority="high" decoding="async">
        </a>
      </div>
    </section>
    {toc_html}
    <div class="content-grid">
      {sections_html}
      {practice_html}
      {mid_cta}
      {faq_html}
      {related_block(slug)}
    </div>
  </div>
</main>
{footer()}
<script src="/script.js" defer></script>
</body>
</html>"""


def write_sitemap():
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in PAGES:
        pri = p.get("priority", "0.8")
        loc = DOMAIN + path_for(p["slug"])
        lines.append(f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{DATE}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{pri}</priority>
  </url>""")
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines), encoding="utf-8")


def merge_expand(page: dict) -> dict:
    page = copy.deepcopy(page)
    extra = list(EXPAND_BY_SLUG.get(page["slug"], []))
    from pages_expand import BIG
    if page["slug"] in BIG:
        extra.append(BIG[page["slug"]])
    if extra:
        page["sections"] = list(page.get("sections", [])) + extra
    return page


def main():
    for page in PAGES:
        page = merge_expand(page)
        html = render_page(page)
        fname = "index.html" if not page["slug"] else f"{page['slug']}.html"
        (ROOT / fname).write_text(html, encoding="utf-8")
        print(f"Wrote {fname} ({len(html.split())} words approx)")
    write_sitemap()
    (ROOT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\nSitemap: https://flagman-casino.vercel.app/sitemap.xml\n",
        encoding="utf-8",
    )
    print("Done.")


if __name__ == "__main__":
    main()
