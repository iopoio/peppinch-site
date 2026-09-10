#!/usr/bin/env python3
"""Generate public article text and llms.txt from the published HTML, without a second copy to edit."""
import html
import json
import re
from html.parser import HTMLParser
from urllib.parse import urljoin
import publish


class ArticleText(HTMLParser):
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
    BLOCK = {"p", "div", "section", "article", "h1", "h2", "h3", "h4", "li", "tr", "blockquote", "summary", "details"}

    def __init__(self, base):
        super().__init__(convert_charrefs=True)
        self.base, self.stack, self.parts = base, [], []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = set(attrs.get("class", "").split())
        parent_active, parent_skip = self.stack[-1][1:3] if self.stack else (False, False)
        active = parent_active or tag == "main" or "content" in classes
        skip = parent_skip or tag in {"script", "style", "nav", "footer", "button"} or bool(classes & {"likewrap", "foot", "topbar"})
        href = attrs.get("href") if tag == "a" else None
        if active and not skip:
            if tag in self.BLOCK or tag == "br": self.parts.append("\n")
            if tag in {"td", "th"}: self.parts.append(" | ")
            if tag == "li": self.parts.append("- ")
            if tag == "img" and attrs.get("alt"): self.parts.append("[이미지: " + attrs["alt"] + "]")
            if tag == "iframe" and attrs.get("src"): self.parts.append("\n[첨부 자료] " + urljoin(self.base, attrs["src"]) + "\n")
        if tag not in self.VOID: self.stack.append((tag, active, skip, href))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                _, active, skip, href = self.stack[i]
                if active and not skip:
                    if href and not href.startswith(("javascript:", "mailto:")):
                        self.parts.append(" (" + urljoin(self.base, href) + ")")
                    if tag in self.BLOCK: self.parts.append("\n")
                del self.stack[i:]
                break

    def handle_data(self, data):
        if self.stack and self.stack[-1][1] and not self.stack[-1][2]:
            self.parts.append(re.sub(r"\s+", " ", data))

    def text(self):
        return "\n\n".join(line.strip() for line in "".join(self.parts).splitlines() if line.strip())


def prepare_article(path):
    """Keep machine metadata and the visible byline in sync; never invent an edit date."""
    source = path.read_text(encoding="utf-8")
    pattern = r'<script type="application/ld\+json">(.*?)</script>'
    match = re.search(pattern, source, re.S)
    if not match: raise ValueError(f"Article structured data missing: {path.name}")
    data = json.loads(match.group(1))
    data["description"] = publish.meta(source, r'name="description" content="([^"]*)"') or data.get("description", "")
    title = publish.meta(source, r'property="og:title" content="([^"]*)"')
    if title: data["headline"] = title
    data["inLanguage"] = "ko-KR"
    modified = data.get("dateModified", data["datePublished"])
    data["dateModified"] = modified
    payload = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")
    source = re.sub(pattern, lambda _: '<script type="application/ld+json">\n' + payload + '\n</script>', source, count=1, flags=re.S)
    source = re.sub(r'<meta property="article:modified_time" content="[^"]*">\n?', '', source)
    source = source.replace('</head>', f'<meta property="article:modified_time" content="{modified}">\n</head>', 1)
    alternate = f'<link rel="alternate" type="text/plain" title="본문 텍스트" href="/blog/text/{path.stem}.txt">'
    source = re.sub(r'<link rel="alternate" type="text/plain"[^>]*>\n?', '', source)
    source = source.replace('</head>', alternate + '\n</head>', 1)
    published = data['datePublished'][:10]
    revised = modified[:10]
    byline = (f'<p class="article-byline" style="font-size:13px;line-height:1.8">작성: {html.escape(data.get("author", {}).get("name", "peppinch"))}'
              f' · 발행 <time datetime="{published}">{published}</time>'
              f' · 수정 <time datetime="{revised}">{revised}</time></p>')
    source = re.sub(r'\n?<p class="article-byline"[^>]*>.*?</p>', '', source, flags=re.S)
    source = re.sub(r'</h1>', lambda _: '</h1>\n' + byline, source, count=1)
    if source != path.read_text(encoding="utf-8"): path.write_text(source, encoding="utf-8")


