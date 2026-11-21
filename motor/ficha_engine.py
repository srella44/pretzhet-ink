"""Prètzhèt Ink · motor de fichas: un JSON por ejercicio -> SVG del diagrama, tarjeta web y página de libro."""
import json, math, re, sys, glob, base64, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'motor'))
import diagram_core as dc
from diagram_core import D, ang, YEL, BLU, RED, NAVY, CORAL, RUN, COND

WHITE = '#f4f4f4'
ROLE = {'A': YEL, 'D': BLU, 'B': RED, 'C': WHITE}
_orig_player = D.player
def _player(self, x, y, face, color, ghost=False):
    X, Y = self.p(x, y)
    dark = {YEL: '#3a2a00', BLU: '#0b1b4a', RED: '#4a0d0a', WHITE: '#333333'}[color]
    op = ' opacity=".42"' if ghost else ''
    self.top.append(f'<g transform="translate({X:.1f},{Y:.1f}) rotate({face+90})"{op}>'
        f'<ellipse cx="0" cy="0" rx="12" ry="7" fill="{color}" stroke="{dark}" stroke-width="1.8"/>'
        f'<circle cx="-11" cy="-1.5" r="2.6" fill="#e9b88c" stroke="{dark}" stroke-width="1"/>'
        f'<circle cx="11" cy="-1.5" r="2.6" fill="#e9b88c" stroke="{dark}" stroke-width="1"/>'
        f'<circle cx="0" cy="0.5" r="5" fill="#e9b88c" stroke="{dark}" stroke-width="1.2"/>'
        f'<path d="M-5 0.5 A5 5 0 0 0 5 0.5 Z" fill="#2b1a0e"/></g>')
D.player = _player

def _hands(self, a, b):
    A = self.p(*a); B = self.p(*b)
    self.top.append(f'<line x1="{A[0]:.1f}" y1="{A[1]:.1f}" x2="{B[0]:.1f}" y2="{B[1]:.1f}" stroke="{NAVY}" stroke-width="3.2" stroke-linecap="round" opacity=".85"/>')
D.hands = _hands

def _light(self, x, y):
    X, Y = self.p(x, y)
    self.top.append(f'<g transform="translate({X:.1f},{Y:.1f})"><rect x="-7" y="-18" width="14" height="36" rx="4" fill="{NAVY}" stroke="#fff" stroke-width="1.2"/>'
                    f'<circle cy="-10" r="4" fill="#2ecc71"/><circle cy="0" r="4" fill="#f5c518"/><circle cy="10" r="4" fill="#e2453c"/></g>')
D.light = _light

def _goal(d, x, y, side, width, keeper):
    """Portería en el borde del campo. side: T (arriba), B (abajo), L, R. width en metros."""
    X, Y = d.p(x, y); w = width * d.s; depth = 8
    if side in ('T', 'B'):
        y0 = Y - depth if side == 'T' else Y
        d.add(f'<rect x="{X-w/2:.1f}" y="{y0:.1f}" width="{w:.1f}" height="{depth}" fill="url(#net)" stroke="#fff" stroke-width="2.2"/>')
        kx, ky, kf = x, y + (0.9 if side == 'T' else -0.9), 90 if side == 'T' else -90
    else:
        x0 = X - depth if side == 'L' else X
        d.add(f'<rect x="{x0:.1f}" y="{Y-w/2:.1f}" width="{depth}" height="{w:.1f}" fill="url(#net)" stroke="#fff" stroke-width="2.2"/>')
        kx, ky, kf = x + (0.9 if side == 'L' else -0.9), y, 0 if side == 'L' else 180
    if keeper:
        KX, KY = d.p(kx, ky)
        d.top.append(f'<g transform="translate({KX:.1f},{KY:.1f}) rotate({kf+90})"><ellipse rx="12" ry="7" fill="#2ecc71" stroke="#0b3d20" stroke-width="1.8"/>'
                     f'<circle cy=".5" r="5" fill="#e9b88c" stroke="#0b3d20" stroke-width="1.2"/><path d="M-5 .5A5 5 0 0 0 5 .5Z" fill="#2b1a0e"/></g>')

