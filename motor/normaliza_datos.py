#!/usr/bin/env python3
"""Limpia títulos feos y propone edad y jugadores que faltan en datos/referencias.json.
Todo lo inferido se marca «(propuesta)». Idempotente: guarda el título original en «Título original»."""
import json, re, unicodedata, collections, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, 'datos', 'referencias.json')
def norm(s): return unicodedata.normalize('NFD', (s or '').lower()).encode('ascii', 'ignore').decode()
def ns(s): return re.sub(r'\s+', '', norm(s))
NUM = {'un':1,'uno':1,'una':1,'dos':2,'tres':3,'cuatro':4,'cinco':5,'seis':6,'siete':7,'ocho':8,'nueve':9,'diez':10,'once':11,'doce':12}
NOUN = {'Rondos':'Rondo','Posesiones y juego de posición':'Posesión','Superioridades':'Superioridad','Oleadas y transiciones':'Transición','Finalización':'Finalización','Defensa y presión':'Defensa','Partidos y situaciones reales':'Juego','Técnica y duelos':'Técnica','Calentamiento':'Activación','Balón parado':'Balón parado','Porteros':'Porteros','Vuelta a la calma':'Vuelta a la calma'}
DEF_PL = {'Rondos':(5,8),'Posesiones y juego de posición':(8,12),'Partidos y situaciones reales':(10,16),'Superioridades':(5,8),'Oleadas y transiciones':(6,10),'Finalización':(4,8),'Defensa y presión':(6,12),'Porteros':(2,4),'Balón parado':(6,10),'Técnica y duelos':(2,6),'Calentamiento':(6,12),'Vuelta a la calma':(6,14)}

def fmt_from(text, title=''):
    """(a, b, k) de «Juego a:b + k» o similar; None si no hay."""
    t = ns(text)
    m = re.search(r'juego(\d{1,2})[:v+x](\d{1,2})(?:\+(\d{1,2}))?', t)
    if not m:
        t2 = norm(title)
        m2 = re.search(r'\b(\d{1,2}) ?(?:v|vs|x|:|contra) ?(\d{1,2})(?: ?\+ ?(\d{1,2}))?', t2)
        if not m2: return None
        m = m2
    a, b, k = int(m.group(1)), int(m.group(2)), int(m.group(3) or 0)
    if not (0 < a <= 15 and 0 < b <= 15): return None
    return a, b, k

def players_from(text, title, block):
    f = fmt_from(text, title)
    if f: return f[0] + f[1] + f[2], 'fmt'
    t = norm(text)
    m = re.search(r'(\w+) equipos de (\w+) jugadores(?: mas (\w+) comodin)?', t)
    if m:
        a = NUM.get(m.group(1)) or (int(m.group(1)) if m.group(1).isdigit() else None)
        b = NUM.get(m.group(2)) or (int(m.group(2)) if m.group(2).isdigit() else None)
        k = NUM.get(m.group(3) or '', 0) or (int(m.group(3)) if (m.group(3) or '').isdigit() else 0)
        if a and b: return a * b + k, 'texto'
    m = re.search(r'\b(\d{1,2}) ?(?:jugadores|participantes)', t)
    if m and 1 < int(m.group(1)) <= 30: return int(m.group(1)), 'texto'
    tt = norm(title)
    if re.search(r'individual', tt): return 1, 'titulo'
    if re.search(r'parejas|por parejas', tt): return 2, 'titulo'
    return None, None

def default_age(n):
    if n is None: return (10, 13)
    if n <= 6: return (10, 13)
    if n <= 12: return (12, 15)
    return (14, 18)

def rasgos(text):
    t = ns(text); out = []
    m = re.search(r'(dos|tres|cuatro|seis|ocho|\d)(?:mini)?porterias(anchas|pequenas|neutrales|normales|grandes)?', t)
    if m:
        n = NUM.get(m.group(1)) or int(m.group(1)); adj = {'anchas':'anchas','pequenas':'pequeñas','neutrales':'neutrales','normales':'normales','grandes':'grandes'}.get(m.group(2) or '', '')
        out.append(f"{n} porterías {adj}".strip())
    elif 'minigoles' in t or 'miniporteria' in t: out.append('miniporterías')
    elif 'unaporteria' in t: out.append('una portería')
    if 'sinportero' in t: out.append('sin portero')
    for k, v in [('hexagono','hexágono'),('pentagono','pentágono'),('triangulo','triángulo'),('rombo','rombo'),('circulo','círculo'),('cuadrados','cuadrados'),('cuadrado','cuadrado'),('pasillo','pasillos'),('carril','carriles'),('franja','franjas'),('cruz','cruz'),('zonacentral','zona central'),('tresequipos','3 equipos')]:
        if k in t: out.append(v); break
    if re.search(r'finalizar.{0,60}zona', t) or 'finalizardesde' in t: out.append('finalizar desde zona')
    m = re.search(r'(?:tras|despuesde|con)(\d{1,2}|dos|tres|cuatro|cinco|seis)pases', t)
    if m: out.append(f"tras {NUM.get(m.group(1)) or m.group(1)} pases")
    if 'comodines' in t or 'comodin' in t:
        if 'esquina' in t: out.append('comodines en esquinas')
        elif 'interior' in t: out.append('comodines dentro')
        elif 'banda' in t or 'lados' in t: out.append('comodines en bandas')
        elif re.search(r'comodinesquevanconelque(defiende|defensor)|conelequipoquedefiende', t): out.append('comodines con la defensa')
        elif re.search(r'conelequipoenposesion|conelequipodeposesion|conelequipoquetienelaposesion', t): out.append('comodines con la posesión')
        else: out.append('comodines')
    m = re.search(r'(\d{1,2}|dos|tres|cuatro)zonas', t)
    if m: out.append(f"{NUM.get(m.group(1)) or m.group(1)} zonas")
    m = re.search(r'cada(\d{1,2})[\'’´]?cambiar', t)
    if m: out.append(f"relevo cada {m.group(1)} min")
    if re.search(r'obligatori', t): out.append('pase obligatorio')
    if re.search(r'limit\w*detoques|dostoques|untoque', t): out.append('toques limitados')
    seen = []; [seen.append(x) for x in out if x not in seen]
    return seen

