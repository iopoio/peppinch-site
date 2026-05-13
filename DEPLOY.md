# 배포 plan — peppinch.com

## 1. Cloudflare Pages

- Cloudflare dashboard → Pages → Connect to Git → `iopoio/peppinch-site` 선택
- Production branch: `main`
- Build command: **(없음)** — 정적 HTML
- Build output directory: `/` (repo root)
- Framework preset: None
- 첫 build = repo 그대로 publish

## 2. Custom domain 연결

### 2-1. Namecheap → Cloudflare 네임서버 위임 (이미 됐을 수도 있음 — 자산.md 확인)

- Namecheap dashboard → peppinch.com → Nameservers → Custom DNS
- Cloudflare가 부여한 NS (예: `xxx.ns.cloudflare.com`) 입력
- 전파 24~48h

### 2-2. Cloudflare Pages → Custom domains

- Pages project → Custom domains → Add → `peppinch.com` + `www.peppinch.com`
- Cloudflare 자동 SSL 발급 (Universal SSL)

## 3. Email Routing (Cloudflare 무료)

- Cloudflare dashboard → peppinch.com → Email → Email Routing
- Destination address: 후추봇 Gmail (verify 의무)
- Custom address: `pepper@peppinch.com` → 후추봇 Gmail forward
- 자산.md 정합 (`hello@peppinch.com`도 함께 추가 권장 — chat에서 사용)

## 4. Analytics

- Cloudflare Web Analytics (Cookie 없음, 프라이버시 친화) — 무료
- Pages project → Web Analytics 활성화

## 5. Pages Functions (선택)

- API 필요 시 `functions/` 폴더 신설 — 본 site MVP에는 X

## 6. Preview deploy

- main 외 모든 branch는 자동 Preview URL 받음 (`<branch>.peppinch-site.pages.dev`)
- Ralph 워커가 작업 branch 생성 → preview에서 검증 → main merge

## 7. 캐시

- 정적 HTML/CSS/JS = Cloudflare CDN 자동
- 폰트 (`/fonts/KyoboHandwriting2019.otf` 4.8MB) = 첫 load 후 캐시. 추후 woff2 변환 권장 (50% 절감)

## 8. SEO / Open Graph (Ralph task 등재 예정)

- `<meta name="description">` · `<meta property="og:image">` · `favicon` (🧂 PNG)
- sitemap.xml · robots.txt

## 검증

- 배포 후 lighthouse score · 모바일 반응형 · 폰트 로딩 시간 점검
- 후추님 직접 view → 후속 polish

## 비용

| 항목 | 비용 |
|---|---|
| Cloudflare Pages | $0 (무료 tier 500 build/월) |
| Cloudflare Email Routing | $0 |
| Cloudflare DNS | $0 |
| Cloudflare Web Analytics | $0 |
| Namecheap domain | $14.98/yr (갱신가) |
| **합계** | **$15/yr** |
