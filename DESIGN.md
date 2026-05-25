# Peppinch Site — Design System

> Claude Code 자동 read 파일. 향후 컴포넌트·페이지 추가 시 본 파일 기준 유지.
> 갱신: 2026-05-25

---

## 브랜드 개요

**펩핀치(Peppinch)** — "한 꼬집의 양념 같은 AI 도구들"

4층 톤 분리 철학:
1. **메인 `/`** — Paper Sketch (rough.js, 손글씨, 종이 질감)
2. **캐릭터 라인업** — 5살 크레용 톤 (AI 이미지)
3. **진열대 도구 UI** — 완성도 우선 (TickDeck 등)
4. **`/business/`** — Cinematic typography-first (투자자·B2B용)

---

## 컬러 시스템

### Main — Paper Sketch

```css
--paper:       #faf6ec   /* 배경: 베이지 종이색 */
--paper-shade: #efe9d8   /* 카드 음영 */
--ink:         #2a2823   /* 본문: 진한 잉크 */
--pencil:      #3a352c   /* 보조 텍스트 */
--red:         #c8412c   /* 강조·액션·스탬프 */
--blue:        #2f5fa8   /* 링크·노트 */
```

### Business — Cinematic Hanji

```css
--bg:       #F1ECE0               /* 배경: 한지색 */
--ink:      #161410               /* 본문: 진한 먹색 */
--accent:   #D63A1F               /* 강조: 붉은 악센트 */
--muted:    rgba(22,20,16,0.5)    /* 보조 텍스트 */
--hairline: rgba(22,20,16,0.18)   /* 경계선 */
```

---

## 타이포그래피

### Main (Paper Sketch)

| 용도 | 폰트 | 비고 |
|---|---|---|
| 본문·UI 전반 | Kyobo Handwriting 2019 | `fonts/` 로컬 woff2/otf |
| 영문 헤드라인 | Shantell Sans | Google Fonts, 300–800 variable |
| 핸드라이팅 accent | Just Me Again Down Here | Google Fonts |

- 폰트 variable axis 활용: `font-variation-settings: "wght" 500, "BNCE" 0, "INFM" 60`
- 유동 크기: `font-size: clamp(64px, 9vw, 124px)`

### Business (Cinematic Hanji)

| 용도 | 폰트 | 비고 |
|---|---|---|
| 디스플레이·헤드라인 | Hahmlet | serif, 100–900 variable |
| 한국어 본문 | IBM Plex Sans KR | 100–700 |
| 한글 굵음 | Black Han Sans | 400 |
| 영문 본문 | Pretendard Variable | 100–900 |
| 코드·모노 | IBM Plex Mono | 300, 400, 500 |

---

## 레이아웃

```css
.page {
  max-width: 1320px;
  margin: 0 auto;
  padding: 60px 56px 120px;   /* 데스크톱 */
}

/* 태블릿 (max 900px) */
padding: 36px 22px 72px;

/* 모바일 (max 600px) */
padding: 32px 18px 64px;
```

### 카드 그리드

```css
.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);   /* 1440px+ */
  gap: 32px 28px;
  align-items: stretch;
}

/* 900px 이하: 2열 */
/* 600px 이하: 1열 */
```

### 섹션 간격

- 섹션 레이블 상단: `margin: 60px 0 8px`
- hero 하단: `margin-bottom: 70px`
- TODO 상단: `margin-top: 88px`
- footer: `margin-top: 100px`

---

## 컴포넌트 패턴

### 카드

```css
.card {
  padding: 28px 24px 22px;
  min-height: 240px;
  height: 100%;
  position: relative;
  transform: rotate(var(--r, 0deg));   /* JS 동적 회전 */
}
```

- 프레임: **RoughJS** `rc.rectangle()` — roughness 2.4, bowing 2.2
  - 일반 카드: stroke `#3a352c`, strokeWidth 1.8
  - TODO 카드: stroke `#c8412c`, strokeWidth 2.4

