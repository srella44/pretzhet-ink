"""Prètzhèt Ink · app completa (un solo HTML) a partir de datos/*.json y ejercicios/*.json.
Uso: python3 motor/build_app.py  ->  salida/app/Pretzhet_Ink_app.html"""
import json, re, glob, sys, os, unicodedata
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'motor'))
from ficha_engine import render_svg, BLOCKS, ink
def norm(s):
    s = unicodedata.normalize('NFKD', str(s or '').lower())
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'\s+', ' ', re.sub(r'[^a-z0-9: ]', ' ', s)).strip()


D = os.path.join(ROOT, 'datos')
refs = json.load(open(os.path.join(D, 'referencias.json')))
fichas = json.load(open(os.path.join(D, 'fichas_propias.json')))
sel = json.load(open(os.path.join(D, 'seleccion.json')))
TOP = {r['ID']: r['top'] for r in refs if r.get('top')}
TOP.update({f['Código']: f['top'] for f in fichas if f.get('top')})
in_book = {p['id']: p['rank'] for p in sel}
score = {p['id']: p['score'] for p in sel}
drawn = {}
for f in glob.glob(os.path.join(ROOT, 'ejercicios', '*.json')):
    e = json.load(open(f)); drawn[e['id']] = e
BL = list(BLOCKS)

CATS = [('Prebenjamín', 6, 7), ('Benjamín', 8, 9), ('Alevín', 10, 11), ('Infantil', 12, 13), ('Cadete', 14, 15), ('Juvenil', 16, 18)]
def ages(s):
    if not s: return None
    t = norm(s); lo, hi = [], []
    for name, a, b in CATS:
        if norm(name) in t: lo.append(a); hi.append(b)
    if norm('Prebenjamín') in t and norm('Benjamín') not in t.replace(norm('Prebenjamín'), ''):
        pass
    for u in re.findall(r'\bu ?(\d{1,2})\b', t):
        k = int(u); lo.append(k - 1); hi.append(k)
    m = re.findall(r'(\d{1,2}) ?(?:a|-|–)? ?(\d{1,2}) anos', t)
    for a, b in m: lo.append(int(a)); hi.append(int(b))
    m = re.search(r'(\d{1,2}) ?\+', t)
    if m and not lo: lo.append(int(m.group(1))); hi.append(18)
    if 'junior' in t or 'senior' in t: return None
    return [min(lo), max(hi)] if lo else None

def players(r_jug, title):
    s = re.sub(r'\+ ?\d+ ?PT|\+ ?PT', '', str(r_jug or ''))
    m = re.search(r'(\d+) equipos(?: de (\d+)(?:[–-](\d+))?)?', s)
    if m:
        if m.group(2): k = int(m.group(1)); return [k * int(m.group(2)), k * int(m.group(3) or m.group(2))]
        return None
    if s.startswith('Parejas'): return [2, 2]
    if s.startswith('Tríos'): return [3, 3]
    if s.startswith(('Todo el grupo', 'Grupos de')): return None
    nums = [int(x) for x in re.findall(r'\b(\d{1,2})\b', s) if 1 < int(x) <= 30]
    if 'entrada' in s: nums = []
    if nums: return [min(nums), max(nums)]
    t = norm(title)
    m = re.search(r'\b(\d{1,2}) ?(?:v|vs|x|:|contra) ?(\d{1,2})(?: ?\+ ?(\d))?', t)
    if m:
        n = int(m.group(1)) + int(m.group(2)) + int(m.group(3) or 0)
        if 1 < n <= 30: return [n, n]
    return None

def fmt_of(title):
    t = norm(str(title or '').replace('+', ' + ').replace('+', '#')).replace('#', '+') if False else re.sub(r'[^a-z0-9:+ ]', ' ', ''.join(c for c in unicodedata.normalize('NFKD', str(title or '').lower()) if not unicodedata.combining(c)))
    m = re.search(r'\b(\d{1,2}) ?(?:\+ ?(\d) ?)?(?:v|vs|x|:|contra) ?(\d{1,2})(?: ?\+ ?(\d))?', t)
    if not m: return ''
    a = m.group(1) + (f'+{m.group(2)}' if m.group(2) else ''); b = m.group(3) + (f'+{m.group(4)}' if m.group(4) else '')
    return f'{a}v{b}'