def render_svg(spec):
    f = spec['field']
    ext = spec.get('extent', {})
    d = D(f[0], f[1], xmin=ext.get('xmin', 0), xmax=ext.get('xmax'), ymin=ext.get('ymin', 0), ymax=ext.get('ymax'))
    if not spec.get('nofield'): d.field(dashed=spec.get('dashed', False))
    for z in spec.get('zones', []):
        if z['t'] == 'poly': d.zone([tuple(p) for p in z['pts']])
        elif z['t'] == 'circle': d.circlezone(z['x'], z['y'], z['r'])
        elif z['t'] == 'rect':
            x0, y0, x1, y1 = z['r']; d.zone([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])
    for l in spec.get('lines', []):
        d.line(tuple(l[0]), tuple(l[1]), dash=l[2] if len(l) > 2 else '6 5', w=1.6, op=.85)
    for c in spec.get('cones', []): d.cone(*c)
    for c in spec.get('discs', []): d.disc(*c)
    for g in spec.get('goals', []): d.minigoal(g[0], g[1], g[2])
    for g in spec.get('porterias', []):
        _goal(d, g['x'], g['y'], g.get('lado', 'T'), g.get('ancho', 5), g.get('portero', False))
    for a in spec.get('arrows', []):
        d.arrow(tuple(a['a']), tuple(a['b']), a.get('k', 'pass'), n=a.get('n'), s0=a.get('s0', 15), s1=a.get('s1', 15),
                nside=a.get('side', 1), nt=a.get('nt', .5))
    for h in spec.get('hands', []): d.hands(tuple(h[0]), tuple(h[1]))
    for p in spec.get('players', []):
        face = p['f'] if isinstance(p.get('f'), (int, float)) else ang((p['x'], p['y']), tuple(p['f']))
        d.player(p['x'], p['y'], face, ROLE[p['r']], ghost=p.get('ghost', False))
        if p.get('ball'):
            d.ball(p['x'], p['y'], face)
    for b in spec.get('balls', []): d.ball(*b)
    for l in spec.get('lights', []): d.light(*l)
    for t in spec.get('labels', []): d.label(t[0], t[1], t[2], t[3] if len(t) > 3 else 'middle')
    return d.svg(spec.get('tag', f'{f[0]} × {f[1]} m'), '')

# ---------------- page and card templates
BLOCKS = {b[0]: b[1] for b in [
 ('Calentamiento', 'F28C28'), ('Técnica y duelos', '1BA6A6'), ('Rondos', 'F5C518'), ('Posesiones y juego de posición', '3B82F6'),
 ('Superioridades', '7C4DCC'), ('Oleadas y transiciones', 'E2453C'), ('Finalización', 'D6336C'), ('Defensa y presión', '4B5563'),
 ('Partidos y situaciones reales', '2E9E5B'), ('Balón parado', 'B7791F'), ('Porteros', '1F2937'), ('Vuelta a la calma', '7CC4F0')]}
def ink(hexc):  # text colour on block colour
    r, g, b = int(hexc[:2], 16), int(hexc[2:4], 16), int(hexc[4:], 16)
    return NAVY if (0.299*r + 0.587*g + 0.114*b) > 150 else '#ffffff'

ICO_CLOCK = '<svg viewBox="0 0 16 16"><circle cx="8" cy="8" r="6.2" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M8 4.6V8l2.4 1.6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>'
ICO_USER = '<svg viewBox="0 0 16 16"><circle cx="8" cy="5" r="3" fill="currentColor"/><path d="M2.5 14.5c.6-3.2 2.8-5 5.5-5s4.9 1.8 5.5 5z" fill="currentColor"/></svg>'
ICO_AREA = '<svg viewBox="0 0 16 16"><path d="M2 5V2h3M11 2h3v3M14 11v3h-3M5 14H2v-3" fill="none" stroke="currentColor" stroke-width="1.9"/><rect x="6" y="6" width="4" height="4" fill="currentColor"/></svg>'
LVL = {'Fácil': 1, 'Normal': 2, 'Medio': 3, 'Alto': 4}

def strip(e):
    pips = ''.join(f'<i class="{"on" if i < LVL.get(e["nivel"], 2) else ""}"></i>' for i in range(4))
    return (f'<div class="strip"><span>{ICO_CLOCK}{e["edad"]}</span><span><b class="pips">{pips}</b>{e["nivel"]}</span>'
            f'<span>{ICO_USER}{e["jugadores"]}</span><span>{ICO_AREA}{e["espacio"]}</span></div>')

def book_card(e, n):
    return f'''<article class="card">
<header><span class="num">{n:02d}</span><h2>{e["titulo"]}</h2><span class="fmt">{e["formato"]}</span>{'<span class="topb">TOP</span>' if e.get("top") else ""}</header>
<div class="dia">{render_svg(e["diagrama"])}<span class="code">{e["id"]}</span></div>
{strip(e)}
<div class="txt">
<p><b class="k">Montaje</b>{e["montaje"]}</p>
<p><b class="k">Juego</b>{e["juego"]}</p>
<p class="pt"><b class="k">Punto</b><mark>{e["punto"]}</mark></p>
<p class="cons"><span class="chip">CONSIGNA</span><em>«{e["consigna"]}»</em></p>
</div></article>'''

