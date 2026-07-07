#!/usr/bin/env python3
"""peppinch.com 발행 스크립트 — sitemap.xml·rss.xml 재생성 + index 누락 검사.

사용: python3 scripts/publish.py   (repo 루트 어디서 실행해도 됨)

- blog/posts/*.html 의 meta 태그(og:title·description·article:published_time)가 SoT.
- *-report.html 은 본문 부록 페이지라 sitemap/RSS 에서 제외 (기존 방침 유지).
- blog/index.html 은 디자인 페이지라 자동 수정 X — 누락 글이 있으면 붙여넣을 snippet 출력.
"""
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS = ROOT / "blog" / "posts"
BASE = "https://www.peppinch.com"
KST = timezone(timedelta(hours=9))


def meta(html, pattern):
    m = re.search(pattern, html)
    return m.group(1).strip() if m else None


def load_posts():
    posts = []
    for f in sorted(POSTS.glob("*.html")):
        # 부록 판정: -report 접미사 + 짝이 되는 본문 글이 실존할 때만
        # (2026-07-01-tech-report 처럼 슬러그가 우연히 -report 로 끝나는 본문 글 보호)
        if f.stem.endswith("-report") and (POSTS / f"{f.stem[:-7]}.html").exists():
            continue
        html = f.read_text(encoding="utf-8")
        date = meta(html, r'article:published_time" content="(\d{4}-\d{2}-\d{2})')
        if not date:  # fallback: 파일명 앞 10자
            date = f.stem[:10]
        posts.append({
            "slug": f.stem,
            "url": f"{BASE}/blog/posts/{f.stem}",
            "title": meta(html, r'property="og:title" content="([^"]*)"') or f.stem,
            "desc": meta(html, r'name="description" content="([^"]*)"') or "",
            "section": meta(html, r'article:section" content="([^"]*)"') or "",
            "date": date,
        })
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


def write_sitemap(posts):
    latest = posts[0]["date"]
    urls = [
        (f"{BASE}/", latest, "weekly", "1.0"),
        (f"{BASE}/business/", "2026-05-14", "monthly", "0.8"),
        (f"{BASE}/blog/", latest, "weekly", "0.7"),
    ] + [(p["url"], p["date"], "monthly", "0.6") for p in posts]
    body = "\n".join(
        f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{mod}</lastmod>\n"
        f"    <changefreq>{freq}</changefreq>\n    <priority>{pri}</priority>\n  </url>"
        for loc, mod, freq, pri in urls
    )
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{body}\n</urlset>\n", encoding="utf-8")
    print(f"sitemap.xml — 글 {len(posts)}개 + 고정 3페이지")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def write_rss(posts):
    def rfc822(d):
        return datetime.strptime(d, "%Y-%m-%d").replace(tzinfo=KST).strftime(
            "%a, %d %b %Y 00:00:00 +0900")
    items = "\n".join(
        f"  <item>\n    <title>{esc(p['title'])}</title>\n"
        f"    <link>{p['url']}</link>\n    <guid>{p['url']}</guid>\n"
        f"    <description>{esc(p['desc'])}</description>\n"
        f"    <pubDate>{rfc822(p['date'])}</pubDate>\n  </item>"
        for p in posts
    )
    (ROOT / "rss.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n<channel>\n'
        "  <title>peppinch blog</title>\n"
        f"  <link>{BASE}/blog/</link>\n"
        "  <description>흥미롭고 관심있는 주제를 끄적입니다. 천천히, 한 꼬집씩.</description>\n"
        "  <language>ko</language>\n"
        f'  <atom:link href="{BASE}/rss.xml" rel="self" type="application/rss+xml"/>\n'
        f"{items}\n</channel>\n</rss>\n", encoding="utf-8")
    print(f"rss.xml — {len(posts)}개 item")


def check_index(posts):
    index = (ROOT / "blog" / "index.html").read_text(encoding="utf-8")
    missing = [p for p in posts if f'/blog/posts/{p["slug"]}"' not in index]
    for p in missing:
        y, m, d = p["date"].split("-")
        print(f"\n⚠️ blog/index.html 에 없는 글: {p['slug']} (분류: {p['section'] or '?'})")
        print("   해당 분류 .plist 최상단에 붙여넣기:")
        print(f'''      <a class="row" href="/blog/posts/{p['slug']}">
        <span class="rd">{y} · {m} · {d}</span>
        <span>
          <span class="rt">{p['title']}</span>
          <span class="rs">{p['desc']}</span>
        </span>
        <span class="go">→ 읽기</span>
      </a>''')
    if not missing:
        print("blog/index.html — 전체 글 등재 확인")
    return not missing


if __name__ == "__main__":
    posts = load_posts()
    write_sitemap(posts)
    write_rss(posts)
    ok = check_index(posts)
    sys.exit(0 if ok else 1)