LABELS = ['Objetivo', 'Montaje', 'Evitar', 'Cómo se juega', 'Reglas', 'Puntuación', 'Puntos', 'Consignas', 'Variantes', 'Más fácil', 'Más difícil', 'Espacio', 'Duración', 'Contexto', 'Frase']
def sections(text):
    t = re.sub(r'\bPuntuación (?=[A-ZÁÉÍÓÚ0-9])', 'Puntuación: ', text or '')
    pat = re.compile(r'(' + '|'.join(re.escape(l) for l in LABELS) + r'):', re.I)
    parts = pat.split(t)
    out = {'_': parts[0].strip(' ·.')}
    for i in range(1, len(parts) - 1, 2):
        k = parts[i].capitalize(); out[k] = (out.get(k, '') + ' ' + parts[i+1].strip(' ·')).strip()
    return out

def short_src(a):
    a = a or ''
    if a.startswith('toplidercoach'): return 'toplidercoach (Entrenadores Top)'
    if a.startswith(('Reel de Instagram', 'Academia (', 'Entrenamiento de un equipo')): return 'Redes y webs'
    for k in ['Tareas Fútbol Base', 'RONDO', 'Level Up Coach', 'FCStage', 'Leicester', 'Athletic', 'AFOPRO', 'Alex Ortiz', 'Javier López', 'FIFA']:
        if k in a: return {'FCStage': 'FCStage Camps', 'Leicester': 'Leicester City Academy', 'Athletic': 'Athletic Club', 'Javier López': 'Javier López (1.380 juegos)'}.get(k, k)
    return 'Redes y webs' if a.startswith('@') or a in ('SoccerXpert', 'Bcoach', 'SoccerDrive') else (a or 'Otras')

CLUB = {'Ajax Amsterdam':'Ajax','Alaves':'Alavés','Argentina National Team':'Argentina','As Monaco':'AS Mónaco','Atletico Madrid':'Atlético de Madrid','Atletico Osasuna':'Osasuna','Bayern Munich':'Bayern Múnich','Belgium National Team':'Bélgica','Brasil National Team':'Brasil','Cadiz':'Cádiz','Celta De Vigo':'Celta de Vigo','Chile National Team':'Chile','Colombia National Team':'Colombia','Elche Cf':'Elche','England National Team':'Inglaterra','Fc Barcelona':'FC Barcelona','France National Team':'Francia','Germany National Team':'Alemania','Inter Milan':'Inter de Milán','Italy National Team':'Italia','Kovenhaun':'Copenhague','Leipzig':'RB Leipzig','Milan':'AC Milan','Napoles':'Nápoles','Olimpiakos':'Olympiacos','Olimpic Marsella':'Olympique de Marsella','Paises Bajos National Team':'Países Bajos','Portugal National Team':'Portugal','Psg':'PSG','Psv':'PSV','Roma':'AS Roma','Sevilla Fc':'Sevilla','Spain National Team':'España','Spartak Praga':'Sparta Praga','Sporting Cp':'Sporting CP','Uruguay National Team':'Uruguay','Valencia Cf':'Valencia','Venezuela National Team':'Venezuela','Wolverhamptom':'Wolverhampton','Athletic Bilbao':'Athletic Club','Glasgow Rangers':'Rangers'}
STOP = set('RONDO RONDOS RUEDA RUEDAS DUELO DUELOS JUEGO POSESION POSESIÓN ATAQUE DEFENSA FINALIZACION FINALIZACIÓN TRANSICION TRANSICIÓN TRANSICIONES PRESION PRESIÓN TECNICA TÉCNICA TACTICO TÁCTICO SALIDA PASES PASE SESION SESIÓN CONTRA CIRCUITO PARTIDO CONTROL REMATE MOVILIDAD AMPLITUD CAMBIO VELOCIDAD TRABAJO COBERTURA CRUCE BALON BALÓN ESTRATEGIA DOS TRES LA EL LOS LAS UN UNA 1X1 CENTROS CENTRO LINEA LÍNEA BLOQUE ORGANIZACION ORGANIZACIÓN PRIMER PRIMERA COMPETICIÓN COMPETICION FÍSICO FISICO TÉCNICO TECNICO CONDUCCIÓN CONDUCCION REPLIEGUE Y CON EN PARA TÁCTICA TACTICA PROGRESIÓN PROGRESION ENTRENAMIENTO EJERCICIO SUPERIORIDAD SUPERIORIDADES LLEGADA FASE OLEADAS REMATES TIROS ACCIONES INTERCAMBIO DEL AL POR SIN'.split())
def _cand(t):
    t = (t or '').upper().strip()
    m = re.match(r"^([A-ZÁÉÍÓÚÑÜ\.' ]{3,30}?)\s*,", t)
    if m and not re.search(r'\d', m.group(1)): return m.group(1).strip(), True
    out = []
    stopped = False
    for w in t.split():
        if w in STOP or re.search(r'\d', w): stopped = True; break
        out.append(w)
        if len(out) == 3: break
    while out and out[-1] in ('DE', 'DEL'): out.pop()
    return (' '.join(out), stopped) if out else ('', False)
