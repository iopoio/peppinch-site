# 블로그 글 기본 레이아웃 (2026-06-15 확정)

펩핀치 블로그 글의 표준 구조. 첫 글(`2026-06-13-all-in-fable5`)에서 확정했고, 다음 글부터 이걸 기본으로 제작한다.

## 구조 = 2개 파일

1. **글 래퍼** `blog/posts/<slug>.html` — 블로그 페이지 셸. 템플릿 = `blog/_template/post.template.html`.
   - 손글씨 메뉴(사이트 정체성) + 단정한 본문(Pretendard) + 크림 종이.
   - 제목 → **요약 3~4줄(실텍스트)** → 리포트(iframe) → **내 생각** → 좋아요 → 다른 글 보기.
   - 폭은 페이지 전체 균일 `max-width:1180px`.
2. **리포트** `blog/posts/<slug>-report.html` — Pepwrap이 생성. `noindex`.
   - 생성기 = `Think/sandbox/meeting-report-tool/src/youtube_report_renderer.py` (2026-06-15부터 이 레이아웃을 자동 출력).
   - 전체 요약 / 화자·출연(한 줄) / **주제별 논의(토픽별 아코디언·제목만 보임)** / 결정·판단 / 오픈 질문 / 다음 액션(3열·⭐ 별표) / 미검증·주의.
   - 리포트가 자기 높이를 부모에 `postMessage`로 알려 iframe 높이를 정확히 맞춤(초기 클리핑·레이스 없음).

## 확정된 규칙 (어기지 말 것)

- **"펩랩"/"Pepwrap" 같은 내부 도구명 노출 금지** — 독자는 모름. "정리한 자료" 정도로.
- **다음 액션 = 독자 관점**("이 글에 관심 생긴 사람이 해볼 것"), 3열(해볼 액션/따라올 산출물/왜), **⭐ 별표**로 꼭 해볼 것 표시(≤5개·3개 OK).
- **주제별 논의 = 토픽별 아코디언** — 제목만 보이고 내용 접힘. 접힌 채로 전체 구조 파악, 보고 싶은 것만 펼침. (통째 토글 X)
- **요약 텍스트는 래퍼에** 둔다 — 리포트가 iframe+noindex라, 이 요약이 검색엔진이 읽는 유일한 본문. SEO 핵심.
- 모바일 가로 오버플로 0 (360/390/414 확인). 메타는 모바일에서 2×2.
- 정치 등 뺄 파트는 빼되, "○○ 파트는 뺐습니다" 한 줄을 리포트 리드에 남긴다(후추님 선호).
- 디자인/브랜드(색·로고·톤) 변경은 후추님 결재.

## 새 글 만들기

1. 영상이면 Pepwrap 파이프라인 실행 → `outputs/youtube_<id>/index.html` 생성 (이미 표준 레이아웃).
   `cp` 해서 `blog/posts/<slug>-report.html`로, `<meta name="robots" content="noindex">` 추가, 필요 시 정치 등 제외 + 리드에 한 줄.
2. `post.template.html` 복사 → `blog/posts/<slug>.html`. `{{ }}` 채우기:
   - `{{SLUG}}`=`<slug>` · `{{REPORT_SLUG}}`=`<slug>-report` · `{{TITLE}}` · `{{DESC}}`/`{{OG_DESC}}` · `{{DATE_DISPLAY}}`(예 `2026 · 06 · 13`)/`{{DATE_ISO}}` · `{{SECTION}}` · `{{KEYWORDS}}` · `{{SUMMARY}}` · `{{MYVIEW_PARAGRAPHS}}`(`<p>...</p>`, 마지막 줄 `<p class="ask">`).
   - 영상 출처 있으면 `{{IS_BASED_ON}}` = `,"isBasedOn":{"@type":"VideoObject","name":"<영상제목>","url":"<url>"}` / 없으면 빈 문자열.
3. `blog/index.html` 카테고리에 카드 추가(`href="/blog/posts/<slug>"` — **`.html` 없이**. Cloudflare가 `.html`을 떼고 308 리다이렉트하므로 내부 링크는 항상 클린 URL).
4. `sitemap.xml`에 `<loc>https://www.peppinch.com/blog/posts/<slug></loc>` 추가.
5. 푸시 전 모바일·PC 실제 렌더 확인(헤드리스는 최소폭 500px라 390 측정은 CDP `Emulation.setDeviceMetricsOverride` 사용).

## 좋아요/조회수

- 조회수 = GA(`G-LZ7ZXMFEBM`)로 후추님만 봄. 화면 표시 없음.
- 좋아요 = localStorage 토글(각자 자기 것만). 공개 카운터는 Cloudflare Worker+KV 필요(미구현).
