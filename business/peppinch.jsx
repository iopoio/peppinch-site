/* peppinch.jsx — typography-first portfolio for peppinch.com */
const { useState, useEffect, useRef, useCallback, useMemo } = React;

/* ------------- TWEAK DEFAULTS ------------- */
const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
  "palette": "fog",
  "pairing": "hahmlet",
  "cursorReactive": true,
  "saltMotif": true,
  "intensity": "normal"
}/*EDITMODE-END*/;

/* ------------- PALETTES ------------- */
const PALETTES = {
  hanji: {
    label: "한지에 먹",
    sub: "Ink on hanji",
    bg: "#F1ECE0", ink: "#161410", accent: "#D63A1F",
    muted: "rgba(22,20,16,.5)", hairline: "rgba(22,20,16,.18)"
  },
  subway: {
    label: "새벽 3시",
    sub: "Subway 3am",
    bg: "#0E0F12", ink: "#E8E4DA", accent: "#5DF0E0",
    muted: "rgba(232,228,218,.5)", hairline: "rgba(232,228,218,.14)"
  },
  alley: {
    label: "비 갠 골목",
    sub: "After-rain alley",
    bg: "#2A2F33", ink: "#EFEAE0", accent: "#FF9B3D",
    muted: "rgba(239,234,224,.55)", hairline: "rgba(239,234,224,.16)"
  },
  fog: {
    label: "옅은 안개",
    sub: "Fog grey",
    bg: "#4D545B", ink: "#F2EFE8", accent: "#FFB066",
    muted: "rgba(242,239,232,.55)", hairline: "rgba(242,239,232,.18)"
  }
};

/* ------------- TYPE PAIRINGS ------------- */
const PAIRINGS = {
  hahmlet: {
    label: "Hahmlet × Pretendard",
    sub: "cinematic serif drama × modern sans whisper",
    display: '"Hahmlet", "Noto Serif KR", serif',
    body: '"Pretendard Variable", "Pretendard", system-ui, sans-serif',
    variable: true   // body supports variable weight axis
  },
  blackhan: {
    label: "Black Han Sans × IBM Plex KR",
    sub: "massive impact × geometric quiet",
    display: '"Black Han Sans", "Hahmlet", sans-serif',
    body: '"IBM Plex Sans KR", system-ui, sans-serif',
    variable: false
  }
};

/* ------------- PROJECTS ------------- */
const PROJECTS = [
  {
    id: 1, name: "Publace", ko: "퍼블레이스",
    line: "도시의 빈 자리를 가만히 들여다보면, 다음 이야기가 보인다.",
    tag: "공공 유휴공간 × AI 매칭",
    year: "2024",
    role: "Concept / Build",
    href: "#"
  },
  {
    id: 2, name: "EatScan", ko: "잇스캔",
    line: "라벨을 한 번 비추면, 먹어도 되는지 아닌지를 조용히 알려준다.",
    tag: "식품 알레르기 라벨 스캐너",
    year: "2024",
    role: "Solo build",
    href: "#"
  },
  {
    id: 3, name: "이달여행", ko: "IdalTrip",
    line: "이번 달, 어디에서 무엇을 먹고 — 어떤 축제를 스칠지.",
    tag: "축제 기반 여행 코스",
    year: "2025",
    role: "Concept / Build",
    href: "#"
  },
  {
    id: 4, name: "잡솔트", ko: "JobSort",
    line: "공고는 너무 많고, 나에게 맞는 건 늘 한두 개.",
    tag: "공공기관 직무 매칭",
    year: "2025",
    role: "In progress",
    href: "#"
  },
  {
    id: 5, name: "TickDeck", ko: "틱덱",
    line: "URL 한 줄을, 발표 슬라이드 한 벌로.",
    tag: "URL → Slides",
    year: "2025",
    role: "Solo build",
    href: "#"
  },
  {
    id: 6, name: "toys", ko: "토이즈",
    line: "틈틈이 재미로 만든 작은 도구들의 진열대.",
    tag: "작은 실험 묶음",
    year: "2025",
    role: "WIP",
    href: "#"
  }
];

