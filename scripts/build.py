#!/usr/bin/env python3
"""peppinch.com 블로그 빌드 — md → 글 HTML 렌더 + 인덱스 자동 삽입 + sitemap/RSS.

사용: python3 scripts/build.py   (repo 루트 어디서 실행해도 됨)

- 소스 = blog/posts/YYYY-MM-DD-slug.md (front-matter 필수, _template.md 참조)
- status: draft 글은 스킵. published만 렌더.
- 기존 손제작 HTML 글(md 없는 것)은 절대 건드리지 않음.
- blog/index.html: 없는 글만 해당 분류 .plist 최상단에 삽입 + 분류 카운트 갱신.
  (디자인 페이지라 전체 재생성 X — 기존 행 원문 보존)
- 마지막에 publish.py(sitemap·rss·인덱스 검사) 자동 실행.

md 문법 (최소): 문단(빈 줄 구분) · ## 소제목 · > 인용 · - 목록 · **강조** ·
[링크](url) · ![이미지](src) · `<`로 시작하는 블록 = raw HTML 통과 (rptcard 등).
문단 안 줄바꿈 = <br>.
"""
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import publish  # sitemap/rss/인덱스 검사 재사용

ROOT = publish.ROOT
POSTS = publish.POSTS
BASE = publish.BASE
TEMPLATE = Path(__file__).resolve().parent / "post_template.html"
INDEX = ROOT / "blog" / "index.html"


# ---------- front-matter ----------

def parse_md(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"\A---\n(.*?)\n---\n(.*)\Z", text, re.S)
    if not m:
        raise ValueError(f"{path.name}: front-matter(---) 없음")
    meta, body = {}, m.group(2).strip()
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    required = [k for k in ("title", "description", "section") if not meta.get(k)]
    if required:
        raise ValueError(f"{path.name}: front-matter 누락 {required}")
    meta.setdefault("date", path.stem[:10])
    meta.setdefault("summary", meta["description"])
    meta.setdefault("status", "published")
    meta["tags"] = [t.strip() for t in meta.get("tags", "").split(",") if t.strip()]
    meta["slug"] = path.stem
    return meta, body


# ---------- md → HTML (최소 변환기) ----------

def inline(text):
    text = html.escape(text, quote=False)
    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img src="\2" alt="\1">', text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    return text


def md_to_html(body):
    out = []
    for block in re.split(r"\n\s*\n", body):
        block = block.strip()
        if not block:
            continue
        if block.startswith("<"):  # raw HTML (rptcard·mv·takeaway 등) 통과
            out.append(f"    {block}")
        elif block.startswith("## "):
            out.append(f"    <h2>{inline(block[3:])}</h2>")
        elif block.startswith("> "):
            quote = "<br>\n".join(inline(l[2:] if l.startswith('> ') else l)
                                  for l in block.splitlines())
            out.append(f"    <blockquote>{quote}</blockquote>")
        elif re.match(r"^[-*] ", block):
            items = "\n".join(f"      <li>{inline(re.sub(r'^[-*] ', '', l))}</li>"
                              for l in block.splitlines())
            out.append(f"    <ul>\n{items}\n    </ul>")
        else:
            out.append(f"    <p>{'<br>'.join(inline(l) for l in block.splitlines())}</p>")
    return "\n\n".join(out)


# ---------- 글 HTML 렌더 ----------

def render_post(meta, body):
    url = f"{BASE}/blog/posts/{meta['slug']}"
    y, mo, d = meta["date"].split("-")
    jsonld = json.dumps({
        "@context": "https://schema.org", "@type": "BlogPosting",
        "headline": meta["title"], "description": meta["description"],
        "datePublished": f"{meta['date']}T00:00:00+09:00",
        "dateModified": f"{meta['date']}T00:00:00+09:00",
        "inLanguage": "ko-KR", "url": url, "mainEntityOfPage": url,
        "image": f"{BASE}/og-image.png", "keywords": ", ".join(meta["tags"]),
        "author": {"@type": "Person", "name": "peppinch", "url": f"{BASE}/"},
        "publisher": {"@type": "Organization", "name": "peppinch",
                      "logo": {"@type": "ImageObject", "url": f"{BASE}/favicon.svg"}},
    }, ensure_ascii=False)
    tags_meta = "".join(f'<meta property="article:tag" content="{t}">' for t in meta["tags"])
    page = TEMPLATE.read_text(encoding="utf-8")
    for k, v in {
        "{{TITLE}}": html.escape(meta["title"], quote=False),
        "{{DESC}}": html.escape(meta["description"]),
        "{{URL}}": url, "{{DATE}}": meta["date"], "{{DATE_DOT}}": f"{y} · {mo} · {d}",
        "{{SECTION}}": meta["section"], "{{TAGS_META}}": tags_meta,
        "{{KEYWORDS}}": ", ".join(meta["tags"]), "{{JSONLD}}": jsonld,
        "{{SLUG}}": meta["slug"], "{{CONTENT}}": md_to_html(body),
    }.items():
        page = page.replace(k, v)
    return page


