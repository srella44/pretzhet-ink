import math, base64


VW, VH = 468, 170   # diagram viewBox (matches card box aspect)
NAVY = '#14213d'; CORAL = '#f0533f'; YEL = '#f7c51e'; BLU = '#2f5bd6'; RED = '#e2453c'
RUN = '#9fdcff'; COND = '#ffb21e'

class D:
    def __init__(self, W, H, xmin=0, xmax=None, ymin=0, ymax=None, pad=10):
        self.W, self.H = W, H
        xmax = W if xmax is None else xmax
        ymax = H if ymax is None else ymax
        ew, eh = xmax - xmin, ymax - ymin
        self.s = min((VW - 2*pad - 60) / ew, (VH - 2*pad - 4) / eh)
        self.ox = (VW - ew*self.s)/2 - xmin*self.s
        self.oy = (VH - eh*self.s)/2 - ymin*self.s + 2
        self.out = []; self.top = []
        self.obst = []; self.lbox = []; self.nums = []   # para colocar los números sin tapar nada
    def p(self, x, y): return (self.ox + x*self.s, self.oy + y*self.s)
    def add(self, s): self.out.append(s)

    # ---------- field elements
    def field(self, dashed=False):
        x0, y0 = self.p(0, 0); x1, y1 = self.p(self.W, self.H)
        self.add(f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{x1-x0:.1f}" height="{y1-y0:.1f}" fill="rgba(255,255,255,.06)" stroke="#fff" stroke-width="2" {"stroke-dasharray=\"6 5\"" if dashed else ""}/>')
    def cone(self, x, y, r=3.6):
        X, Y = self.p(x, y)
        self.add(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="{r}" fill="#ff8a1f" stroke="#fff" stroke-width="1.4"/>')
    def disc(self, x, y):
        X, Y = self.p(x, y)
        self.add(f'<ellipse cx="{X:.1f}" cy="{Y:.1f}" rx="5" ry="3.2" fill="#ffd23c" stroke="#9a6a00" stroke-width="1"/>')
    def line(self, a, b, dash='4 4', w=1.4, op=.7):
        A = self.p(*a); B = self.p(*b)
        self.add(f'<line x1="{A[0]:.1f}" y1="{A[1]:.1f}" x2="{B[0]:.1f}" y2="{B[1]:.1f}" stroke="rgba(255,255,255,{op})" stroke-width="{w}" stroke-dasharray="{dash}"/>')
    def zone(self, pts, label=None, lx=0, ly=0):
        P = ' '.join(f'{self.p(*q)[0]:.1f},{self.p(*q)[1]:.1f}' for q in pts)
        self.add(f'<polygon points="{P}" fill="url(#hatch)" stroke="rgba(255,255,255,.75)" stroke-width="1.2" stroke-dasharray="3 3"/>')
        if label: self.label(lx, ly, label)
    def circlezone(self, x, y, r, label=None):
        X, Y = self.p(x, y)
        self.add(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="{r*self.s:.1f}" fill="url(#hatch)" stroke="rgba(255,255,255,.8)" stroke-width="1.2" stroke-dasharray="3 3"/>')
        if label: self.label(x, y - r - .55, label)
    def label(self, x, y, t, anchor='middle'):
        X, Y = self.p(x, y)
        self.top.append(f'<text x="{X:.1f}" y="{Y:.1f}" text-anchor="{anchor}" font-family="Inter" font-weight="800" font-size="8" letter-spacing=".6" fill="#fff" paint-order="stroke" stroke="rgba(10,40,25,.55)" stroke-width="2.4">{t}</text>')
    def minigoal(self, x, y, side):
        # side: 'L' opening to right, 'R' opening to left
        X, Y = self.p(x, y); h = 2.4*self.s; d = 9
        x0 = X - d if side == 'L' else X
        self.add(f'<rect x="{x0:.1f}" y="{Y-h/2:.1f}" width="{d}" height="{h:.1f}" fill="url(#net)" stroke="#fff" stroke-width="2"/>')

    # ---------- players / ball
    def player(self, x, y, face, color, ghost=False):
        X, Y = self.p(x, y)
        dark = {YEL: '#3a2a00', BLU: '#0b1b4a', RED: '#4a0d0a'}[color]
        op = ' opacity=".42"' if ghost else ''
        self.top.append(
            f'<g transform="translate({X:.1f},{Y:.1f}) rotate({face+90})"{op}>'
            f'<ellipse cx="0" cy="0" rx="12" ry="7" fill="{color}" stroke="{dark}" stroke-width="1.8"/>'
            f'<circle cx="-11" cy="-1.5" r="2.6" fill="#e9b88c" stroke="{dark}" stroke-width="1"/>'
            f'<circle cx="11" cy="-1.5" r="2.6" fill="#e9b88c" stroke="{dark}" stroke-width="1"/>'
            f'<circle cx="0" cy="0.5" r="5" fill="#e9b88c" stroke="{dark}" stroke-width="1.2"/>'
            f'<path d="M-5 0.5 A5 5 0 0 0 5 0.5 Z" fill="#2b1a0e"/>'
            f'</g>')
    def ball(self, x, y, face=None, off=1.0):
        X, Y = self.p(x, y)
        if face is not None:
            a = math.radians(face); X += math.cos(a)*14; Y += math.sin(a)*14
        self.top.append(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="4.2" fill="#fff" stroke="{NAVY}" stroke-width="1.6"/><circle cx="{X:.1f}" cy="{Y:.1f}" r="1.4" fill="{NAVY}"/>')

    # ---------- arrows
    def _ends(self, a, b, s0, s1):
        A = self.p(*a); B = self.p(*b)
        dx, dy = B[0]-A[0], B[1]-A[1]; L = math.hypot(dx, dy); ux, uy = dx/L, dy/L
        return (A[0]+ux*s0, A[1]+uy*s0), (B[0]-ux*s1, B[1]-uy*s1), (ux, uy), L
    def _place_num(self, A, B, ux, uy, nt, nside):
        """Elige la posición del número que menos tapa a jugadores, etiquetas u otros números."""
        best = None
        cands = [(nt, nside, 11)]
        for t in (.5, .4, .6, .33, .67, .25, .75, .15, .85):
            for sd in (nside, -nside):
                for off in (11, 17):
                    cands.append((t, sd, off))
        for k, (t, sd, off) in enumerate(cands):
            mx = A[0] + (B[0]-A[0])*t + (-uy)*off*sd
            my = A[1] + (B[1]-A[1])*t + (ux)*off*sd
            cost = k * 0.01
            if not (10 < mx < VW - 10 and 10 < my < VH - 10): cost += 50
            for (ox, oy, r) in self.obst:
                d = math.hypot(mx - ox, my - oy)
                if d < r + 8: cost += (r + 8 - d) * 3
            for (ox, oy) in self.nums:
                d = math.hypot(mx - ox, my - oy)
                if d < 17: cost += (17 - d) * 3
            for (lx, ly, hw, hh) in self.lbox:
                dx = max(abs(mx - lx) - hw, 0); dy = max(abs(my - ly) - hh, 0)
                d = math.hypot(dx, dy)
                if d < 9: cost += (9 - d) * 3
            if best is None or cost < best[0]: best = (cost, mx, my)
            if cost < 0.2 and k == 0: break
        return best[1], best[2]

    def arrow(self, a, b, kind='pass', n=None, s0=15, s1=15, nside=1, nt=.5):
        A, B, (ux, uy), L = self._ends(a, b, s0, s1)
        if kind == 'pass':
            self.add(f'<line x1="{A[0]:.1f}" y1="{A[1]:.1f}" x2="{B[0]:.1f}" y2="{B[1]:.1f}" stroke="#fff" stroke-width="2.4" marker-end="url(#ahW)"/>')
        elif kind == 'run':
            self.add(f'<line x1="{A[0]:.1f}" y1="{A[1]:.1f}" x2="{B[0]:.1f}" y2="{B[1]:.1f}" stroke="{RUN}" stroke-width="2.2" stroke-dasharray="5 4" marker-end="url(#ahB)"/>')
        elif kind == 'cond':
            Lr = math.hypot(B[0]-A[0], B[1]-A[1]) - 8; px, py = -uy, ux
            pts = []; steps = int(Lr/1.5)
            for i in range(steps+1):
                t = i*1.5; w = 3.2*math.sin(t/4.2)
                pts.append(f'{A[0]+ux*t+px*w:.1f},{A[1]+uy*t+py*w:.1f}')
            pts.append(f'{B[0]:.1f},{B[1]:.1f}')
            self.add(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{COND}" stroke-width="2.4" stroke-linejoin="round" marker-end="url(#ahO)"/>')
        if n is not None:
            mx, my = self._place_num(A, B, ux, uy, nt, nside)
            self.nums.append((mx, my))
            self.top.append(f'<g><circle cx="{mx:.1f}" cy="{my:.1f}" r="7.2" fill="{NAVY}" stroke="#fff" stroke-width="1.5"/><text x="{mx:.1f}" y="{my+3.4:.1f}" text-anchor="middle" font-family="Inter" font-weight="800" font-size="9.5" fill="#fff">{n}</text></g>')

    def svg(self, size_tag, code):
        # scale bar 2 m
        L = 2*self.s; x1 = VW - 12; x0 = x1 - L; y = VH - 10
        bar = (f'<text x="{x0-4:.1f}" y="{y+3.4:.1f}" text-anchor="end" font-family="Inter" font-weight="800" font-size="8.5" fill="#fff">2 m</text>'
               f'<path d="M{x0:.1f} {y-3:.1f} V{y+3:.1f} M{x0:.1f} {y:.1f} H{x1:.1f} M{x1:.1f} {y-3:.1f} V{y+3:.1f}" stroke="#fff" stroke-width="1.6"/>')
        tw = 9 + 5.6*len(size_tag)
        tag = (f'<rect x="7" y="7" width="{tw:.0f}" height="15" rx="7.5" fill="rgba(10,20,35,.72)" stroke="rgba(255,255,255,.45)"/>'
               f'<text x="{7+tw/2:.1f}" y="17.8" text-anchor="middle" font-family="Inter" font-weight="800" font-size="8.6" fill="#fff">{size_tag}</text>')
        stripes = ''.join(f'<rect x="{i*VW/12:.1f}" y="0" width="{VW/24:.1f}" height="{VH}" fill="rgba(255,255,255,.035)"/>' for i in range(12))
        defs = f'''<defs>
<radialGradient id="g" cx="50%" cy="50%" r="70%"><stop offset="0" stop-color="#3f8a5c"/><stop offset="1" stop-color="#245c3b"/></radialGradient>
<pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="6" height="6" fill="rgba(255,255,255,.10)"/><line x1="0" y1="0" x2="0" y2="6" stroke="rgba(255,255,255,.30)" stroke-width="1.6"/></pattern>
<pattern id="net" width="3" height="3" patternUnits="userSpaceOnUse"><rect width="3" height="3" fill="rgba(255,255,255,.15)"/><path d="M0 0H3M0 0V3" stroke="rgba(255,255,255,.6)" stroke-width=".5"/></pattern>
<marker id="ahW" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="4.4" markerHeight="4.4" orient="auto"><path d="M0 0L10 5L0 10z" fill="#fff"/></marker>
<marker id="ahB" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="4.6" markerHeight="4.6" orient="auto"><path d="M0 0L10 5L0 10z" fill="{RUN}"/></marker>
<marker id="ahO" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="4.4" markerHeight="4.4" orient="auto"><path d="M0 0L10 5L0 10z" fill="{COND}"/></marker>
</defs>'''
        return (f'<svg viewBox="0 0 {VW} {VH}" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice">{defs}'
                f'<rect width="{VW}" height="{VH}" fill="url(#g)"/>{stripes}' + ''.join(self.out) + ''.join(self.top) + tag + bar + '</svg>')

def ang(a, b): return math.degrees(math.atan2(b[1]-a[1], b[0]-a[0]))