/* ------------- HOOKS ------------- */
function useCursor() {
  const ref = useRef({ x: 0, y: 0, tx: 0, ty: 0 });
  useEffect(() => {
    const el = document.getElementById("cursor");
    if (!el) return;
    let raf;
    const onMove = (e) => {
      ref.current.tx = e.clientX;
      ref.current.ty = e.clientY;
    };
    const tick = () => {
      ref.current.x += (ref.current.tx - ref.current.x) * 0.22;
      ref.current.y += (ref.current.ty - ref.current.y) * 0.22;
      el.style.transform = `translate(${ref.current.x}px, ${ref.current.y}px) translate(-50%,-50%)`;
      raf = requestAnimationFrame(tick);
    };
    window.addEventListener("mousemove", onMove);
    raf = requestAnimationFrame(tick);
    return () => { window.removeEventListener("mousemove", onMove); cancelAnimationFrame(raf); };
  }, []);
  return ref;
}

/* Cursor-reactive variable weight: every .reactive char gets weight based on distance to cursor */
function useReactiveType(enabled, intensity) {
  useEffect(() => {
    if (!enabled) {
      document.querySelectorAll(".reactive .ch").forEach(c => {
        c.style.fontVariationSettings = '"wght" 400';
      });
      return;
    }
    let raf;
    const radius = intensity === "dramatic" ? 320 : intensity === "slow" ? 200 : 260;
    const maxW = intensity === "dramatic" ? 900 : intensity === "slow" ? 700 : 800;
    const minW = 200;
    let mx = -9999, my = -9999;
    const onMove = (e) => { mx = e.clientX; my = e.clientY; };
    window.addEventListener("mousemove", onMove);
    const tick = () => {
      const chars = document.querySelectorAll(".reactive .ch");
      chars.forEach(ch => {
        const r = ch.getBoundingClientRect();
        if (r.bottom < -200 || r.top > window.innerHeight + 200) return;
        const cx = r.left + r.width/2;
        const cy = r.top + r.height/2;
        const dx = mx - cx, dy = my - cy;
        const d = Math.sqrt(dx*dx + dy*dy);
        const t = Math.max(0, 1 - d / radius);
        const w = Math.round(minW + (maxW - minW) * t);
        ch.style.fontVariationSettings = `"wght" ${w}`;
      });
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => { window.removeEventListener("mousemove", onMove); cancelAnimationFrame(raf); };
  }, [enabled, intensity]);
}

/* ------------- LETTER SCRAMBLE — slower, calmer ------------- */
const SCRAMBLE_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
function ScrambleText({ text, className }) {
  const [out, setOut] = useState(text);
  const rafRef = useRef(null);
  const playingRef = useRef(false);

  // Reset displayed text when source changes
  useEffect(() => { setOut(text); }, [text]);

  const play = useCallback(() => {
    if (playingRef.current) return;
    playingRef.current = true;
    const original = text;
    const len = original.length;

    // Slower: ~80 frames total (~1.3s @60fps), and only swap a random char every ~3 frames
    const totalFrames = 80;
    // Each char settles in sequence, left to right
    const settleAt = original.split("").map((_, i) =>
      Math.floor((i / Math.max(1, len - 1)) * totalFrames * 0.85) + 6
    );

    cancelAnimationFrame(rafRef.current);
    let frame = 0;
    let lastChars = original.split(""); // start as original; gradually scramble unsettled positions
    const tick = () => {
      const s = [];
      for (let i = 0; i < len; i++) {
        const ch = original[i];
        if (ch === " " || ch === "\u00A0") { s.push(ch); continue; }
        if (frame >= settleAt[i]) {
          s.push(ch);
          lastChars[i] = ch;
        } else {
          // only swap every 3 frames so it's not strobing
          if (frame % 3 === 0) {
            lastChars[i] = SCRAMBLE_CHARS[Math.floor(Math.random() * SCRAMBLE_CHARS.length)];
          }
          s.push(lastChars[i]);
        }
      }
      setOut(s.join(""));
      frame++;
      if (frame <= totalFrames) {
        rafRef.current = requestAnimationFrame(tick);
      } else {
        setOut(original);
        playingRef.current = false;
      }
    };
    rafRef.current = requestAnimationFrame(tick);
  }, [text]);

  useEffect(() => () => cancelAnimationFrame(rafRef.current), []);

  return (
    <span
      className={className}
      onMouseEnter={play}
      onTouchStart={play}
    >{out}</span>
  );
}

/* Splits text into per-character spans for variable-weight + animation hooks */
function SplitText({ text, className = "", reactive = true }) {
  const chars = useMemo(() => Array.from(text), [text]);
  return (
    <span className={(reactive ? "reactive " : "") + className}>
      {chars.map((c, i) => (
        <span key={i} className="ch" style={{ display: "inline-block" }} aria-hidden={c === " "}>
          {c === " " ? "\u00A0" : c}
        </span>
      ))}
    </span>
  );
}

/* ------------- SALT CANVAS ------------- */
function SaltCanvas({ enabled, accent, ink, mutedRgb }) {
  const ref = useRef(null);
  useEffect(() => {
    if (!enabled) return;
    const canvas = ref.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    let w, h, raf;
    const grains = [];
    const resize = () => {
      const r = canvas.getBoundingClientRect();
      w = canvas.width = r.width * devicePixelRatio;
      h = canvas.height = r.height * devicePixelRatio;
      canvas.style.width = r.width + "px";
      canvas.style.height = r.height + "px";
    };
    resize();
    window.addEventListener("resize", resize);
    let mx = w/2, my = h/2;

    const onMove = (e) => {
      const r = canvas.getBoundingClientRect();
      mx = (e.clientX - r.left) * devicePixelRatio;
      my = (e.clientY - r.top) * devicePixelRatio;
      // emit grains
      for (let i = 0; i < 2; i++) {
        grains.push({
          x: mx + (Math.random() - 0.5) * 24 * devicePixelRatio,
          y: my + (Math.random() - 0.5) * 24 * devicePixelRatio,
          vx: (Math.random() - 0.5) * 0.4,
          vy: 0.4 + Math.random() * 0.8,
          life: 60 + Math.random() * 80,
          age: 0,
          size: (0.6 + Math.random() * 1.4) * devicePixelRatio,
          color: Math.random() < 0.12 ? accent : ink
        });
      }
    };
    window.addEventListener("mousemove", onMove);

    // initial scatter
    for (let i = 0; i < 200; i++) {
      grains.push({
        x: Math.random() * w,
        y: Math.random() * h,
        vx: 0, vy: 0,
        life: 9999, age: 0,
        size: (0.5 + Math.random() * 1.2) * devicePixelRatio,
        color: ink, scatter: true,
        baseAlpha: 0.05 + Math.random() * 0.15
      });
    }

    const tick = () => {
      ctx.clearRect(0, 0, w, h);
      for (let i = grains.length - 1; i >= 0; i--) {
        const g = grains[i];
        if (!g.scatter) {
          g.x += g.vx;
          g.y += g.vy;
          g.vy += 0.012;
          g.age++;
          if (g.age > g.life) { grains.splice(i, 1); continue; }
          const a = 1 - g.age / g.life;
          ctx.fillStyle = g.color;
          ctx.globalAlpha = a * 0.85;
          ctx.fillRect(g.x, g.y, g.size, g.size);
        } else {
          ctx.fillStyle = g.color;
          ctx.globalAlpha = g.baseAlpha;
          ctx.fillRect(g.x, g.y, g.size, g.size);
        }
      }
      ctx.globalAlpha = 1;
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => {
      window.removeEventListener("mousemove", onMove);
      window.removeEventListener("resize", resize);
      cancelAnimationFrame(raf);
    };
  }, [enabled, accent, ink]);
  return <canvas ref={ref} className="salt-canvas" />;
}

/* ------------- PROJECT INDEX (click to expand) ------------- */
function ProjectIndex({ projects }) {
  const [openId, setOpenId] = useState(null);
  return (
    <section className="index">
      <div className="label">02 — 인덱스 · index of works ({String(projects.length).padStart(2,"0")})</div>
      <ol>
        {projects.map((p, i) => {
          const isOpen = openId === p.id;
          return (
            <li key={p.id} className={"idx-item hoverable" + (isOpen ? " open" : "")}>
              <button
                type="button"
                className="idx-row"
                onClick={() => setOpenId(isOpen ? null : p.id)}
                aria-expanded={isOpen}
              >
                <span className="idx-num">{String(i+1).padStart(2,"0")}</span>
                <span className="idx-name">
                  <ScrambleText text={p.name} />
                  <span className="ko">{p.ko}</span>
                </span>
                <span className="idx-meta">{p.tag}</span>
                <span className="idx-chev" aria-hidden="true">{isOpen ? "—" : "+"}</span>
              </button>
              <div className="idx-body" style={{ gridTemplateRows: isOpen ? "1fr" : "0fr" }}>
                <div className="idx-body-inner">
                  <p className="idx-line">{p.line}</p>
                  <div className="idx-foot">
                    <span className="idx-tag">{p.year} · {p.role}</span>
                    <a className="idx-visit" href={p.href} target="_blank" rel="noopener noreferrer" onClick={(e) => e.stopPropagation()}>
                      {p.ko} 보러가기 <span aria-hidden="true">→</span>
                    </a>
                  </div>
                </div>
              </div>
            </li>
          );
        })}
      </ol>
    </section>
  );
}

/* ------------- APP ------------- */
function App() {
  const [tweaks, setTweak] = useTweaks(TWEAK_DEFAULTS);
  const palette = PALETTES[tweaks.palette] || PALETTES.hanji;
  const pairing = PAIRINGS[tweaks.pairing] || PAIRINGS.hahmlet;
  const reactive = tweaks.cursorReactive && pairing.variable; // only Pretendard supports the wght axis
  const cursorRef = useCursor();
  useReactiveType(reactive, tweaks.intensity);

  // Apply palette + fonts as CSS variables on :root
  useEffect(() => {
    const r = document.documentElement;
    r.style.setProperty("--bg", palette.bg);
    r.style.setProperty("--ink", palette.ink);
    r.style.setProperty("--accent", palette.accent);
    r.style.setProperty("--muted", palette.muted);
    r.style.setProperty("--hairline", palette.hairline);
    r.style.setProperty("--display-font", pairing.display);
    r.style.setProperty("--body-font", pairing.body);
  }, [palette, pairing]);

  // hover state for cursor halo
  useEffect(() => {
    const cur = document.getElementById("cursor");
    const ons = document.querySelectorAll("a, .hoverable, .index li, .project .name");
    const enter = () => cur.classList.add("hover");
    const leave = () => cur.classList.remove("hover");
    ons.forEach(el => { el.addEventListener("mouseenter", enter); el.addEventListener("mouseleave", leave); });
    return () => ons.forEach(el => { el.removeEventListener("mouseenter", enter); el.removeEventListener("mouseleave", leave); });
  });

  return (
    <>
      <div className="frame">
        <div className="corner tl" style={{ pointerEvents: "auto", zIndex: 100 }}>
          PEPPINCH<br/>SOLO STUDIO · KR<br/><br/>
          <a href="/" style={{ color: "var(--accent)", textDecoration: "none", borderBottom: "1.5px solid var(--accent)", padding: "2px 0", letterSpacing: ".12em", pointerEvents: "auto", position: "relative", zIndex: 101 }}>← 메인 사이트 보기</a>
        </div>
        <div className="corner tr">PALETTE — {palette.label}<br/>{palette.sub}</div>
        <div className="corner bl">EST. 2024</div>
        <div className="corner br">{pairing.label}</div>
      </div>

      {/* HERO */}
      <section className="hero">
        <div className="eyebrow"><span className="dot"></span>peppinch.com — solo lab, kr</div>
        <h1>
          <span className="pinch">A Pinch Of</span>{' '}
          <span className="pepper">
            <SplitText text="Pepper." className="" reactive={pairing.variable} />
          </span>
          <span className="ko">
            <SplitText text="한 꼬집의 후추." reactive={pairing.variable} />
          </span>
        </h1>
        <p className="sub">
          신사업을 기획하고, 만들고 — 가끔은 갈아 엎는다.{' '}
          <em>혼자, AI와 함께.</em><br/>
          A solo lab in Seoul, building small useful things.
          The kind that don't change the world, only your Tuesday.
        </p>
        <div className="scrolltip"><span className="line"></span> scroll · 스크롤</div>
      </section>

      {/* MANIFESTO */}
      <section className="manifesto">
        <div className="number">01 — 작업 노트</div>
        <p>
          크지 않게.{' '}
          <span className="strike">빠르게.</span>{' '}
          <span className="accent">정확하게.</span><br/>
          한 꼬집씩 — 무언가가 너무 심심할 때.
        </p>
        <div className="signoff">
          <span>— 페핀치 / Peppinch</span>
          <span>SINCE TWENTY · TWENTY · FOUR</span>
        </div>
      </section>

      {/* INDEX — click to expand */}
      <ProjectIndex projects={PROJECTS} />


      {/* NOW + SALT */}
      <section className="now">
        {tweaks.saltMotif && <SaltCanvas enabled={true} accent={palette.accent} ink={palette.ink} />}
        <div className="label">03 — 지금 · what i'm on this month</div>
        <h2>
          요즘은 <em>잡솔트</em>와 <em>이달여행</em>을<br/>
          한 꼬집씩 다듬는 중.
        </h2>
        <ul>
          <li>
            <strong>지금 / now</strong>
            잡솔트 — 채용 매칭 더 빠르게
          </li>
          <li>
            <strong>다음 / next</strong>
            이달여행 — 추천 흐름 더 자연스럽게
          </li>
          <li>
            <strong>읽는 중 / reading</strong>
            『프로덕트 매니지먼트의 기술』, 그리고 좀 졸린 책들
          </li>
          <li>
            <strong>연료 / fuel</strong>
            새벽 3시의 조용함, 한 꼬집의 후추
          </li>
        </ul>
      </section>

      {/* CONTACT */}
      <section className="contact">
        <div className="label">04 — 연락 · ping me</div>
        <h2>
          말 걸어요.<br/>
          <a href="mailto:pepper@peppinch.com" style={{ fontSize: "0.65em", wordBreak: "break-all" }}>pepper@peppinch.com</a>
        </h2>
        <div className="lines">
          <div>
            <strong>email</strong>
            <a href="mailto:pepper@peppinch.com">pepper@peppinch.com</a>
          </div>
          <div>
            <strong>twitter / x</strong>
            <a href="https://x.com/peppinch_" target="_blank" rel="noopener noreferrer">@peppinch_</a>
          </div>
          <div>
            <strong>site</strong>
            <a href="https://peppinch.com">peppinch.com</a>
          </div>
          <div>
            <strong>roles</strong>
            신사업 개발자 · 기획자 · 솔로 메이커
          </div>
        </div>
      </section>

      <footer>
        <span>© {new Date().getFullYear()} <span className="pinch">peppinch</span> — pinch of pepper</span>
        <span>made slow, in seoul · 🧂</span>
      </footer>

      {/* TWEAKS PANEL */}
      <TweaksPanel>
        <TweakSection label={`Palette · ${palette.label}`}>
          <TweakRadio
            label="scheme"
            value={tweaks.palette}
            onChange={(v) => setTweak("palette", v)}
            options={[
              { value: "fog", label: "안개" },
              { value: "hanji", label: "한지" },
              { value: "subway", label: "새벽" },
              { value: "alley", label: "골목" },
            ]}
          />
          <div style={{ fontSize: 10, opacity: .55, marginTop: 4, fontFamily: 'ui-monospace, monospace', letterSpacing: '.04em' }}>
            {palette.sub} · {palette.bg} / {palette.ink} / {palette.accent}
          </div>
        </TweakSection>

        <TweakSection label="Type pairing">
          <TweakRadio
            label="pairing"
            value={tweaks.pairing}
            onChange={(v) => setTweak("pairing", v)}
            options={[
              { value: "hahmlet", label: "Hahmlet" },
              { value: "blackhan", label: "Black Han" },
            ]}
          />
          <div style={{ fontSize: 10, opacity: .55, marginTop: 4, fontFamily: 'ui-monospace, monospace', letterSpacing: '.04em' }}>
            {pairing.sub}
          </div>
        </TweakSection>

        <TweakSection label="Interactions">
          <TweakToggle
            label="Cursor-reactive weight"
            value={tweaks.cursorReactive}
            onChange={(v) => setTweak("cursorReactive", v)}
          />
          <div style={{ fontSize: 10, opacity: .5, marginTop: -2, marginBottom: 4, fontFamily: 'ui-monospace, monospace' }}>
            requires Pretendard (variable wght)
          </div>
          <TweakToggle
            label="Salt motif"
            value={tweaks.saltMotif}
            onChange={(v) => setTweak("saltMotif", v)}
          />
          <TweakSelect
            label="Intensity"
            value={tweaks.intensity}
            onChange={(v) => setTweak("intensity", v)}
            options={[
              { value: "slow", label: "slow" },
              { value: "normal", label: "normal" },
              { value: "dramatic", label: "dramatic" },
            ]}
          />
        </TweakSection>
      </TweaksPanel>
    </>
  );
}

ReactDOM.createRoot(document.getElementById("app")).render(<App />);
