<!-- _template.md — 새 글 draft template (2026-07-08 빌드 시스템 도입 후 형식)
파일명: YYYY-MM-DD-slug.md (예: 2026-07-10-tickdeck-pivot.md)
완성되면 status: published로 바꾸고 `python3 scripts/build.py` 한 번 — 끝.
(글 HTML·인덱스 행·sitemap·RSS 전부 자동 생성) -->

---
title: <한 줄 제목 — 글 페이지 h1이자 og:title>
description: <한 줄 설명 — 검색·SNS 미리보기에 노출>
summary: <인덱스 목록 요약 2~3줄. 생략하면 description 재사용>
section: <분류 — AI랑 만들기 | 관심있는 것들 정리 | 주식 이야기 | (새 분류면 자동 신설)>
tags: <쉼표 구분 — 팔란티어, AI주권>
status: draft
---

첫 문단. 빈 줄로 문단 구분. **강조**·[링크](https://...)·같은 문단 안 줄바꿈은 그대로 <br> 처리.

## 소제목

> 인용 블록

- 목록도
- 됩니다

<!-- 리포트 카드·내생각(mv) 박스 같은 특수 요소는 raw HTML 블록으로 그대로 붙여넣으면 통과됨:
<a class="rptcard" href="/blog/posts/...-report">
  <span class="rl"><span class="rk">영상 핵심 정리 브리핑</span><span class="rt">리포트 보기</span></span>
  <span class="ra">→</span>
</a>
-->
