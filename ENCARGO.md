# Encargo permanente · Prètzhèt Ink

Este documento es la orden de trabajo completa. Cada ejecución programada empieza sin memoria: lee esto, mira por dónde va el trabajo y haz **una tanda**. **No preguntes nada a Sergio**: si falta un dato, decide de forma razonable, márcalo como «(propuesta)» y sigue.

## Qué es el proyecto

Banco personal de ejercicios de fútbol base de Sergio, organizado en 11 bloques con color. Uso **personal y de sus compañeros, sin venta**. De los mismos archivos salen dos productos:

- **App** (`salida/app/Pretzhet_Ink_app.html`): todo el banco, con filtros. Ficha pequeña en la lista y grande al pulsar.
- **Libro/PDF** (`salida/libro/Pretzhet_Ink_libro.pdf`): los 1.000 mejores, 6 por página A4, con el estilo aprobado (ver `salida/libro/muestra_rondos_p001.pdf`).

Cada ejercicio terminado es un archivo `ejercicios/<ID>.json`. Ese archivo alimenta las dos cosas.

## Qué hacer en cada ejecución

1. **Prepara el entorno.** Si el repositorio `srella44/pretzhet-ink` no está en el directorio de trabajo, añádelo con acceso de escritura y clónalo. Trabaja dentro de él.
2. **Elige la tanda.** Hay dos tareas en paralelo, llamadas **carriles A y B** (el carril viene en el mensaje de la tarea; si no viene, eres A). Abre `estado/cola.json` y numera sus elementos por su posición en el archivo (0, 1, 2…; **no los renumeres**). El carril A toma los de posición par (0, 2, 4…) y el B los de posición impar (1, 3, 5…). Si algún día se abre un carril C, se avisará aquí y se repartirá de nuevo; mientras tanto C no existe. Toma los **24 primeros** de tu carril cuyo `id` todavía no tenga `ejercicios/<id>.json` (los `NUEVO-…` de fase 3 los hace solo el carril A; mira `estado/progreso.md`). Respeta el orden: fase 1 (TOP del libro), fase 2 (resto del libro), fase 3 (crear ejercicios nuevos), fase 4 (resto del banco para la app). Antes de empezar haz `git pull --rebase`.
   - **Reglas de carril para no chocar:** nadie toca `estado/cola.json` ni `datos/` salvo lo que diga este documento. Solo el carril A guarda en git los archivos de `salida/` (libro y app). Los carriles B y C montan y revisan igual, pero antes del commit ejecutan `git checkout -- salida estado/revision_maqueta.txt` y solo suben `ejercicios/` y su línea de `estado/progreso.md` (por ejemplo «carril B»). Si hay conflicto en `progreso.md`, conserva las líneas de todos.
