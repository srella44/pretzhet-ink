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
    m = re.findall(r'(\d{1,2}) ?(?:a|-|–) ?(\d{1,2}) anos', t)
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
    t = norm(title)
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
    for k in ['Tareas Fútbol Base', 'RONDO', 'Level Up Coach', 'FCStage', 'Leicester', 'Athletic', 'AFOPRO', 'Alex Ortiz', 'Javier López', 'FIFA', 'Rella']:
        if k in a: return {'FCStage': 'FCStage Camps', 'Leicester': 'Leicester City Academy', 'Athletic': 'Athletic Club', 'Javier López': 'Javier López (1.380 juegos)'}.get(k, k)
    return 'Redes y webs' if a.startswith('@') or a in ('SoccerXpert', 'Bcoach', 'SoccerDrive') else (a or 'Otras')

# Atribución: genera campos co (coach/autor) y cl (club/equipo) para who().
# No webs, repositorios, plataformas ni handles de Instagram.
_TLC_RE = re.compile(r'toplidercoach · (?:Entrenadores Top|Fútbol Base) ?\(?([^)]*)\)?')
def source_cocl(a):
    """Devuelve (co, cl, tl) — coach, club, flag toplidercoach."""
    a = a or ''
    # TLC con club entre paréntesis
    m = _TLC_RE.match(a)
    if m and m.group(1):
        return ('', m.group(1).title(), 1)
    if a == 'toplidercoach · Fútbol Base':
        return ('', 'TLC Fútbol Base', 1)
    if a == 'toplidercoach · Entrenadores Top':
        return ('', '', 1)
    if a.startswith('toplidercoach'):
        return ('', '', 1)
    # Clubes y academias
    _CLUB_MAP = {
        'Athletic Club Lezama 2005': 'Athletic Lezama',
        'Leicester City Academy': 'Leicester City',
    }
    if a in _CLUB_MAP: return ('', _CLUB_MAP[a], 0)
    if 'Athletic' in a and 'Lezama' in a: return ('', 'Athletic Lezama', 0)
    # Autores deportivos concretos (coach)
    _COACH_MAP = {
        'Roger Crusells': 'Roger Crusells',
        'Samy Ayoub Kassri': 'Samy Ayoub',
        'The Rondo / Brais Acebal': 'Brais Acebal',
        'Tito Ramallo': 'Tito Ramallo',
    }
    if a in _COACH_MAP: return (_COACH_MAP[a], '', 0)
    # Organizaciones deportivas
    _ORG_MAP = {
        'FCStage Camps · dosier de sesiones': 'FCStage Camps',
        'RONDO': 'RONDO',
        'FFF': 'FFF',
        'England Football Learning': 'England FA',
        'FIFA Training Centre': 'FIFA',
    }
    if a in _ORG_MAP: return ('', _ORG_MAP[a], 0)
    # AFOPRO
    if 'AFOPRO' in a:
        # AFOPRO - 25 atribuidos a Mourinho → co: Mourinho, cl: AFOPRO
        m2 = re.search(r'atribuidos a (.+)', a)
        if m2: return (m2.group(1).strip(), 'AFOPRO', 0)
        return ('', 'AFOPRO', 0)
    # Autores con nombre propio (no plataformas ni handles)
    if a.startswith('@') or a in ('SoccerXpert','Bcoach','SoccerDrive','Formation Football','Coach Corner Tactics'):
        return ('', '', 0)
    if a == 'Rella': return ('', 'Rella', 0)
    if a.startswith(('Tareas Fútbol Base','100 ejercicios','Javier López','Level Up Coach','Alex Ortiz','Prime Group','Reel de Instagram')):
        return ('', '', 0)
    if 'FIFA' in a and '/' in a:
        return ('', '', 0)
    return ('', '', 0)

recs = []
for r in refs:
    if r['dec'] not in ('Candidato', 'Revisar nivel'): continue
    s = sections(r.get('Mecánica identificada / datos') or '')
    d = drawn.get(r['ID'])
    _co, _cl, _tl = source_cocl(r['Autor / proveedor'])
    rec = dict(i=r['ID'], b=BL.index(r['b08']), t=r['Título / referencia'], s=short_src(r['Autor / proveedor']), co=_co, cl=_cl,
               a=ages(r['Edades']), ar=r['Edades'] or '', n=r['Dificultad'] or 'Normal', p=players(r['Jugadores'], r['Título / referencia'] or ''),
               f=fmt_of(r['Título / referencia'] or ''), rv=1 if r['dec'] == 'Revisar nivel' else 0, why=r['why'] if r['dec'] == 'Revisar nivel' else '',
               lb=in_book.get(r['ID'], 0), sc=score.get(r['ID'], 0), ref=r.get('URL o PDF · página') or '',
               x={'obj': s.get('Objetivo', ''), 'mont': s.get('Montaje', ''), 'avoid': s.get('Evitar', ''), 'how': s.get('Cómo se juega', '') or s.get('_', ''), 'rules': s.get('Reglas', ''),
                  'pts': (s.get('Puntuación', '') + ' ' + s.get('Puntos', '')).strip(), 'cues': s.get('Consignas', '') or s.get('Frase', ''),
                  'fac': s.get('Más fácil', ''), 'dif': s.get('Más difícil', ''), 'var': s.get('Variantes', ''), 'sp': s.get('Espacio', '').rstrip('. '),
                  'ctx': s.get('Contexto', ''), 'notes': (r.get('Advertencias / siguiente revisión') or '') if (r['ID'].startswith(('TFB', 'RONDO', 'DOS')) or r.get('completed')) else ''})
    if _tl: rec['tl'] = 1
    if r.get('probado'): rec['pr'] = 1
    if r.get('_fmt'): rec['f'] = r['_fmt']
    if d:
        rec.update(t=d['titulo'], f=d['formato'], dg=1, x={'obj': d['objetivo'], 'mont': d['montaje'], 'how': d['juego'], 'pts': d['punto'], 'cues': d['consigna'],
                   'fac': d['variantes']['facil'], 'dif': d['variantes']['dificil'], 'dur': d['duracion'], 'ser': d['series'], 'adapt': d['adaptacion'],
                   'sp': d['espacio']}, ot=d['fuente']['titulo_original'])
    recs.append(rec)
for f in fichas:
    rec = dict(i=f['Código'], b=BL.index(f['b08']), t=f['Nombre'], s='Prètzhèt Ink (propias)', co='', cl='', a=ages(f['Edad']), ar=f['Edad'] or '',
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
    recs.append(dict(i=k, b=BL.index(d['bloque']), t=d['titulo'], f=d['formato'], s='Prètzhèt Ink (propias)', co='', cl='',
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
out = tpl.replace('/*DATA*/null', DATA)
open(os.path.join(ROOT, 'salida', 'app', 'Pretzhet_Ink_app.html'), 'w').write(out)
# Sincronizar automáticamente web/index.html
import shutil
web_dir = os.path.join(ROOT, 'web')
os.makedirs(web_dir, exist_ok=True)
shutil.copy2(os.path.join(ROOT, 'salida', 'app', 'Pretzhet_Ink_app.html'), os.path.join(web_dir, 'index.html'))
print('bytes', len(DATA), '· web/index.html sincronizado')