def web_card(e):
    v = e.get('variantes', {})
    return f'''<article class="wcard">
<header><span class="num">{e["bloque"]}</span><h2>{e["titulo"]}</h2><span class="fmt">{e["formato"]}</span>{'<span class="topb">TOP</span>' if e.get("top") else ""}</header>
<div class="dia">{render_svg(e["diagrama"])}<span class="code">{e["id"]}</span></div>
{strip(e)}
<div class="wtxt">
<p class="obj">{e.get("objetivo", "")}</p>
<h3>Montaje</h3><p>{e["montaje"]}</p>
<h3>Juego</h3><p>{e["juego"]}</p>
<h3>Punto</h3><p class="pt"><mark>{e["punto"]}</mark></p>
<p class="cons"><span class="chip">CONSIGNA</span><em>«{e["consigna"]}»</em></p>
<div class="vars"><div><h3>Más fácil</h3><p>{v.get("facil", "—")}</p></div><div><h3>Más difícil</h3><p>{v.get("dificil", "—")}</p></div></div>
<p class="meta"><b>Duración:</b> {e.get("duracion", "—")} · <b>Series:</b> {e.get("series", "—")}</p>
<p class="meta"><b>Por edades:</b> {e.get("adaptacion", "—")}</p>
<p class="src">Fuente: {e["fuente"]["autor"]} · {e["fuente"]["titulo_original"]} · {e["fuente"]["ref"]}</p>
</div></article>'''

LEG = '''<footer class="legend">
<span><i class="lp a"></i>Atacante</span><span><i class="lp b"></i>2.º equipo</span><span><i class="lp d"></i>Defensor</span><span><i class="lp c"></i>Comodín</span>
<span><svg viewBox="0 0 12 12" class="li"><circle cx="6" cy="6" r="4.4" fill="#fff" stroke="#14213d" stroke-width="1.6"/><circle cx="6" cy="6" r="1.4" fill="#14213d"/></svg>Balón</span>
<span><svg viewBox="0 0 12 12" class="li"><circle cx="6" cy="6" r="4" fill="#ff8a1f" stroke="#fff" stroke-width="1.4"/></svg>Cono</span>
<span><svg viewBox="0 0 30 10" class="la"><line x1="1" y1="5" x2="22" y2="5" stroke="#fff" stroke-width="2.4"/><path d="M21 1l8 4-8 4z" fill="#fff"/></svg>Pase</span>
<span><svg viewBox="0 0 30 10" class="la"><line x1="1" y1="5" x2="22" y2="5" stroke="#9fdcff" stroke-width="2.2" stroke-dasharray="4 3"/><path d="M21 1l8 4-8 4z" fill="#9fdcff"/></svg>Desplazamiento</span>
<span><svg viewBox="0 0 30 10" class="la"><path d="M1 5q2.5-4 5 0t5 0 5 0 5 0" fill="none" stroke="#ffb21e" stroke-width="2.2"/><path d="M21 1l8 4-8 4z" fill="#ffb21e"/></svg>Conducción</span>
<span><svg viewBox="0 0 14 14" class="li"><rect x="1" y="1" width="12" height="12" fill="none" stroke="#fff" stroke-dasharray="2 2"/></svg>Zona</span>
<span><svg viewBox="0 0 16 16" class="li"><circle cx="8" cy="8" r="6.6" fill="#14213d" stroke="#fff" stroke-width="1.4"/><text x="8" y="11.3" text-anchor="middle" font-family="Inter" font-weight="800" font-size="9" fill="#fff">1</text></svg>Orden</span>
</footer>'''

def css(bc):
    t = ink(bc)
    base = open(os.path.join(ROOT, 'motor', 'page_base.css')).read()
    return base.replace('BC', '#' + bc).replace('BT', t)

def book_page(exs, block, kicker_b, kicker, page_no, start_n=1):
    bc = BLOCKS[block]
    logo = base64.b64encode(open(os.path.join(ROOT, 'motor', 'logo.png'), 'rb').read()).decode()
    cards = ''.join(book_card(e, start_n + i) for i, e in enumerate(exs))
    return f'''<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><style>{css(bc)}</style></head><body>
<div class="top"><div class="pitch"></div><div class="logo"><img src="data:image/png;base64,{logo}"></div><h1>{block.upper()}</h1>
<div class="kick"><b>{kicker_b}</b>{kicker}</div></div><div class="dash"></div>
<main class="grid">{cards}</main>{LEG}
<div class="foot"><span>PRÈTZHÈT INK · BANCO PERSONAL DE EJERCICIOS</span><span class="pg">{page_no:03d}</span></div></body></html>'''

def web_page(e):
    bc = BLOCKS[e['bloque']]
    return f'''<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><style>{css(bc)}{open(os.path.join(ROOT, 'motor', 'web.css')).read()}</style></head>
<body class="web">{web_card(e)}</body></html>'''