3. **Para cada ejercicio, lee la fuente completa**:
   - Datos en `datos/referencias.json` (campo `Mecánica identificada / datos`, `Advertencias / siguiente revisión`, `URL o PDF · página`, `top`, `probado`) (las fichas propias ORI-/PI- se eliminaron el 2026-11-23 a petición de Sergio: archivo en `datos/descartados/`; **no las rehagas ni crees ejercicios propios nuevos**).
   - Si la fuente es un PDF de `fuentes/`, **mira la página** (`pdftoppm -f N -l N -r 110 -png …`) para ver el diagrama original y colocar bien jugadores, medidas y recorridos. Para FCStage (DOS-) el PDF es `fuentes/dosier.pdf` y el texto `fuentes/dosier_FCStage.txt`; para Tareas Fútbol Base (TFB…) son los PDF de 100, 40 y 25 tareas; para RONDO, los cuatro volúmenes; para Level Up Coach (LU-P…) usa el texto de la fuente en la base (y la página indicada).
   - Para los vídeos que envió Sergio (`VID-…`): en `fuentes/videos/<código>.jpg` hay 8 fotogramas del vídeo en cuadrícula 4×2. **Mira la imagen** (Read), entiende el montaje y el movimiento, dibuja el diagrama y escribe la ficha con palabras propias. Los vídeos casi no traen texto: reglas, edad, puntos y series van como (propuesta). `fuente.autor` = «Reel de Instagram (autor sin identificar)». Entran en la app; no los metas en el libro salvo que falte ejercicio en su bloque.
   - Para toplidercoach (`TLC-…`, «Entrenadores Top»): el texto completo está en `fuentes/toplidercoach_entrenadores.json` (clave = ruta de la URL que figura en `referencias.json`; ignora el aviso de «subscriptores» del final). No hay diagrama original: dibújalo a partir del texto. Escribe con palabras propias (no copies frases), pon `fuente.autor` = «toplidercoach · Entrenadores Top (entrenador)» y marca edad, puntuación y series como (propuesta) si no vienen. La etiqueta de edad de la web («10+», «13+») es la mínima: usa «10–13 años» o «12–13 años». Los 16+/18+ (fase 4) se adaptan a fútbol base y se indica en `completado`.
   - **Títulos y datos ya normalizados** (`motor/normaliza_datos.py`): los títulos feos («Juego técnico 5:5 | entrada 712», «Ficha visual de 4x4 — p.81»…) se renombraron en `referencias.json`; el original está en `Título original` (úsalo en `fuente.titulo_original`). Edad y jugadores que faltaban se propusieron en `referencias.json` con «(propuesta)»: puedes corregirlos en la ficha con mejor criterio al leer el ejercicio. Cada ficha nueva lleva su propio título corto.
   - Para toplidercoach «Fútbol Base» (`FB-…`): la web solo da **título y edades** (el ejercicio es un vídeo de pago; la lista está en `fuentes/toplidercoach_futbol_base.txt`). Haz la ficha como un ejercicio de fútbol base típico de ese nombre: edad = la de la web; montaje, reglas, medidas, nº de jugadores, series y diagrama son **propuesta** (márcalo así en el texto y en `completado`). Antes de escribir, haz una búsqueda web rápida con el título por si hay una descripción del mismo ejercicio. `fuente.autor` = «toplidercoach · Fútbol Base», `titulo_original` = el título de la web, `ref` = su URL. Son ejercicios de 6–15 años: vigila que el nivel y el espacio sean realistas para esa edad.
   - Para Prime Group (`PG-…`, PDF en inglés «500 Football Training Sessions» y «25 Games to Start Training»): el texto completo está en `Mecánica identificada / datos` de `referencias.json` (y en `fuentes/prime_group.json`). Escribe en español con palabras propias. **No copies el diagrama del PDF**: es genérico y casi nunca corresponde al ejercicio; dibújalo a partir del texto. Edad y bloque vienen como (propuesta). Si la nota de la cola dice «posible duplicado de WEB-…», comprueba si ese WEB ya tiene ficha: si es el mismo juego, dilo en `completado` y en el aviso de la tanda. `fuente.autor` = «Prime Group», `titulo_original` = el título inglés, `ref` = el valor de `URL o PDF · página`. **Mejóralas a fondo** (petición de Sergio): la fuente es muy escueta, así que desarrolla cada una al nivel de `datos/modelo_ficha_fb.json`: medidas y material concretos, quién empieza y dónde, juego paso a paso, puntuación clara, qué pasa al fallar, rotaciones, series y descanso, errores típicos, variante fácil y difícil con cambios concretos y adaptación por edades. Si el ejercicio es muy genérico (triángulo, rombo, slalom…), dale un reto o una regla que lo haga más jugado y competitivo. Todo lo añadido va como (propuesta) en `completado`.
4. **Escribe la ficha** `ejercicios/<ID>.json` con el formato de abajo. Reglas de redacción:
   - Español claro, frases cortas, sin jerga innecesaria. Título corto (máximo unos 28 caracteres; el título original va en `fuente.titulo_original`).
   - Conserva las reglas y la puntuación de la fuente. Si faltan, complétalas como **(propuesta)** dentro del texto y añade una nota en `completado`.
   - Montaje + juego + punto + consigna: **unos 340–430 caracteres en total**, para que quepan en la página. El detalle extra va en `objetivo`, `variantes`, `series` y `adaptacion` (salen en la app).
   - Edad en años («8–11 años»). Categorías: prebenjamín 6–7, benjamín 8–9, alevín 10–11, infantil 12–13, cadete 14–15, juvenil 16–18. Si la fuente no la da, propón una razonable.
   - Conserva `top` (motivo) y `probado` si vienen en la base: no quites ni pongas TOP por tu cuenta, salvo en la fase 3 (ejercicios nuevos, sin TOP).
5. **Dibuja el diagrama** en `diagrama` (formato abajo). Estilo aprobado: jugadores vistos desde arriba, campo verde a escala, flechas numeradas en orden, zonas rayadas, leyenda común. Comprueba que no se pisan jugadores, números ni etiquetas, y que nada queda cortado en los bordes (usa `extent` para dejar margen a los jugadores que están fuera del campo).
6. **Monta y revisa**:
   - `python3 motor/build_book.py --tanda ID1,ID2,…` → libro completo + `salida/libro/ultima_tanda.pdf` + vista PNG. Lee `estado/revision_maqueta.txt`: si hay avisos de texto o título que no caben, acorta y repite.
   - **Mira la vista PNG** de la tanda (y, si hace falta, recorta y amplía) para revisar los diagramas. Corrige lo que se vea mal.
   - `python3 motor/build_app.py` → regenera la app.
