# peppinch-site

[peppinch.com](https://peppinch.com) — 1인 lab portfolio site for 후추님 (시즌드 → 펩핀치).

## 구조

| 경로 | 페이지 | 디자인 톤 |
|---|---|---|
| `/` | 메인 sketch · paper mockup · 손글씨 wireframe | rough.js · Kyobo Hand 2019 · #faf6ec paper |
| `/business/` | cinematic portfolio · click-to-expand 6 projects | Hahmlet × Pretendard · 3 palettes (한지에 먹·새벽 3시·비 갠 골목) · salt-grain canvas |
| `/blog/` | base layer · TickDeck 6주 검증 누적용 | 동일 paper 톤 |

## 자산 출처

- `/tmp/peppinch_design/peppinch-v3/` (Claude Design 핸드오프 번들, 2026-05-13)
- chat transcript: `peppinch-v3/chats/chat1.md`

## 로컬 미리보기

```bash
python3 -m http.server 8000
# http://localhost:8000/
```

JSX는 babel/standalone로 런타임 컴파일. 빌드 없음.

## 배포

[`DEPLOY.md`](DEPLOY.md) 참조. Cloudflare Pages + Namecheap DNS 위임 + Cloudflare Email Routing.

## 운영

- 메인 repo·정본
- Ralph 워커 (Think repo의 `.claude/ralph/`) Phase 2 task가 본 repo iteration 담당
- domain: peppinch.com (Namecheap, Auto-renew ON)
- email: pepper@peppinch.com → 후추봇 Gmail forward