def fmt_str(a, b, k): return f"{a}v{b}" + (f"+{k}" if k else '')

def new_title(x):
    t = x['Título / referencia'] or ''; mech = x['Mecánica identificada / datos'] or ''
    noun = NOUN.get(x['b08'], 'Juego')
    m = re.match(r'Ficha visual de (\d+)x(\d+) — p\.(\d+)', t)
    if m: return f"{noun} {m.group(1)}v{m.group(2)} (p. {m.group(3)})"
    m = re.match(r'Tarea técnica ilustrada - pág\. (\d+)(?: \| (.+))?$', t)
    if m:
        return (m.group(2).strip().capitalize() if m.group(2) and m.group(2).strip() else f"Tarea técnica (p. {m.group(1)})")
    if re.match(r'Ficha numerada de Level Up - página (\d+)', t) or re.search(r'Juego técnico', t):
        f = fmt_from(mech, t if 'Juego técnico' in t and re.search(r'\d', t) else '')
        r = rasgos(mech)
        n, _ = players_from(mech, '', x['b08']) if not f else (None, None)
        base = f"{noun} {fmt_str(*f)}" if f else (f"{noun} ({n} jug.)" if n else noun)
        pg = re.search(r'página (\d+)', t)
        if r: return base + ': ' + ', '.join(r[:3])
        return base + (f" (p. {pg.group(1)})" if pg else '')
    return t

UGLY = re.compile(r'entrada \d+|Ficha visual|Tarea técnica ilustrada|Ficha numerada|Juego técnico', re.I)

def main():
    ref = json.load(open(P))
    changed = 0; ages_set = 0; pl_set = 0
    for x in ref:
        if x['dec'] not in ('Candidato', 'Revisar nivel', 'Desarrollar'): continue
        t0 = x.get('Título original') or x['Título / referencia']
        if UGLY.search(x['Título / referencia'] or ''):
            x['Título original'] = t0
            nt = new_title(x)
            if nt != x['Título / referencia']: x['Título / referencia'] = nt; changed += 1
    # duplicados: numerar
    cnt = collections.Counter(x['Título / referencia'] for x in ref if x.get('Título original'))
    for x in ref:
        if x.get('Título original') and cnt[x['Título / referencia']] > 1:
            m = re.search(r'entrada (\d+)', x['Título original'])
            if m: x['Título / referencia'] += f" · nº {m.group(1)}"
            else:
                m = re.search(r'p(?:ág\.|ágina|\.) ?(\d+)', x['Título original'])
                if m and '(p.' not in x['Título / referencia']: x['Título / referencia'] += f" (p. {m.group(1)})"
    for x in ref:
        if x['dec'] not in ('Candidato', 'Revisar nivel'): continue
        mech = x['Mecánica identificada / datos'] or ''
        n = None
        if not x['Jugadores'] or not re.search(r'\d', str(x['Jugadores'])):
            n, how = players_from(mech, x['Título / referencia'], x['b08'])
            if n is None:
                lo, hi = DEF_PL[x['b08']]
                x['Jugadores'] = f"{lo}–{hi} (propuesta)"
            else:
                x['Jugadores'] = f"{n} (propuesta)"
            pl_set += 1
            note = 'Jugadores propuestos'
        else:
            m = re.search(r'\d+', str(x['Jugadores'])); n = int(m.group()) if m else None; note = ''
        if not x['Edades'] or 'no indicada' in norm(x['Edades']) or not re.search(r'\d', str(x['Edades'])):
            lo, hi = default_age(n)
            x['Edades'] = f"{lo}–{hi} años (propuesta)"; ages_set += 1
            note = (note + ' y edad' if note else 'Edad') + ' propuestas'
        if note:
            x['Advertencias / siguiente revisión'] = ((x.get('Advertencias / siguiente revisión') or '') + ' ' + note + ' por Claude (propuesta).').strip()
    json.dump(ref, open(P, 'w'), ensure_ascii=False, indent=0)
    print('títulos', changed, 'edades', ages_set, 'jugadores', pl_set)

if __name__ == '__main__': main()
