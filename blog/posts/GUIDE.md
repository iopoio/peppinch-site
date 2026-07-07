# blog 글 추가 흐름 가이드

peppinch.com/blog/ 새 글 추가하는 절차. 빌드 시스템 X — 손으로 직접 추가.

## 1. draft 작성 (posts/.md)

```bash
cp _template.md 2026-05-20-tickdeck-week1.md
```

파일명 룰: `YYYY-MM-DD-slug.md` (날짜 + 영문 슬러그). 마음 가는 대로 .md로 작성.

## 2. index.html에 snippet 추가

draft 완성되면 `blog/index.html` 안 `.stack` div 최상단 (가장 최근 글이 위)에 아래 snippet 삽입:

```html
<article class="post">
  <span class="date">2026 · 05 · 20</span>
  <h2 class="title">tickdeck 1주차 — URL 한 줄로 PPT가 나오는가</h2>
  <p class="summary">
    DESIGN.md만 던지면 진짜 슬라이드가 나올까. 6주 실험 시작.
    첫 주는 명세서 한 장 쓰는 데서 막혔다.
  </p>
</article>
```

- 날짜 = `YYYY · MM · DD` (공백 + 가운뎃점)
- 제목 = 한 줄 (`.title`)
- 요약 = 2~3줄 (`.summary`)
- 본문 link 없음 — 본문은 .md 자체에 남기고 index는 summary만 (지금 단계)

## 3. 본문 link (선택)

본문 자체를 사이트에 노출하고 싶으면 두 옵션:

### A. 별도 HTML 페이지 (수동)
`blog/posts/2026-05-20-tickdeck-week1.html` 새로 만들고 `<a href="/blog/posts/2026-05-20-tickdeck-week1.html">` link 추가. 본문 HTML로 변환.

### B. .md 그대로 (marked.js 런타임 렌더링)
js 한 줄로 .md fetch + 렌더. 빌드 X·근데 첫 load 살짝 느림.

지금은 **summary만 index에 노출·.md는 draft 보관용**으로 시작. 본문 link 필요해지면 그때 결정.

## 4. 발행 스크립트 (필수 · 2026-07-07 신설)

```bash
python3 scripts/publish.py
```

- `blog/posts/*.html` meta 태그를 읽어 **sitemap.xml·rss.xml 전체 재생성** (손 편집 X — 스크립트가 SoT)
- `blog/index.html`에 안 걸린 글이 있으면 붙여넣을 snippet까지 출력 (index는 손으로 유지)
- 배경: 6/24~7/4 글 5건이 sitemap에 빠진 채 발행됨 — 절차에 이 단계가 없어서 생긴 구조적 누락

## 5. commit·push

```bash
cd ~/Projects/Automation/peppinch-site
git add blog/ sitemap.xml rss.xml
git commit -m "blog: <글 제목 한 줄>"
git push
```

Cloudflare Pages 자동 deploy. 1~2분 뒤 peppinch.com/blog/ 반영.

---

## 빌드 시스템 도입 결정 영역 (후추님 view)

지금 = HTML 직접 작성 (위 절차). 빌드 X·deps X·즉시 가동.

빌드 도입 고려 시점:
- 글 5~10개 누적 후 — index 관리 부담 늘어남
- .md → HTML 자동 변환 필요해질 때
- 본문 link 다수 추가 시점

후보 (도입 시):
- **Eleventy** (11ty) — 정적 사이트 generator·.md → .html·minimal·Cloudflare Pages 호환
- **Astro** — 더 무거움·필요 X 지금
- **자작 Python 스크립트** — `posts/*.md` → `index.html` 자동 generate (간단)

권고: **5글 누적 후 결정**. 그때까지는 manual HTML로 슬렁슬렁.

---

## 참고

- 디자인 톤·CSS = `blog/index.html` 상단 `<style>` 영역. snippet 추가만 하면 자동 적용
- 모바일 styling 점검 필요 시 `python3 -m http.server 8000` 로컬 미리보기
- 첫 글 placeholder: TickDeck 6주 검증 누적용 (5/14 시작 영역)
