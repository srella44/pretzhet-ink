"""Monta el libro con todas las fichas dibujadas (ejercicios/*.json) en el orden de datos/seleccion.json.
Uso:  python3 motor/build_book.py            -> salida/libro/Pretzhet_Ink_libro.pdf + vista PNG de la última página tocada
      python3 motor/build_book.py --tanda ID1,ID2,...   -> además, PDF solo con las páginas donde están esas fichas
"""
import json, os, sys, subprocess, glob, shutil
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'motor'))
from ficha_engine import book_page, render_svg, web_page

KICK = {
 'Calentamiento': ('Activa cabeza y balón.', 'Juegos para empezar la sesión con todos en movimiento y muchas decisiones desde el primer minuto.'),
 'Técnica y duelos': ('Gana tu duelo.', 'Pase, control, conducción, regate y 1 contra 1 con oposición y decisión.'),
 'Rondos': ('Pasa, muévete y mira.', 'Conservar con superioridad: apoyos, perfiles y pase antes de que llegue la presión.'),
 'Posesiones y juego de posición': ('Ten el balón con sentido.', 'Conservar y progresar con comodines, zonas, paredes y tercer hombre.'),
 'Superioridades': ('Fija y pasa.', 'Atacar con un jugador más: reconocer la ventaja y aprovecharla antes de que desaparezca.'),
 'Oleadas y transiciones': ('Cuando cambia el balón, cambias tú.', 'Ataques encadenados, contraataques y reacción tras pérdida.'),
 'Finalización': ('Llega y remata.', 'Tiro, remate y llegada al área con oposición y en competición.'),
 'Defensa y presión': ('Defiende juntos.', 'Presión, coberturas, temporización y línea defensiva.'),
 'Partidos y situaciones reales': ('Juega con reglas que enseñan.', 'Partidos y juegos reducidos con condiciones que provocan lo que se entrena.'),
 'Balón parado': ('Cada saque es una ocasión.', 'Córners, faltas y saques de banda trabajados como juego.'),
 'Porteros': ('El primer atacante, el último defensor.', 'Tareas específicas y porteros integrados en el juego.'),
 'Vuelta a la calma': ('Cierra la sesión.', 'Juegos de baja intensidad, retos y repaso para terminar.'),
}
ORDER = list(KICK)

def chrome_pdf(html_path, pdf_path):
    subprocess.run(['google-chrome', '--headless=new', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer',
                    f'--print-to-pdf={pdf_path}', f'file://{html_path}'], capture_output=True)

def overflow_report(html_paths):
    """Devuelve [(pagina, codigo, problema)] para fichas cuyo texto o título no caben."""
    try:
        from playwright.sync_api import sync_playwright
    except Exception:
        return [('-', '-', 'playwright no disponible: revisa la vista a ojo')]
    out = []
    js = '''() => [...document.querySelectorAll('.card')].map(c => {
        const t = c.querySelector('.txt'), h = c.querySelector('h2'), hd = c.querySelector('header');
        const last = t.lastElementChild.getBoundingClientRect().bottom, cb = c.getBoundingClientRect().bottom; return [c.querySelector('.code').textContent, Math.round(last - cb), hd.scrollWidth - hd.clientWidth];
    })'''
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=shutil.which('google-chrome'), args=['--no-sandbox'])
        pg = b.new_page(viewport={'width': 794, 'height': 1123})
        for hp in html_paths:
            pg.goto('file://' + hp); pg.wait_for_timeout(150)
            for code, dt, dh in pg.evaluate(js):
                if dt > 2: out.append((os.path.basename(hp), code, f'texto no cabe ({dt}px de más)'))
                if dh > 2: out.append((os.path.basename(hp), code, f'título demasiado largo ({dh}px)'))
        b.close()
    return out

def main():
    sel = json.load(open(os.path.join(ROOT, 'datos', 'seleccion.json')))
    ex = {}
    for f in glob.glob(os.path.join(ROOT, 'ejercicios', '*.json')):
        e = json.load(open(f)); ex[e['id']] = e
    tanda = set(sys.argv[sys.argv.index('--tanda') + 1].split(',')) if '--tanda' in sys.argv else set()
    tmp = os.path.join(ROOT, 'salida', 'tmp'); shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    pages, tanda_pages, page_no, htmls = [], [], 0, []
    for blk in ORDER:
        ids = [p['id'] for p in sel if p['blk'] == blk and p['id'] in ex]
        n = 1
        for i in range(0, len(ids), 6):
            chunk = [ex[k] for k in ids[i:i + 6]]
            page_no += 1
            html = book_page(chunk, blk, KICK[blk][0], KICK[blk][1], page_no, start_n=n)
            hp = os.path.join(tmp, f'p{page_no:03d}.html'); open(hp, 'w').write(html)
            pp = os.path.join(tmp, f'p{page_no:03d}.pdf'); chrome_pdf(hp, pp)
            pages.append(pp); htmls.append(hp)
            if tanda & set(ids[i:i + 6]): tanda_pages.append(pp)
            n += len(chunk)
    # fichas de la tanda que no están en datos/seleccion.json (solo app): hojas de revisión aparte, fuera del libro
    in_sel = {p['id'] for p in sel}
    extra = [k for k in sorted(tanda) if k in ex and k not in in_sel]
    rev_no = 0
    for blk in ORDER:
        ids = [k for k in extra if ex[k]['bloque'] == blk]
        for i in range(0, len(ids), 6):
            rev_no += 1
            chunk = [ex[k] for k in ids[i:i + 6]]
            html = book_page(chunk, blk, 'Revisión de tanda · fuera del libro.', ' Fichas solo para la app (no están en la selección del libro).', 0, start_n=i + 1)
            hp = os.path.join(tmp, f'r{rev_no:03d}.html'); open(hp, 'w').write(html)
            pp = os.path.join(tmp, f'r{rev_no:03d}.pdf'); chrome_pdf(hp, pp)
            tanda_pages.append(pp); htmls.append(hp)
    if not pages:
        print('sin fichas'); return
    out = os.path.join(ROOT, 'salida', 'libro', 'Pretzhet_Ink_libro.pdf')
    subprocess.run(['pdfunite'] + pages + [out], check=True)
    if tanda_pages:
        tp = os.path.join(ROOT, 'salida', 'libro', 'ultima_tanda.pdf')
        subprocess.run(['pdfunite'] + tanda_pages + [tp] if len(tanda_pages) > 1 else ['cp', tanda_pages[0], tp], check=True)
        subprocess.run(['pdftoppm', '-r', '110', '-png', '-singlefile', tanda_pages[-1], os.path.join(ROOT, 'salida', 'libro', 'ultima_tanda_vista')])
    # diagramas sueltos (web/app)
    os.makedirs(os.path.join(ROOT, 'salida', 'svg'), exist_ok=True)
    for k, e in ex.items():
        open(os.path.join(ROOT, 'salida', 'svg', f'{k}.svg'), 'w').write(render_svg(e['diagrama']))
    probs = overflow_report(htmls)
    with open(os.path.join(ROOT, 'estado', 'revision_maqueta.txt'), 'w') as fh:
        fh.write('\n'.join(' · '.join(x) for x in probs) or 'Sin problemas de espacio.')
    for x in probs: print('AVISO', *x)
    shutil.rmtree(tmp, ignore_errors=True)
    print(f'{page_no} páginas · {len(ex)} fichas dibujadas · {out}')

if __name__ == '__main__':
    main()