def _key(n): return norm(n).replace(' ', '')
def build_coaches(titles):
    # cuenta candidatos; los que cortó una palabra de parada valen ya con 1 aparición

    cnt = {}
    for t in titles:
        c, _ = _cand(t)
        if c: cnt[_key(c)] = cnt.get(_key(c), 0) + 1
    return cnt

TLC_TITLES = [(drawn[r['ID']]['fuente']['titulo_original'] if r['ID'] in drawn else r['Título / referencia']) for r in refs if r['ID'].startswith('TLC-')]
COACH_CNT = build_coaches(TLC_TITLES)
ACC = {}
for _t in TLC_TITLES:
    _c, _ = _cand(_t)
    if _c and (_key(_c) not in ACC or (not _c.isascii() and ACC[_key(_c)].isascii())): ACC[_key(_c)] = _c
COACH_FIX = {'Kompani':'Kompany','Kovac':'Niko Kovac','Nico Kovac':'Niko Kovac','Michel':'Michel Sánchez','Pochetino':'Pochettino','Alguacil':'Imanol Alguacil','Simone Inzaghi':'Inzaghi','Unai Emery':'Emery','Lionel Scaloni':'Scaloni','Ruben Amorín':'Rúben Amorim','Eddi Howe':'Eddie Howe','Kloop':'Klopp','Ten Hag':'Erik ten Hag','Adi Hutter':'Adi Hütter','Addi Hutter':'Adi Hütter','Giraldez':'Claudio Giraldez','Cristian Chivu':'Chivu','Steven Gerrard':'Gerrard','Dorival Júnior':'Dorival Jr.','Roberto Mártinez':'Roberto Martínez','Dino Toppmoller':'Dino Toppmöller','Alvaro Cervera':'Álvaro Cervera','Sergio Conceiçao':'Sérgio Conceição','Frank Lampard':'Lampard','Joachim Low':'Joachim Löw','Rafa Marquez':'Rafa Márquez','Luis':'', 'Juegos Reducidos':'', 'Middlesbrough':''}
COACH_TAIL = ('Acción Combinativa','Ataques','Activación','Combinación','Tricolor','Pared','Contraataque','Salida de Balón')
def coach_of(t):
    c = _coach_of(t)
    for tail in COACH_TAIL:
        if c.endswith(' ' + tail): c = c[:-len(tail)-1]
    return COACH_FIX.get(c, c)
def _coach_of(t):
    c, comma = _cand(t)
    if not c: return ''
    if c == 'LUIS DE': c = 'LUIS DE LA FUENTE'
    if not (comma or COACH_CNT.get(_key(c), 0) >= 2): return ''
    c = ACC.get(_key(c), c)
    return ' '.join(('De' if (w == 'DE' and i == 0) else w.lower() if w in ('DE', 'DEL', 'TEN', 'LA') else w.capitalize()) for i, w in enumerate(c.replace('.', '. ').split())).replace('  ', ' ').replace('. ', '.')

