# blog 글 추가 흐름 가이드

peppinch.com/blog/ 새 글 추가하는 절차. **2026-07-08 빌드 시스템 도입** — md 한 장 쓰고 커맨드 한 번.

## 1. draft 작성 (posts/*.md)

```bash
cp _template.md 2026-07-10-slug.md
```

파일명 룰: `YYYY-MM-DD-slug.md`. front-matter(title·description·section 필수) 채우고 본문은 md로.
특수 요소(리포트 카드·내생각 박스)는 raw HTML 블록으로 붙여넣으면 그대로 통과됨.

## 2. 빌드 (발행)

완성되면 `status: published`로 바꾸고:

```bash
python3 scripts/build.py
```

이 한 번으로 전부 자동:
- **글 HTML 렌더** — `scripts/post_template.html` 디자인 그대로 (OG·JSON-LD·좋아요 버튼 포함)
- **blog/index.html 자동 삽입** — 해당 분류 최상단 + 분류 카운트 갱신 (분류 없으면 신설)
- **sitemap.xml·rss.xml 전체 재생성** (publish.py 자동 호출)

md 없이 손으로 만든 옛 글 HTML은 절대 안 건드림. md 수정 후 재빌드하면 HTML만 다시 생성.

## 3. commit·push

```bash
git add blog/ sitemap.xml rss.xml
git commit -m "blog: <글 제목 한 줄>"
git push
```

Cloudflare Pages 자동 deploy. 1~2분 뒤 반영.

## 참고 — publish.py 단독 실행

빌드 없이 sitemap/RSS만 다시 만들고 싶을 때 (예: HTML 직접 수정 후):

```bash
python3 scripts/publish.py
```

배경: 6/24~7/4 글 5건이 sitemap에 빠진 채 발행됨(7/7 발견) → 발행 절차 자동화가 근본 해결.

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