7. **Fase 3 (ejercicios nuevos)**: crea ejercicios propios originales para el bloque indicado (17 de superioridades, 21 de vuelta a la calma), inspirados en lo que falta en el banco pero sin copiar ninguno. ID `PI-NEW-###` (siguiente número libre). Añádelos al final de su bloque en `datos/seleccion.json` (`kind: "Ficha propia nueva"`, `top: ""`). Anota en `estado/progreso.md` qué `NUEVO-…` cubre cada uno.
8. **Registra y guarda**:
   - Añade una línea a `estado/progreso.md`: fecha, IDs hechos, páginas del libro, avisos pendientes y decisiones que hayas tomado.
   - `git add -A && git commit -m "Tanda N: …"` y `git push`.
   - Termina con un mensaje corto para Sergio: cuántas fichas van, qué bloque, enlace al PDF de la tanda en el repositorio y cualquier aviso.
9. Si la cola está terminada, genera el libro y la app finales, deja un resumen en `estado/progreso.md` y avisa de que el trabajo ha acabado.

## Formato de `ejercicios/<ID>.json`

```json
{
 "id": "TFB25-007", "bloque": "Rondos", "titulo": "Rondo semáforo", "formato": "5v2",
 "edad": "8–11 años", "nivel": "Fácil", "jugadores": "7–14 jug.", "espacio": "12 × 12 m",
 "duracion": "12 min", "series": "3 × 3 min…",
 "objetivo": "…", "montaje": "…", "juego": "…", "punto": "…", "consigna": "… (sin comillas)",
 "variantes": {"facil": "…", "dificil": "…"}, "adaptacion": "…",
 "fuente": {"autor": "Tareas Fútbol Base", "titulo_original": "…", "ref": "25 rondos para fútbol base · pág. 16"},
 "top": "motivo si es TOP, si no vacío", "probado": false, "completado": "qué has añadido tú (propuesta)",
 "diagrama": { … }
}
```

`nivel`: Fácil, Normal, Medio o Alto. Bloques válidos: los 12 de `motor/ficha_engine.py` (`BLOCKS`).

## Formato del diagrama

Coordenadas en **metros**, origen arriba a la izquierda del campo, x hacia la derecha, y hacia abajo. Ángulos en grados (0 = mira a la derecha, 90 = abajo, -90 = arriba, 180 = izquierda) o un punto `[x, y]` hacia el que mira.

| Clave | Ejemplo | Qué dibuja |
|---|---|---|
| `field` | `[12, 12]` | Campo de 12 × 12 m (obligatorio) |
| `extent` | `{"xmin": -2, "xmax": 14, "ymin": -2, "ymax": 14}` | Margen visible alrededor del campo (para jugadores fuera, porterías, etiquetas) |
| `dashed` / `nofield` | `true` | Borde discontinuo / sin borde |
| `tag` | `"pentágono 12 m"` | Texto de la etiqueta de medidas (por defecto «12 × 12 m») |
| `zones` | `{"t": "rect", "r": [5,0,10,10]}` · `{"t": "circle", "x":8, "y":7, "r":1.7}` · `{"t":"poly","pts":[[..],[..]]}` | Zonas rayadas |
| `lines` | `[[[0,6],[24,6],"6 5"]]` | Líneas de carril o zona |
| `cones` / `discs` | `[[0,0],[12,0]]` | Conos naranja / discos amarillos |
| `goals` | `[[0, 9, "L"]]` | Miniportería en borde izquierdo (L) o derecho (R) |
| `porterias` | `{"x": 15, "y": 0, "lado": "T", "ancho": 6, "portero": true}` | Portería grande en lado T, B, L o R, con portero verde opcional |
| `players` | `{"r": "A", "x": 2, "y": 7, "f": 0, "ball": true}` | Jugador: A atacante (amarillo), D defensor (azul), B segundo equipo (rojo), C comodín (blanco). `ghost: true` = semitransparente |
| `balls` | `[[6, 6]]` | Balón suelto |
| `arrows` | `{"a": [2,7], "b": [12,7], "k": "pass", "n": 1, "side": 1}` | `k`: pass (blanco), run (desplazamiento azul discontinuo), cond (conducción naranja ondulada). `n` = número de orden; `side` 1/-1 cambia el lado del número; `s0`/`s1` acortan inicio/fin (px); `nt` posición del número (0–1) |
| `hands` | `[[[3.9,3.6],[6.1,4.4]]]` | Dos jugadores cogidos de la mano |
| `lights` | `[[14.6, 7.6]]` | Semáforo |
| `labels` | `[[6, 1.9, "CONO LIBRE", "start"]]` | Etiquetas en mayúsculas (anclaje start, middle, end) |

