# Encargo permanente · Prètzhèt Ink

Este documento es la orden de trabajo completa. Cada ejecución programada empieza sin memoria: lee esto, mira por dónde va el trabajo y haz **una tanda**. **No preguntes nada a Sergio**: si falta un dato, decide de forma razonable, márcalo como «(propuesta)» y sigue.

## Qué es el proyecto

Banco personal de ejercicios de fútbol base de Sergio, organizado en 12 bloques con color. Uso **personal y de sus compañeros, sin venta**. De los mismos archivos salen dos productos:

- **App** (`salida/app/Pretzhet_Ink_app.html`): todo el banco, con filtros. Ficha pequeña en la lista y grande al pulsar.
- **Libro/PDF** (`salida/libro/Pretzhet_Ink_libro.pdf`): los 1.000 mejores, 6 por página A4, con el estilo aprobado (ver `salida/libro/muestra_rondos_p001.pdf`).

Cada ejercicio terminado es un archivo `ejercicios/<ID>.json`. Ese archivo alimenta las dos cosas.

## Qué hacer en cada ejecución

1. **Prepara el entorno.** Si el repositorio `srella44/pretzhet-ink` no está en el directorio de trabajo, añádelo con acceso de escritura y clónalo. Trabaja dentro de él.
2. **Elige la tanda.** Hay dos tareas en paralelo, llamadas **carriles A y B** (el carril viene en el mensaje de la tarea; si no viene, eres A). Abre `estado/cola.json` y numera sus elementos por su posición en el archivo (0, 1, 2…; **no los renumeres**). El carril A toma los de posición par (0, 2, 4…) y el B los de posición impar (1, 3, 5…). Si algún día se abre un carril C, se avisará aquí y se repartirá de nuevo; mientras tanto C no existe. Toma los **24 primeros** de tu carril cuyo `id` todavía no tenga `ejercicios/<id>.json` (los `NUEVO-…` de fase 3 los hace solo el carril A; mira `estado/progreso.md`). Respeta el orden: fase 1 (TOP del libro), fase 2 (resto del libro), fase 3 (crear ejercicios nuevos), fase 4 (resto del banco para la app). Antes de empezar haz `git pull --rebase`.
   - **Reglas de carril para no chocar:** nadie toca `estado/cola.json` ni `datos/` salvo lo que diga este documento. Solo el carril A guarda en git los archivos de `salida/` (libro y app). Los carriles B y C montan y revisan igual, pero antes del commit ejecutan `git checkout -- salida estado/revision_maqueta.txt` y solo suben `ejercicios/` y su línea de `estado/progreso.md` (por ejemplo «carril B»). Si hay conflicto en `progreso.md`, conserva las líneas de todos.
3. **Para cada ejercicio, lee la fuente completa**:
   - Datos en `datos/referencias.json` (campo `Mecánica identificada / datos`, `Advertencias / siguiente revisión`, `URL o PDF · página`, `top`, `probado`) o `datos/fichas_propias.json` (códigos ORI- y PI-).
   - Si la fuente es un PDF de `fuentes/`, **mira la página** (`pdftoppm -f N -l N -r 110 -png …`) para ver el diagrama original y colocar bien jugadores, medidas y recorridos. Para FCStage (DOS-) el PDF es `fuentes/dosier.pdf` y el texto `fuentes/dosier_FCStage.txt`; para Tareas Fútbol Base (TFB…) son los PDF de 100, 40 y 25 tareas; para RONDO, los cuatro volúmenes; para Level Up Coach (LU-P…) usa el texto de la fuente en la base (y la página indicada).
   - Para los vídeos que envió Sergio (`VID-…`): en `fuentes/videos/<código>.jpg` hay 8 fotogramas del vídeo en cuadrícula 4×2. **Mira la imagen** (Read), entiende el montaje y el movimiento, dibuja el diagrama y escribe la ficha con palabras propias. Los vídeos casi no traen texto: reglas, edad, puntos y series van como (propuesta). `fuente.autor` = «Reel de Instagram (autor sin identificar)». Entran en la app; no los metas en el libro salvo que falte ejercicio en su bloque.
   - Para toplidercoach (`TLC-…`, «Entrenadores Top»): el texto completo está en `fuentes/toplidercoach_entrenadores.json` (clave = ruta de la URL que figura en `referencias.json`; ignora el aviso de «subscriptores» del final). No hay diagrama original: dibújalo a partir del texto. Escribe con palabras propias (no copies frases), pon `fuente.autor` = «toplidercoach · Entrenadores Top (entrenador)» y marca edad, puntuación y series como (propuesta) si no vienen. La etiqueta de edad de la web («10+», «13+») es la mínima: usa «10–13 años» o «12–13 años». Los 16+/18+ (fase 4) se adaptan a fútbol base y se indica en `completado`.
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