def article_data(path):
    source = path.read_text(encoding="utf-8")
    match = re.search(r'<script type="application/ld\+json">(.*?)</script>', source, re.S)
    data = json.loads(match.group(1)) if match else {}
    url = data.get("url", f"{publish.BASE}/blog/posts/{path.stem}")
    parser = ArticleText(url)
    parser.feed(source)
    body = parser.text()
    if not body: raise ValueError(f"No article body: {path.name}")
    description = publish.meta(source, r'name="description" content="([^"]*)"') or ""
    return {"slug": path.stem, "url": url, "title": data.get("headline", path.stem),
            "description": description, "published": data.get("datePublished", path.stem[:10])[:10],
            "modified": data.get("dateModified", data.get("datePublished", path.stem[:10]))[:10],
            "author": data.get("author", {}).get("name", "peppinch"), "body": body}


def prune_generated(target, filenames):
    """Remove only files recorded by this generator, never arbitrary public assets."""
    manifest = target / ".generated.json"
    previous = json.loads(manifest.read_text()) if manifest.exists() else []
    for name in set(previous) - set(filenames):
        if not isinstance(name, str) or "/" in name or "\\" in name or not name.endswith(".txt"):
            raise ValueError("Invalid generated text filename")
        (target / name).unlink(missing_ok=True)
    manifest.write_text(json.dumps(sorted(filenames), ensure_ascii=False) + "\n", encoding="utf-8")


def write_readable():
    for path in sorted(publish.POSTS.glob("*.html")):
        prepare_article(path)
    entries = [article_data(p) for p in sorted(publish.POSTS.glob("*.html"), reverse=True)]
    target = publish.ROOT / "blog" / "text"
    target.mkdir(exist_ok=True)
    for entry in entries:
        text = (f"{entry['title']}\n\n원문: {entry['url']}\n" +
                f"작성: {entry['author']} | 발행: {entry['published']} | 수정: {entry['modified']}\n\n" +
                entry['description'] + "\n\n" + entry['body'] + "\n")
        (target / f"{entry['slug']}.txt").write_text(text, encoding="utf-8")
    prune_generated(target, [entry["slug"] + ".txt" for entry in entries])
    lines = ["# peppinch", "", "> 작은 도구를 만들고, 직접 해본 일과 읽은 자료에 관한 생각을 기록합니다.", "",
             "## 사이트", "", f"- [홈]({publish.BASE}/)", f"- [사업 소개]({publish.BASE}/business/)",
             f"- [블로그]({publish.BASE}/blog/)", f"- [쇼츠 대본]({publish.BASE}/shorts/)", "",
             "## 블로그 글과 브리핑", "", "개인적인 감상은 본문에, 자료의 발언과 출처는 연결된 브리핑에 담았습니다. 아래 텍스트는 공개 HTML에서 자동 생성합니다.", ""]
    for entry in entries:
        title = entry['title'].replace("[", "(").replace("]", ")")
        lines.append(f"- [{title}]({entry['url']}): {entry['description']} (발행 {entry['published']}, 수정 {entry['modified']}) · [본문 텍스트]({publish.BASE}/blog/text/{entry['slug']}.txt)")
    lines += ["", "## 갱신 정보", "", f"- [RSS]({publish.BASE}/rss.xml)", f"- [사이트맵]({publish.BASE}/sitemap.xml)", ""]
    (publish.ROOT / "llms.txt").write_text("\n".join(lines), encoding="utf-8")
    print(f"본문 텍스트 {len(entries)}개 · llms.txt 갱신")


if __name__ == "__main__":
    write_readable()