Consejos: 3–8 jugadores bien separados (mínimo 2 m entre centros a escala pequeña), 2–4 flechas numeradas que cuenten la acción clave, etiquetas solo donde aclaren. Si la tarea tiene fases, dibuja el momento más representativo.

## Dónde está cada cosa

- `datos/` · base v08 (Excel), referencias, fichas propias, selección del libro, objetivos.
- `ejercicios/` · fichas terminadas (una por ejercicio).
- `motor/` · `ficha_engine.py` (diagramas y plantillas), `build_book.py`, `build_app.py`, estilos y plantilla de la app.
- `fuentes/` · PDF y textos de las fuentes (uso personal; no redistribuir RONDO).
- `estado/` · `cola.json` (orden de trabajo), `progreso.md` (registro), `revision_maqueta.txt` (avisos de espacio).
- `salida/` · libro y app generados.


## Cambios pedidos por Sergio (2026-11-23)
- **Sin ejercicios inventados.** Se eliminaron las 299 fichas propias (ORI-/PI-) y mis 25 PI-NEW (archivados en `datos/descartados/` y `ejercicios_descartados/`). Las entradas de `estado/cola.json` con `"omitir": true` se saltan (no se renumera la cola; el carril sigue contando su posición). Ya no hay fase 3: no se crean ejercicios nuevos.
- **Libro de 1.000** rehecho con los mejores candidatos de las demás fuentes (primero los que ya tienen ficha dibujada). Vuelta a la calma solo tiene 9 (no hay candidatos en las fuentes) y Porteros 24 (la mayoría de portero solo trae título).
- **Explicaciones muy completas.** Sergio quiere que cada ficha se entienda sin dudas: en `montaje`, `juego` y `punto` di quién se coloca dónde, qué hace cada uno, cuánto dura, cuándo se rota y cómo se puntúa, con medidas y números concretos. Usa el máximo de caracteres que quepa en la página (hasta ~430) y pon el resto del detalle (cómo explicarlo, errores típicos, qué observar) en `objetivo`, `variantes`, `series` y `adaptacion`, que salen completos en la app.
- **TOP:** los TOP de las fichas propias se sustituyeron por 18 propuestas `(propuesta)` entre las nuevas del libro; Sergio las revisará.
- **Bloque «Vuelta a la calma» eliminado** (2026-11-23, a petición de Sergio: con 9 ejercicios no merecía bloque). Sus 9 se repartieron: Calentamiento (LU-P160, LEI-122, DOS-073, RONDO-PLANB-24x), Técnica y duelos (RONDO-PLANB-03, DOS-017) y Partidos y situaciones reales (RONDO-PLANB-06, DOS-057, RONDO-PLANB-15). Ya no existe en `BLOCKS`; ningún ejercicio nuevo va a ese bloque. Libro: 11 bloques, 1.000 ejercicios.
- **Modelo para los «Fútbol Base» (FB-):** Sergio aprobó el nivel de detalle de `datos/modelo_ficha_fb.json` («Evitar al destructor»). Cada ficha FB se escribe así: montaje con medidas y materiales, juego paso a paso con las reglas y qué pasa al fallar, puntuación clara, consigna corta, variante fácil y difícil con cambios concretos, y adaptación por edades. Todo lo que no da la web va marcado como (propuesta) en `completado`. Cuida más el diagrama que en la muestra: jugadores separados, números sin tapar a nadie y etiquetas fuera de los jugadores.
- **Porteros (prioridad):** Sergio quiere el bloque Porteros bien desarrollado. Las entradas de `estado/cola.json` con `"prioridad": true` (60 fichas de Porteros) se hacen **antes** que el resto de tu carril (sigue contando la posición par/impar de cada una). Casi todas vienen solo con título (SoccerDrive, SoccerXpert…): desarróllalas a fondo como un entrenador de porteros. Incluye: objetivo técnico concreto (colocación y posición base, blocaje, desvío, caída lateral, juego aéreo y centros, 1 contra 1, salida con pies o saque), montaje con distancias y número de porteros, tiradores o servidores y balones, ejecución paso a paso (qué hace el portero, cómo se mueve, dónde mira, con qué manos y piernas), puntos de coaching (errores típicos y qué corregir), progresión por edades (empieza fácil y sube) y cómo se puntúa. Diagrama con la portería, el portero (rol `G`), quien sirve o dispara, balones y las flechas numeradas. Todo lo que la fuente no diga es (propuesta). Se escribe con palabras propias.
- **Fichas con solo título (Fútbol Base, SoccerDrive, etc.):** se desarrollan al nivel del modelo `datos/modelo_ficha_fb.json`, nunca como un resumen de una línea.
- Porteros pasa de 24 a 60 ejercicios en el libro (se quitaron 36 de otros bloques sin dibujar para mantener 1.000).