# ---------- 인덱스 자동 삽입 ----------

def make_row(meta):
    y, mo, d = meta["date"].split("-")
    return f'''      <a class="row" href="/blog/posts/{meta['slug']}">
        <span class="rd">{y} · {mo} · {d}</span>
        <span>
          <span class="rt">{html.escape(meta['title'], quote=False)}</span>
          <span class="rs">{html.escape(meta['summary'], quote=False)}</span>
        </span>
        <span class="go">→ 읽기</span>
      </a>'''


def insert_into_index(meta):
    """해당 분류 .plist 최상단에 행 삽입. 분류 없으면 새 섹션 생성."""
    idx = INDEX.read_text(encoding="utf-8")
    if f'/blog/posts/{meta["slug"]}"' in idx:
        return False
    section_pat = (r'(<div class="cat-head"><span class="cn">'
                   + re.escape(meta["section"])
                   + r'</span>.*?<div class="plist">\n)')
    m = re.search(section_pat, idx, re.S)
    row = make_row(meta)
    if m:
        idx = idx[:m.end()] + row + "\n" + idx[m.end():]
    else:  # 새 분류 — 마지막 </section> 뒤에 신설
        new_sec = f'''
  <section class="cat">
    <div class="cat-head"><span class="cn">{meta['section']}</span><span class="cc">0</span><span class="cl"></span></div>
    <div class="plist">
{row}
    </div>
  </section>
'''
        last = idx.rfind("</section>")
        if last == -1:
            raise ValueError("index.html에 </section> 없음 — 구조 변경됨, 수동 확인 필요")
        idx = idx[:last + len("</section>")] + new_sec + idx[last + len("</section>"):]
    INDEX.write_text(idx, encoding="utf-8")
    return True


def update_counts():
    """각 분류의 .cc 카운트를 실제 행 수로 재계산."""
    idx = INDEX.read_text(encoding="utf-8")
    sections = re.split(r'(?=<section class="cat">)', idx)
    out = []
    for chunk in sections:
        if chunk.startswith('<section class="cat">'):
            n = chunk.count('class="row"')
            chunk = re.sub(r'(<span class="cn">[^<]+</span>)(<span class="cc">\d*</span>)?',
                           rf'\1<span class="cc">{n}</span>', chunk, count=1)
        out.append(chunk)
    INDEX.write_text("".join(out), encoding="utf-8")


# ---------- main ----------

if __name__ == "__main__":
    built = 0
    for md in sorted(POSTS.glob("*.md")):
        if md.stem.startswith("_"):
            continue
        try:
            meta, body = parse_md(md)
        except ValueError as e:  # 구형식 draft — 보관용, 빌드 대상 아님
            print(f"스킵(구형식): {e}")
            continue
        if meta["status"] != "published":
            print(f"draft 스킵: {md.name}")
            continue
        out = POSTS / f"{meta['slug']}.html"
        if out.exists() and out.stat().st_mtime >= md.stat().st_mtime:
            continue
        out.write_text(render_post(meta, body), encoding="utf-8")
        print(f"렌더: {out.name}")
        if insert_into_index(meta):
            print(f"인덱스 삽입: {meta['slug']} → [{meta['section']}]")
        built += 1
    if built:
        update_counts()
    print(f"빌드 {built}건 — sitemap/RSS 갱신으로 이어감")
    posts = publish.load_posts()
    publish.write_sitemap(posts)
    publish.write_rss(posts)
    ok = publish.check_index(posts)
    sys.exit(0 if ok else 1)
