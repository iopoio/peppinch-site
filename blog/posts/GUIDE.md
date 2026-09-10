# blog 글 추가 흐름 가이드

peppinch.com/blog/ 새 글 추가하는 절차. **2026-07-08 빌드 시스템 도입** — md 한 장 쓰고 커맨드 한 번.

## 0. 말투 — 쓰기 전에 무조건 (2026-08-08 신설)

**`_template.md` 상단 말투 블록을 읽고 시작한다.** 링크 참조로 걸어두면 매번 안 열고 넘어가서 후추님이 같은 지적을 반복했다 (voice drift). 그래서 템플릿 안에 실물로 박아놨다 — `cp`로 복사하면 그 규칙이 파일 맨 위에 딸려온다.

핵심만: **반말 · 마침표 거의 안 씀 · 문장 미완결로 흐림 · 비전문가 눈높이 · 가르치는 톤 금지.**
발행 전에 템플릿 하단 자가 점검 4문항을 실제로 돌린다.

전문 = `Think/outputs/marketing/_foundation/voice_profile.md`

## 1. draft 작성 (posts/*.md)

```bash
cp _template.md 2026-07-10-slug.md
```

파일명 룰: `YYYY-MM-DD-slug.md`. front-matter(title·description·section 필수) 채우고 본문은 md로.
특수 요소(리포트 카드·내생각 박스)는 raw HTML 블록으로 붙여넣으면 그대로 통과됨.

## 2. 로컬 빌드

완성되면 `status: published`로 바꾸고:

```bash
python3 scripts/build.py
```

이 한 번으로 전부 자동:
- **글 HTML 렌더** — `scripts/post_template.html` 디자인 그대로 (OG·JSON-LD·좋아요 버튼 포함)
- **blog/index.html 자동 삽입** — 해당 분류 최상단 + 분류 카운트 갱신 (분류 없으면 신설)
- **sitemap.xml·rss.xml 전체 재생성** (publish.py 자동 호출)
- **공개 HTML의 작성자·발행일·수정일 표시와 JSON-LD 정합성 갱신**
- **blog/text/*.txt와 llms.txt 전체 목록 재생성** — 본문 HTML이 정본이며 텍스트 파일은 직접 편집하지 않음

md 없는 옛 글의 본문은 유지한다. 모든 공개 HTML의 공통 메타데이터와 작성 정보만 갱신한다. 기존 md를 수정할 때는 front-matter에 `modified: YYYY-MM-DD`를 실제 수정일로 넣는다. HTML을 직접 수정했다면 JSON-LD의 `dateModified`를 실제 수정일로 바꾼다. 최초 발행일은 유지한다.

## 3. commit·push

```bash
git add blog/ scripts/ llms.txt sitemap.xml rss.xml
git commit -m "blog: <글 제목 한 줄>"
git push
```

Cloudflare Pages 자동 deploy. 1~2분 뒤 반영.

## 참고 — publish.py 단독 실행

HTML 직접 수정 후 메타데이터·본문 텍스트·llms.txt·sitemap/RSS를 다시 만들 때:

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

## 발행 전 자가 점검 (2026-07-09 후추님 — 두 번 지적 후 근본 fix)

펩랩 리포트·본문을 만든 직후, 발행 전에 아래를 스스로 훑는다:

1. **쉬운말** — 전문어·영문 약어를 첫 등장에 쉬운 말로 풀거나 괄호 풀이. 기준 독자 = "AI=ChatGPT 정도" 아는 사람. 예: RLVR→"정답을 기계가 확인해줘서 반복 훈련이 잘 되는", test-time compute→"답할 때 계산을 더 쓴다", 파운데이션 모델→"범용 AI 모델(챗봇의 그 큰 모델)", acqui-hire→"회사째 인수돼", 벤치마크→"시험 점수". 개념명이 꼭 필요하면 쉬운 풀이 뒤 괄호 병기. `내 생각`은 원래 쉬운 후추 보이스라 해당 없음 — **브리핑이 주 대상**(TickDeck writing-standard 풀어쓰기의 블로그판).
2. **요약 밀도** — 브리핑 `전체 요약` 불릿은 주제 카드 수와 1:1 금지. 핵심 줄기 5개 안팎·각 한 줄, 디테일은 주제 카드가 전담(요약은 스캔용). brief-main 2문장.

## 참고

- 디자인 톤·CSS = `blog/index.html` 상단 `<style>` 영역. snippet 추가만 하면 자동 적용
- 모바일 styling 점검 필요 시 `python3 -m http.server 8000` 로컬 미리보기
- 첫 글 placeholder: TickDeck 6주 검증 누적용 (5/14 시작 영역)


## 글 수정과 AI 접근성 (2026-09-11)

- 개인 글은 실제 작성자의 경험·망설임·감정을 보존한다. 새 일화나 감정을 만들어 넣지 않는다. 브리핑은 중립적인 설명과 발언 귀속을 유지한다.
- 전역 한국어 규칙 `~/.hermes/shared/공통-가드레일.md`의 한국어 말투 부분과 실제 사용자 지적을 적용한다. 문장을 무조건 짧게 자르거나 모든 전문어를 지우지 않는다.
- “단순한 X가 아닌 Y”, “핵심은”, “진짜 문제는”, 대상 없는 “흐름·결·자리·구조”로 문장을 마무리했다면 무엇이 어떻게 달라졌는지 쓴다. 정확한 대조나 전문 개념까지 일괄 금지하지 않는다.
- 사이트를 집으로 바꿔 “우리 집도 재봤더니”라고 쓰는 식의 생활 비유는 사용하지 않는다(2026-09-11 독자 리뷰). 후추님 지정에 따라 자칭은 “내 사이트” 또는 “펩핀치 사이트”로 쓴다. 요청·모니터링 서비스를 그대로 지칭한다.
- 제목·설명·목록 요약·본문의 주장이 일치해야 한다. 통계의 분류 이름을 확정된 원인으로 바꾸지 않는다. 인용은 원문 확인 없이 재작성하지 않는다.
- 본문 텍스트는 공개된 최상위 `blog/posts/*.html`만 추출한다. 초안 md·내부 메모·스크립트·좋아요 버튼·메뉴는 싣지 않는다. 첨부 자료와 출처 링크는 남긴다.
- `llms.txt`는 읽기 편한 안내 파일이다. 검색 노출이나 AI 인용을 보장하지 않는다. 숨은 키워드나 본문에 없는 구조화 데이터를 추가하지 않는다.
- 검증: `python3 -m unittest discover -s scripts -p 'test_*.py'`와 `python3 scripts/build.py`. 로컬 빌드는 배포가 아니다. 게시 승인 후 commit/push한다.

참고: [Google AI 기능 안내](https://developers.google.com/search/docs/appearance/ai-features), [Article 구조화 데이터](https://developers.google.com/search/docs/appearance/structured-data/article).