recs = []
for r in refs:
    if r['dec'] not in ('Candidato', 'Revisar nivel'): continue
    s = sections(r.get('Mecánica identificada / datos') or '')
    d = drawn.get(r['ID'])
    rec = dict(i=r['ID'], b=BL.index(r['b08']), t=r['Título / referencia'], s=short_src(r['Autor / proveedor']), sl=r['Autor / proveedor'],
               a=ages(r['Edades']), ar=r['Edades'] or '', n=r['Dificultad'] or 'Normal', p=players(r['Jugadores'], r['Título / referencia'] or ''),
               f=fmt_of(r['Título / referencia'] or ''), rv=1 if r['dec'] == 'Revisar nivel' else 0, why=r['why'] if r['dec'] == 'Revisar nivel' else '',
               lb=in_book.get(r['ID'], 0), sc=score.get(r['ID'], 0), ref=r.get('URL o PDF · página') or '',
               x={'obj': s.get('Objetivo', ''), 'mont': s.get('Montaje', ''), 'avoid': s.get('Evitar', ''), 'how': s.get('Cómo se juega', '') or s.get('_', ''), 'rules': s.get('Reglas', ''),
                  'pts': (s.get('Puntuación', '') + ' ' + s.get('Puntos', '')).strip(), 'cues': s.get('Consignas', '') or s.get('Frase', ''),
                  'fac': s.get('Más fácil', ''), 'dif': s.get('Más difícil', ''), 'var': s.get('Variantes', ''), 'sp': s.get('Espacio', '').rstrip('. '),
                  'ctx': s.get('Contexto', ''), 'notes': (r.get('Advertencias / siguiente revisión') or '') if (r['ID'].startswith(('TFB', 'RONDO', 'DOS')) or r.get('completed')) else ''})
    if r['ID'].startswith(('TLC-','FB-')):
        rec['tl'] = 1
        m_ = re.search(r'\(([^()]*)\)\s*$', r['Autor / proveedor'] or '')
        if m_: rec['tm'] = CLUB.get(m_.group(1).strip().title(), m_.group(1).strip().title())
        if r['ID'].startswith('TLC-'):
            co_ = coach_of(d['fuente']['titulo_original'] if d else (r.get('Título original') or r['Título / referencia']))
            if co_: rec['co'] = co_
            if rec.get('tm'): rec['cl'] = rec['tm']
        elif r['ID'].startswith('FB-'): rec['tm'] = 'Fútbol Base'
    _src = r['Autor / proveedor'] or ''
    if 'Leicester' in _src: rec['cl'] = 'Leicester City'
    elif 'Athletic Club' in _src: rec['cl'] = 'Athletic Club'
    if 'Mourinho' in _src: rec['co'] = 'Mourinho'
    if not rec.get('cl'):
        if 'FCStage' in _src: rec['cl'] = 'FCS'
        elif r['ID'].startswith('RONDO-') or _src.strip().upper() == 'RONDO': rec['cl'] = 'Rondo'
        elif 'FIFA' in _src.upper(): rec['cl'] = 'FIFA'
    if r['ID'].startswith('IG-'):
        m2_ = re.search(r'\(([A-Za-zÁÉÍÓÚáéíóúñ][^()]{3,30})\)\s*$', r['Título / referencia'] or '')
        if m2_ and not re.search(r'propuesta|adaptaci|parte|variante', m2_.group(1), re.I): rec['cl'] = m2_.group(1).strip()
    if r.get('probado'): rec['pr'] = 1
    if r.get('_fmt'): rec['f'] = r['_fmt']
    if not rec['f']:
        tl_, p_ = norm(r['Título / referencia'] or ''), rec['p']
        if 'individual' in tl_ or (p_ and p_[0] == p_[1] == 1): rec['f'] = 'individual'
        elif p_ and p_[0] == p_[1] == 2: rec['f'] = 'parejas'
        elif p_ and p_[0] == p_[1] == 3: rec['f'] = 'tríos'
        elif 'circuito' in tl_: rec['f'] = 'circuito'
        elif 'rueda' in tl_: rec['f'] = 'rueda'
        elif 'rondo' in tl_: rec['f'] = 'rondo'
    if r.get('Título original'): rec['ot'] = r['Título original']
    if d:
        rec.update(t=d['titulo'], f=d['formato'], dg=1, x={'obj': d['objetivo'], 'mont': d['montaje'], 'how': d['juego'], 'pts': d['punto'], 'cues': d['consigna'],
                   'fac': d['variantes']['facil'], 'dif': d['variantes']['dificil'], 'dur': d['duracion'], 'ser': d['series'], 'adapt': d['adaptacion'],
                   'sp': d['espacio']}, ot=d['fuente']['titulo_original'])
    recs.append(rec)