### 텍스트 계층 (카드 내부)

```css
.card .num  { font-size: 12px; letter-spacing: 0.15em; color: var(--red); text-transform: uppercase; }
.card .name { font-size: clamp(32px, 5vw, 42px); font-weight: 700; line-height: 0.95; }
.card .ko   { font-size: 20px; color: var(--pencil); opacity: 0.8; }
.card .line { font-size: 19px; line-height: 1.55; color: var(--pencil); }
.card .foot { font-size: 15.5px; letter-spacing: 0.08em; text-transform: uppercase; opacity: 0.7; }
```

### 스탬프 버튼

```css
.stamp {
  border: 2.5px solid var(--red);
  color: var(--red);
  padding: 8px 14px 6px;
  font-size: 13px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  transform: rotate(6deg);
  box-shadow: inset 0 0 0 1px rgba(200,65,44,.3);
}
```

### WIP 스티키 노트

```css
.card.wip::after {
  content: "작업중";
  background: #fde88a;
  font-size: 15px;
  padding: 8px 13px 6px;
  transform: rotate(8deg);
  box-shadow: 0 2px 4px rgba(0,0,0,.1);
}
```

### 구멍 펀치

```css
.holes span {
  width: 16px; height: 16px;
  background: radial-gradient(circle at 35% 35%, #d4cdb8 0%, #c0b89e 60%, #a8a087 100%);
  box-shadow: inset 1px 1px 2px rgba(0,0,0,.25);
}
```

---

## 인터랙션

### Shantell Sans Variable Axis (마우스 반응)

카드 hover 또는 커서 거리에 따라 variable font axis 조정:

```css
.card:hover .name {
  letter-spacing: 0.04em;
  color: var(--red);
  font-variation-settings: "wght" 750, "BNCE" 0, "INFM" 60;
}
```

### 타이프라이터 (카드 hover)

```javascript
// 90ms per character
el._sint = setInterval(() => {
  el.textContent = original.slice(0, i++);
}, 90);
```

### 핸드라이팅 SVG 애니메이션

```css
.name .hw {
  stroke: var(--red);
  stroke-dasharray: 100;
  stroke-dashoffset: 100;
  animation: hw-draw 0.22s ease-out forwards;
}
/* 최대 22개 스트로크, 0.1s stagger */
```

### 종이 질감

```css
body::before {
  background-image:
    repeating-linear-gradient(91deg, transparent 0 38px, rgba(0,0,0,.022) 38px 39px),
    repeating-linear-gradient(2deg, transparent 0 46px, rgba(0,0,0,.022) 46px 47px);
  mix-blend-mode: multiply;
}
/* body::after: feTurbulence SVG grain, opacity 0.45 */
```

---

## 금지 패턴

**브랜드 위반:**
- 순백 `#FFFFFF` 배경 — 반드시 종이색(`#faf6ec`) 또는 한지색(`#F1ECE0`) 사용
- 깔끔한 직선 테두리 — 메인 카드는 반드시 RoughJS 프레임
- Kyobo Handwriting 없이 Pretendard 단독 (메인에서)

**AI 디자인 함정:**
- 보라·핑크 그라디언트 배경
- 모든 카드에 이모지 도배 (✨🚀💡)
- 패스텔 무지개 배지 (등급마다 다른 색)
- 모든 버튼 hover scale-105 (애니메이션 인플레)
- "Lorem ipsum" 임시 텍스트 노출
- 8px 미만 폰트

---

## 파일 구조 참고

```
peppinch-site/
├── index.html          메인 (Paper Sketch 톤)
├── business/
│   └── index.html      비즈니스 (Cinematic Hanji 톤)
├── fonts/
│   └── KyoboHandwriting2019.otf
└── DESIGN.md           ← 본 파일
```

---

## 갱신 이력

- 2026-05-25 신설 — 실 코드 grep + 브랜드 메모리 기반 작성 (클차장)
