"""카드 이름 핸드라이팅 SVG 생성기 (7/2 신설)

Kyobo 폰트에서 글자 외곽선(clipPath) + 스켈레톤 획 중심선을 추출해
붓이 획을 따라 그리는 stroke-dashoffset SVG를 만든다 (CodePen XYNdvd 기법).
index.html의 HANDWRITING_SVGS 블록을 stdout으로 출력 — 이름 바뀌면 재실행해서 교체.

deps: python3 -m venv .venv && .venv/bin/pip install fonttools pillow scikit-image scipy numpy
run:  .venv/bin/python scripts/gen_handwriting_svg.py
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from skimage.morphology import skeletonize
from skimage.measure import approximate_polygon
from scipy.ndimage import distance_transform_edt
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
import os

NAMES = ['Publace', 'Pepstocks', 'EatScan', '이달여행', '잡솔트', 'TickDeck', 'etc']
FONT = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'KyoboHandwriting2019.otf')
PXEM = 300      # 래스터 해상도 (px per em)
SPEED = 4500    # 붓 속도 (font units/s) — 카드 호버라 빠르게
GAP = 0.02      # 글자 사이 간격(s)
FS = 90         # viewBox 기준 폰트 크기

tt = TTFont(FONT)
cmap = tt.getBestCmap()
glyphset = tt.getGlyphSet()
upm = tt['head'].unitsPerEm
pil_font = ImageFont.truetype(FONT, PXEM)


def skeleton_strokes(ch):
    """글자 래스터화 → 스켈레톤 → 획 중심선 폴리라인(font units, y-up) + 잉크 굵기"""
    W = H = PXEM * 2
    pad, base = PXEM // 2, PXEM + PXEM // 3
    img = Image.new('L', (W, H), 0)
    ImageDraw.Draw(img).text((pad, base), ch, fill=255, font=pil_font, anchor='ls')
    mask = np.array(img) > 128
    if not mask.any():
        return [], 0
    skel = skeletonize(mask)
    ink_px = distance_transform_edt(mask)[skel].max() * 2
    pts = set(zip(*np.nonzero(skel)))

    def nbrs(p):
        y, x = p
        return [(y + dy, x + dx) for dy in (-1, 0, 1) for dx in (-1, 0, 1)
                if (dy or dx) and (y + dy, x + dx) in pts]

    deg = {p: len(nbrs(p)) for p in pts}
    nodes = [p for p in pts if deg[p] != 2]
    visited = set()
    segs = []

    def walk(start, nxt):
        line = [start, nxt]
        visited.add((start, nxt)); visited.add((nxt, start))
        prev, cur = start, nxt
        while deg[cur] == 2:
            nx = [q for q in nbrs(cur) if q != prev and (cur, q) not in visited]
            if not nx:
                break
            prev, cur = cur, nx[0]
            visited.add((prev, cur)); visited.add((cur, prev))
            line.append(cur)
        return line

    for n in nodes:
        for q in nbrs(n):
            if (n, q) not in visited:
                segs.append(walk(n, q))
    loop_pts = pts - {p for s in segs for p in s}  # 순수 루프 (o, ㅇ 등)
    while loop_pts:
        start = min(loop_pts)
        q = [p for p in nbrs(start) if p in loop_pts]
        if not q:
            loop_pts.discard(start); continue
        line = walk(start, q[0])
        segs.append(line)
        loop_pts -= set(line)

    out = []
    for s in segs:
        if len(s) < ink_px * 0.7:  # 스켈레톤 노이즈 가시 제거
            continue
        arr = approximate_polygon(np.array(s, float), tolerance=1.5)
        out.append([((x - pad) / PXEM * upm, (base - y) / PXEM * upm) for y, x in arr])
    return out, ink_px / PXEM * upm


def order_segs(segs):
    """왼쪽 위 획부터 그리디 최근접 — 필기 순서 근사 (7/2 후추님: 자동 순서 확정)"""
    rem = [s[:] for s in segs]
    ordered, cur = [], None
    while rem:
        bi, brev, bd = 0, False, 1e18
        for i, s in enumerate(rem):
            for rev in (False, True):
                p = s[-1] if rev else s[0]
                d = (p[0] * 1.5 - p[1] * 0.5) if cur is None else (p[0] - cur[0]) ** 2 + (p[1] - cur[1]) ** 2
                if d < bd:
                    bd, bi, brev = d, i, rev
        s = rem.pop(bi)
        if brev:
            s.reverse()
        ordered.append(s)
        cur = s[-1]
    return ordered


def seg_len(s):
    return sum(((s[i][0] - s[i - 1][0]) ** 2 + (s[i][1] - s[i - 1][1]) ** 2) ** .5 for i in range(1, len(s)))


def word_svg(text, wi):
    scale = FS / upm
    x, t = 0, 0.0
    clips, groups = [], []
    for li, ch in enumerate(text):
        g = glyphset[cmap[ord(ch)]]
        pen = SVGPathPen(glyphset)
        g.draw(pen)
        d = pen.getCommands()
        if d:
            tr = f'translate({x * scale:.1f},{FS}) scale({scale:.5f},{-scale:.5f})'
            cid = f'hwclip{wi}-{li}'
            clips.append(f'<clipPath id="{cid}"><path d="{d}"/></clipPath>')
            segs, ink = skeleton_strokes(ch)
            sw = ink * 1.8  # clip이 삐져나온 붓자국을 잘라줌
            paths = []
            for s in order_segs(segs):
                dur = max(seg_len(s) / SPEED, 0.03)
                pd = 'M' + ' L'.join(f'{px:.0f} {py:.0f}' for px, py in s)
                paths.append(f'<path class="hw" d="{pd}" pathLength="100" '
                             f'style="stroke-width:{sw:.0f};animation-duration:{dur:.2f}s;animation-delay:{t:.2f}s"/>')
                t += dur
            t += GAP
            groups.append(f'<g clip-path="url(#{cid})" transform="{tr}">{"".join(paths)}</g>')
        x += g.width
    w, h = x * scale, FS * 1.35
    return (f'<svg class="hw-svg" viewBox="0 0 {w:.0f} {h:.0f}" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
            f'<defs>{"".join(clips)}</defs>{"".join(groups)}</svg>'), t


entries = []
for wi, name in enumerate(NAMES):
    svg, dur = word_svg(name, wi)
    entries.append(f"  '{name}': `{svg}`,  // {dur:.1f}s")

print('/* 카드 handwriting SVG — Kyobo 폰트 글자 clipPath + 스켈레톤 획 붓 reveal.')
print('   scripts/gen_handwriting_svg.py 자동 생성 (7/2) — 이름 바뀌면 재실행. */')
print('const HANDWRITING_SVGS = {')
print('\n'.join(entries))
print('};')