for f in fichas:
    rec = dict(i=f['Código'], b=BL.index(f['b08']), t=f['Nombre'], s='Prètzhèt Ink (propias)', sl='Diseño propio Prètzhèt Ink', a=ages(f['Edad']), ar=f['Edad'] or '',
               n=f['Dificultad'] or 'Normal', p=players(f['Participantes total'], f['Nombre']), f=fmt_of(str(f['Jugadores campo'])) or fmt_of(f['Nombre']),
               rv=0, why='', lb=in_book.get(f['Código'], 0), sc=score.get(f['Código'], 0), ref='Banco de 299 fichas propias',
               x={'obj': f.get('Objetivo') or '', 'mont': f.get('Organización') or '', 'how': f.get('Desarrollo') if f.get('Desarrollo') != f.get('Organización') else '',
                  'pts': f.get('Reglas y puntuación') or '', 'cues': f.get('Consigna entrenador') or '', 'sp': f.get('Espacio aprox.') or '',
                  'notes': f.get('Problema y ajuste') or ''})
    if isinstance(rec['x']['how'], type(None)): rec['x']['how'] = ''
    recs.append(rec)
known = {r['i'] for r in recs}
for k, d in drawn.items():
    if k in known: continue
    recs.append(dict(i=k, b=BL.index(d['bloque']), t=d['titulo'], f=d['formato'], s='Prètzhèt Ink (propias)', sl='Diseño propio Prètzhèt Ink',
                     a=ages(d['edad']) if d.get('edad') else None, ar=d.get('edad', ''), n=d.get('nivel', 'Normal'), p=players(d.get('jugadores'), d['titulo']),
                     rv=0, why='', lb=in_book.get(k, 0), sc=score.get(k, 0), ref='Ficha nueva', dg=1,
                     x={'obj': d.get('objetivo', ''), 'mont': d['montaje'], 'how': d['juego'], 'pts': d['punto'], 'cues': d['consigna'],
                        'fac': d.get('variantes', {}).get('facil', ''), 'dif': d.get('variantes', {}).get('dificil', ''), 'dur': d.get('duracion', ''),
                        'ser': d.get('series', ''), 'adapt': d.get('adaptacion', ''), 'sp': d.get('espacio', '')}))
for r in recs:
    r['x'] = {k: v for k, v in r['x'].items() if v}
    if r['i'] in TOP: r['tp'] = TOP[r['i']]
svgs = {k: render_svg(v['diagrama']) for k, v in drawn.items()}
print(len(recs), sum(1 for r in recs if r['lb']), len(svgs))
blocks = [{'n': b, 'c': '#' + c, 'k': ink(c)} for b, c in BLOCKS.items()]
DATA = json.dumps({'blocks': blocks, 'recs': recs, 'svg': svgs}, ensure_ascii=False, separators=(',', ':'))
tpl = open(os.path.join(ROOT, 'motor', 'app_template.html')).read()
open(os.path.join(ROOT, 'salida', 'app', 'Pretzhet_Ink_app.html'), 'w').write(tpl.replace('/*DATA*/null', DATA).replace('%%LOGO%%', 'data:image/png;base64,' + __import__('base64').b64encode(open(os.path.join(ROOT, 'recursos', 'logo_app.png'), 'rb').read()).decode()))
print('bytes', len(DATA))
