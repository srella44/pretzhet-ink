import json, math, os
ROOT = '/home/claude/pretzhet-ink'
def P(r, x, y, f=0, ball=False, ghost=False):
    d = {'r': r, 'x': round(x, 2), 'y': round(y, 2), 'f': f}
    if ball: d['ball'] = True
    if ghost: d['ghost'] = True
    return d
def ring(cx, cy, rx, ry, n, role='A', ball0=False, start=-90, ghost=False):
    out = []
    for i in range(n):
        a = math.radians(start + 360 * i / n)
        out.append(P(role, cx + rx * math.cos(a), cy + ry * math.sin(a), [cx, cy], ball=(ball0 and i == 0), ghost=ghost))
    return out
def pt(p): return [p['x'], p['y']]
def arr(a, b, k='pass', n=None, side=1, s0=15, s1=15, nt=.5):
    d = {'a': a, 'b': b, 'k': k, 's0': s0, 's1': s1, 'side': side, 'nt': nt}
    if n: d['n'] = n
    return d
def ext(w, h, m=1.5): return {'xmin': -m, 'xmax': w + m, 'ymin': -m, 'ymax': h + m}

fichas = []
def F(i, blk, titulo, formato, edad, jug, esp, dur, ser, obj, mont, juego, punto, cons, fac, dif, adapt, dg, nivel='Fácil'):
    fichas.append(dict(id=f'PI-NEW-{i:03d}', bloque=blk, titulo=titulo, formato=formato, edad=edad, nivel=nivel, jugadores=jug, espacio=esp,
        duracion=dur, series=ser, objetivo=obj, montaje=mont, juego=juego, punto=punto, consigna=cons, variantes={'facil': fac, 'dificil': dif},
        adaptacion=adapt, fuente={'autor': 'Prètzhèt Ink · diseño propio', 'titulo_original': titulo, 'ref': f'Ficha propia nueva PI-NEW-{i:03d}'},
        top='', probado=False, completado='Ejercicio nuevo de diseño propio: todo (edad, medidas, series, reglas y diagrama) es propuesta, sin prueba de campo.', diagrama=dg))

VC = 'Vuelta a la calma'; SU = 'Superioridades'

# 1 Paseo con respiración
pl = [P('A',3,3,0,True),P('A',7,3,180),P('A',3,7,0),P('A',7,7,0),P('A',12,11,0),P('A',16,11,0)]
F(1,VC,'Paseo con respiración','Parejas','6–13 años','6–20 jug.','20 × 14 m','5 min','Una vez, al final de la sesión.','Bajar pulsaciones con pases suaves y respiración lenta.',
 'Parejas con un balón, repartidas por el campo. Todos caminan, sin correr.',
 'Se pasan el balón despacio mientras caminan. Cada 3 pases se paran, inspiran 4 segundos por la nariz y sueltan el aire otros 4 por la boca.',
 'Sin puntuación. Termina cuando el entrenador lo indica.','Pasa suave y respira hondo.',
 'Pasos más cortos y balón más cerca.','Cuentan 6 segundos al inspirar y 6 al soltar.','Con los pequeños, solo 2 respiraciones por parada.',
 dict(field=[20,14],dashed=True,extent=ext(20,14),players=[P('A',3,3,0,True),P('A',8,3,180),P('A',3,7.5,0),P('A',8,7.5,0),P('A',12,11,0),P('A',17,11,0)],
  arrows=[arr([3,3],[8,3],'pass',1,1,10,10),arr([8,3],[3,3],'pass',2,-1,10,10),arr([3,7.5],[8,7.5],'run',None,1,10,10),arr([12,11],[17,11],'run',None,1,10,10)],
  labels=[[10,13.2,'3 PASES → RESPIRA','middle']]))
# 2 Pasa y da un paso atrás
F(2,VC,'Pasa y un paso atrás','Parejas','6–13 años','6–20 jug.','15 × 10 m','5 min','2 vueltas de ida y vuelta.','Pase suave y control de la distancia mientras baja el ritmo.',
 'Parejas frente a frente a 4 m, un balón por pareja.',
 'Cada pase hay que darlo despacio. Después de cada pase, los dos dan un paso atrás hasta separarse unos 12 m. Entonces vuelven acercándose un paso por pase.',
 'Sin puntuación. Una vuelta completa es una serie.','Pase suave, que llegue sin prisa.',
 'Empezar a 3 m y llegar solo a 8 m.','Pasar con la pierna menos hábil.','Prebenjamín: máximo 6 m de separación.',
 dict(field=[15,10],dashed=True,extent=ext(15,10),players=[P('A',3,2.5,0,True),P('A',7,2.5,180),P('A',2,7.5,0),P('A',8,7.5,180,True)],
  arrows=[arr([3,2.5],[7,2.5],'pass',1,1,10,10),arr([7,7.5],[2,7.5],'pass',2,-1,10,10),arr([3,2.5],[1.4,2.5],'run',None,1,5,5),arr([7,2.5],[9,2.5],'run',None,1,5,5)],
  labels=[[7.5,5,'UN PASO ATRÁS POR PASE','middle']]))
# 3 Corro de estiramientos
rp = ring(7,5.5,4,3.4,8,'A',True)
F(3,VC,'Corro de estiramientos','Corro','6–13 años','8–16 jug.','14 × 11 m','6 min','Una ronda completa.','Estirar los músculos que más han trabajado y escuchar al compañero.',
 'Corro de 8 jugadores con un balón. El que lo tiene es quien dirige.',
 'El que tiene el balón propone un estiramiento (muslo, gemelo, espalda) y todos lo aguantan 15 segundos, sin rebotes. Luego pasa el balón al compañero de su derecha, que propone el siguiente.',
 'Sin puntuación. Termina cuando el balón da la vuelta al corro.','Estira sin dolor y respira.',
 'El entrenador propone los estiramientos.','Cada uno estira un músculo que haya usado hoy y dice cuál.','Con grupos mayores de 8, hacer varios corros.',
 dict(field=[14,11],dashed=True,extent=ext(14,11),players=rp,
  arrows=[arr(pt(rp[i]),pt(rp[(i+1)%8]),'pass',i+1 if i<3 else None,1,14,14) for i in range(4)],labels=[[7,5.5,'15 s','middle']]))
# 4 El espejo lento
F(4,VC,'El espejo lento','Parejas','6–13 años','6–20 jug.','12 × 10 m','5 min','2 minutos y cambio de guía.','Coordinación suave y atención al compañero.',
 'Parejas frente a frente a 2 m, sin balón.',
 'Uno guía y hace movimientos lentos con brazos, piernas y tronco. El otro los copia como un espejo. A la señal cambian los papeles.',
 'Sin puntuación. Gana el espejo que no se despega del guía.','Muévete despacio y mira a tu pareja.',
 'Solo movimientos de brazos.','Añadir un balón en el suelo que el guía mueve con la suela y el espejo copia.','Con grupos pequeños, el entrenador hace de guía.',
 dict(field=[12,10],dashed=True,extent=ext(12,10),players=[P('A',3,3,[3,6]),P('B',3,7,[3,3]),P('A',9,3,[9,6]),P('B',9,7,[9,3])],
  arrows=[arr([3,3],[1.6,2],'run',None,1,5,5),arr([3,7],[1.6,8],'run',None,1,5,5)],labels=[[3,5,'GUÍA','middle'],[9,5,'ESPEJO','middle']]))
# 5 Pasa y siéntate
rp = ring(7,5.5,4,3.4,6,'A',True)
F(5,VC,'Pasa y siéntate','Corro','6–12 años','6–10 jug.','14 × 11 m','5 min','Dos rondas.','Bajar el ritmo y recordar el orden del pase.',
 'Corro de 6 jugadores con un balón.',
 'Pasan el balón a un compañero que no sea el de al lado. Quien pasa se sienta. Quien ya está sentado no recibe más pases. Cuando solo queda uno de pie, todos se levantan estirando.',
 'Sin puntuación. Se repite cambiando el orden.','Pasa y siéntate; nadie corre.',
 'Se puede pasar al de al lado.','Pasan con un solo toque.','Grupos grandes: dos corros.',
 dict(field=[14,11],dashed=True,extent=ext(14,11),players=rp,
  arrows=[arr(pt(rp[0]),pt(rp[2]),'pass',1,1,14,14),arr(pt(rp[2]),pt(rp[4]),'pass',2,1,14,14),arr(pt(rp[4]),pt(rp[1]),'pass',3,1,14,14)],labels=[[7,10.4,'QUIEN PASA, SE SIENTA','middle']]))
# 6 Balón en la barriga
F(6,VC,'Balón en la barriga','Individual','6–13 años','Todo el grupo','10 × 8 m','4 min','10 respiraciones.','Relajar la respiración y bajar las pulsaciones.',
 'Cada jugador tumbado boca arriba con un balón sobre la barriga, en fila, separados 2 m.',
 'Respiran hondo y miran cómo sube el balón al inspirar y baja al soltar el aire. Hacen 10 respiraciones lentas con los ojos cerrados.',
 'Sin puntuación.','Que el balón suba y baje despacio.',
 'Solo 5 respiraciones.','Respirar contando hasta 5 al inspirar y 5 al soltar.','Con frío, hacerlo sentados con el balón en las rodillas.',
 dict(field=[10,8],dashed=True,extent=ext(10,8),players=[P('A',1.5+i*2.3,4,90,ghost=True) for i in range(4)],balls=[[1.5+i*2.3,4] for i in range(4)],
  labels=[[5,1.4,'10 RESPIRACIONES','middle']]))
# 7 Tren lento de pases
tr = [P('A',2+i*3.4,5,0,i==3) for i in range(4)]
F(7,VC,'Tren lento de pases','Fila','7–13 años','6–12 jug.','20 × 10 m','5 min','Dos vueltas de campo.','Pase y apoyo caminando, sin prisa.',
 'Filas de 4 jugadores en columna, caminando hacia el otro lado del campo.',
 'El último de la fila pasa el balón al de delante, que lo pasa al siguiente, y así hasta el primero. Luego el primero se queda atrás y vuelve a empezar. Todo el tren camina.',
 'Sin puntuación. Cuenta cuántas veces cruzan el campo sin que se pare el balón.','Camina y pasa con calma.',
 'Filas de 3.','Pase al primer toque.','Reducir a 2 filas si el grupo es pequeño.',
 dict(field=[20,10],dashed=True,extent=ext(20,10),players=[P('A',2+i*3.6,5,0,i==3) for i in range(4)],
  arrows=[arr([12.8,5],[9.2,5],'pass',1,1,12,12),arr([9.2,5],[5.6,5],'pass',2,1,12,12),arr([5.6,5],[2,5],'pass',3,1,12,12),arr([14.5,5],[19,5],'run',None,1,10,10)],labels=[[10,9.2,'TODOS CAMINAN','middle']]))
# 8 Malabares suaves
F(8,VC,'Malabares suaves','Individual','6–13 años','Todo el grupo','15 × 12 m','4 min','3 tandas de 10.','Tacto con el balón en reposo.',
 'Cada jugador con su balón, repartidos por el campo con espacio alrededor.',
 'Lanzan el balón con las manos a la altura del pecho y lo recogen con la suela o el empeine. Cuentan hasta 10 toques suaves sin que el balón se escape.',
 'Sin puntuación. Cada uno compite contra sí mismo.','Toques suaves, sin prisa.',
 'Dejarlo botar una vez entre toque y toque.','Alternar pie derecho e izquierdo.','En pequeños, ayudan con las manos.',
 dict(field=[15,12],dashed=True,extent=ext(15,12),players=[P('A',3,3,90,True),P('A',11,3,90,True),P('A',3,9,90,True),P('A',11,9,90,True),P('A',7,6,90,True)],
  labels=[[7.5,0.6,'10 TOQUES','middle']]))
# 9 Tela de araña
rp = ring(7,5.5,4,3.4,6,'A',True)
F(9,VC,'Tela de araña','Corro','8–13 años','6–12 jug.','14 × 11 m','5 min','Una vuelta y otra al revés.','Pase a distancia suave y atención a quién recibe.',
 'Corro de 6 jugadores con un balón. Todos de pie y relajados.',
 'Pasan al segundo de la derecha, saltándose uno. Así el balón dibuja una estrella. Quien recibe da un estiramiento breve antes de pasar. A mitad de ronda cambian el sentido.',
 'Sin puntuación. Termina cuando el balón vuelve al primero.','Pase suave y mira a quien recibe.',
 'Pasar al de al lado.','Pasar a dos toques como máximo.','Con 7 u 8, saltar a un jugador en cada pase.',
 dict(field=[14,11],dashed=True,extent=ext(14,11),players=rp,
  arrows=[arr(pt(rp[0]),pt(rp[2]),'pass',1,1,14,14),arr(pt(rp[2]),pt(rp[4]),'pass',2,1,14,14),arr(pt(rp[4]),pt(rp[0]),'pass',3,1,14,14)],labels=[[7,5.5,'ESTRELLA','middle']]))
# 10 Conducción en silencio
F(10,VC,'Conducción en silencio','Individual','7–13 años','Todo el grupo','20 × 14 m','5 min','Una vuelta de campo.','Conducción lenta y atención al espacio.',
 'Cada jugador con balón en un campo sin conos. Nadie habla.',
 'Conducen caminando despacio por todo el campo, sin tocarse ni hablar. Al oír un silbido suave, cambian de dirección y siguen. Mirar a los lados, no al balón.',
 'Sin puntuación. Si dos balones chocan, los dos se paran un momento y siguen.','Despacio y sin hablar.',
 'Sin silbido: cambian cuando quieran.','Con la pierna menos hábil.','Con muchos jugadores, usar más campo.',
 dict(field=[20,14],dashed=True,extent=ext(20,14),players=[P('A',4,4,0,True),P('A',16,4,180,True),P('A',4,10,0,True),P('A',16,10,180,True),P('A',10,7,90,True)],
  arrows=[arr([4,4],[9,4],'cond',1,1,10,10),arr([16,4],[11,4],'cond',2,1,10,10),arr([4,10],[9,10],'cond',3,-1,10,10),arr([16,10],[11,10],'cond',None,-1,10,10)],labels=[[10,1.2,'SIN HABLAR','middle']]))
# 11 Estatuas de estiramiento
F(11,VC,'Estatuas de estiramiento','Individual','6–12 años','Todo el grupo','20 × 14 m','5 min','4 estatuas.','Estirar sin perder el control del balón.',
 'Cada jugador con balón en el campo. El entrenador, de pie en el centro.',
 'Conducen despacio. Cuando el entrenador levanta la mano, paran el balón con la suela y se quedan quietos como una estatua. El entrenador dice un estiramiento y lo aguantan 15 segundos.',
 'Sin puntuación. Cada estatua bien hecha suma un aplauso del grupo.','Para, estira y respira.',
 'Elegir ellos el estiramiento.','Estirar con el balón bajo la suela.','Con pequeños, el estiramiento lo muestra el entrenador.',
 dict(field=[20,14],dashed=True,extent=ext(20,14),players=[P('C',10,7,90),P('A',4,3.5,0,True),P('A',16,3.5,180,True),P('A',4,10.5,0,True),P('A',16,10.5,180,True)],
  labels=[[10,1.4,'ESTATUA 15 s','middle']]))
# 12 Pase a un pie
F(12,VC,'Pase a un pie','Parejas','7–13 años','6–20 jug.','12 × 8 m','5 min','5 pases por pie.','Equilibrio y pase suave.',
 'Parejas frente a frente a 4 m, un balón por pareja.',
 'Se pasan el balón apoyados en un solo pie, con los brazos abiertos. Hacen 5 pases y cambian de pie de apoyo. Si pierden el equilibrio, vuelven a contar desde 1.',
 'Sin puntuación. Cuenta cada pareja hasta 10 pases seguidos.','Un pie en el suelo y pase suave.',
 'Pueden apoyar una mano en el hombro del compañero.','Pase de interior y control con la suela.','Para pequeños, 3 m de separación.',
 dict(field=[12,8],dashed=True,extent=ext(12,8),players=[P('A',3,2.5,0,True),P('A',9,2.5,180),P('A',3,6,0),P('A',9,6,180,True)],
  arrows=[arr([3,2.5],[9,2.5],'pass',1,1,12,12),arr([9,6],[3,6],'pass',2,-1,12,12)],labels=[[6,4.2,'UN PIE','middle']]))
# 13 Suela suave
F(13,VC,'Suela suave','Individual','6–13 años','Todo el grupo','14 × 10 m','4 min','20 segundos por pie.','Relajar los pies con balón.',
 'Cada jugador con balón y espacio alrededor, de pie.',
 'Pasan la suela por encima del balón rodándolo suave: adelante, atrás y a los lados, 20 segundos con cada pie. Después lo detienen y estiran el pie descalzo si pueden.',
 'Sin puntuación.','Pie relajado, balón suave.',
 'Sin cambiar de pie, 10 segundos.','Rodar el balón alrededor del cuerpo sin mirar.','Con calzado de tacos, hacerlo con más cuidado.',
 dict(field=[14,10],dashed=True,extent=ext(14,10),players=[P('A',3,3,0,True),P('A',11,3,180,True),P('A',3,7.5,0,True),P('A',11,7.5,180,True)],
  arrows=[arr([3,3.9],[4.3,4.7],'run',None,1,6,6),arr([11,3.9],[9.8,4.7],'run',None,1,6,6)],labels=[[7,5.4,'20 s CADA PIE','middle']]))
# 14 Camino de conos lento
F(14,VC,'Camino de conos lento','Fila','7–13 años','5–15 jug.','18 × 8 m','5 min','Ida y vuelta, 2 veces.','Control cercano con calma.',
 'Una fila de 5 conos separados 3 m. Los jugadores esperan por turnos en un extremo.',
 'Cada jugador conduce el balón en zigzag entre los conos, caminando. Al terminar, vuelve estirando los brazos hacia arriba y respirando. Sale el siguiente cuando va por el tercer cono.',
 'Sin puntuación. No se pisa ningún cono.','Camina y toca suave.',
 'Conos separados 4 m.','Con la pierna menos hábil.','Si hay mucha gente, dos caminos de conos.',
 dict(field=[18,8],dashed=True,extent=ext(18,8),cones=[[3+i*3,4] for i in range(5)],players=[P('A',0.8,4,0,True),P('A',0.8,6.6,0)],
  arrows=[arr([1.8,4],[3.8,3.2],'cond',1,1,8,8),arr([4,3.2],[7,4.8],'cond',2,1,8,8),arr([13.5,4.8],[17,6.5],'run',3,1,8,8)],labels=[[9,7.4,'ZIGZAG','middle']]))
# 15 Tríos caminando
t1 = [P('A',3,3.5,[5,5.5],True),P('A',7,3.5,[5,5.5]),P('A',5,8,[5,5.5])]
t2 = [P('A',13,3.5,[15,5.5],True),P('A',17,3.5,[15,5.5]),P('A',15,8,[15,5.5])]
F(15,VC,'Tríos caminando','Tríos','7–13 años','6–18 jug.','20 × 12 m','5 min','Dos sentidos de giro.','Pase y movimiento sencillo con calma.',
 'Tríos en triángulo de 4 m de lado, un balón por trío.',
 'Se pasan el balón siguiendo las agujas del reloj y, tras cada pase, caminan un paso hacia el compañero que recibió. Cada 6 pases cambian el sentido del giro.',
 'Sin puntuación. Cuenta cuántos giros completos sin errores.','Pasa y camina un paso.',
 'Triángulo de 3 m.','Pase al primer toque.','Si falta uno, en pareja.',
 dict(field=[20,12],dashed=True,extent=ext(20,12),players=t1+t2,
  arrows=[arr(pt(t1[0]),pt(t1[1]),'pass',1,1,12,12),arr(pt(t1[1]),pt(t1[2]),'pass',2,1,12,12),arr(pt(t1[2]),pt(t1[0]),'pass',3,1,12,12),
          arr(pt(t2[0]),pt(t2[2]),'pass',1,-1,12,12),arr(pt(t2[2]),pt(t2[1]),'pass',2,-1,12,12),arr(pt(t2[1]),pt(t2[0]),'pass',3,-1,12,12)],labels=[[10,11,'CAMBIO DE SENTIDO CADA 6','middle']]))
# 16 Pelota viajera
rp = ring(7,5.5,4,3.4,6,'A',True)
F(16,VC,'Pelota viajera','Corro','6–12 años','6–10 jug.','14 × 11 m','5 min','Dos vueltas.','Bajar el ritmo sentados en grupo.',
 'Corro de 6 jugadores sentados con las piernas estiradas hacia el centro.',
 'Pasan el balón con las manos al de la derecha. El que lo recibe lo sube sobre su cabeza, estira la espalda y lo pasa al siguiente. Dan una vuelta y luego la otra.',
 'Sin puntuación. La pelota no puede tocar el suelo.','Sube el balón y estira.',
 'Pasar solo con las manos y sin subir.','Pasar el balón con los pies sentados.','Grupos de más de 6: dos corros.',
 dict(field=[14,11],dashed=True,extent=ext(14,11),players=rp,
  arrows=[arr(pt(rp[i]),pt(rp[(i+1)%6]),'pass',i+1 if i<3 else None,1,14,14) for i in range(4)],labels=[[7,5.5,'BALÓN ARRIBA','middle']]))
# 17 El árbol y el balón
F(17,VC,'El árbol y el balón','Parejas','7–13 años','6–20 jug.','12 × 8 m','4 min','15 s por pierna.','Equilibrio, estiramiento y calma.',
 'Parejas frente a frente a 3 m, un balón por pareja.',
 'Uno sostiene el balón sobre la cabeza y se pone a un pie como un árbol 15 segundos. Luego pasa a su pareja, que repite con la otra pierna.',
 'Sin puntuación. Gana el árbol que no se mueve.','Sube el balón y no te caigas.',
 'Apoyarse en el hombro de la pareja.','Cerrar los ojos 5 segundos.','Con grupos pequeños, el entrenador hace de pareja.',
 dict(field=[12,8],dashed=True,extent=ext(12,8),players=[P('A',3,2.8,0,True),P('A',9,2.8,180),P('A',3,6,0),P('A',9,6,180,True)],
  arrows=[arr([3,2.8],[9,2.8],'pass',1,1,12,12),arr([9,6],[3,6],'pass',2,-1,12,12)],labels=[[6,4.4,'ÁRBOL 15 s','middle']]))
# 18 Pasa y estira
F(18,VC,'Pasa y estira','Parejas','8–13 años','6–20 jug.','15 × 8 m','5 min','6 repeticiones por pareja.','Estirar lo que se acaba de trabajar.',
 'Parejas frente a frente a 5 m, un balón por pareja.',
 'Uno pasa y estira el músculo de la pierna con que pasó (muslo o gemelo) 10 segundos. El otro controla, pasa y estira. Así durante 6 pases.',
 'Sin puntuación.','Pasa y estira la pierna.',
 'Estirar sin soltar el equilibrio apoyándose en la pareja.','Alternar pierna cada pase.','Grupos pequeños: en tríos.',
 dict(field=[15,8],dashed=True,extent=ext(15,8),players=[P('A',3,4,0,True),P('A',12,4,180)],
  arrows=[arr([3,4],[12,4],'pass',1,1,12,12),arr([12,4],[3,4],'pass',2,-1,12,12)],labels=[[7.5,1.4,'PASA → ESTIRA 10 s','middle']]))
# 19 Cuatro esquinas tranquilo
sq = [P('A',2.5,2.5,0,True),P('A',9.5,2.5,90),P('A',9.5,9.5,180),P('A',2.5,9.5,270)]
F(19,VC,'Cuatro esquinas tranquilo','Cuadrado','8–13 años','4–12 jug.','12 × 12 m','5 min','4 vueltas.','Pase y desplazamiento con calma.',
 'Cuadrado de 12 m con un cono en cada esquina. Un jugador por esquina y un balón.',
 'Pasan al siguiente jugador del cuadrado y caminan a ocupar la esquina del compañero. Quien recibe controla y pasa al siguiente. Cada vuelta completa cambian de sentido.',
 'Sin puntuación. Cuentan las vueltas sin parar el balón.','Pasa y camina a la siguiente esquina.',
 'Cuadrado de 8 m.','Con un solo toque.','Si hay más gente, 2 cuadrados.',
 dict(field=[12,12],dashed=True,extent=ext(12,12),cones=[[0,0],[12,0],[12,12],[0,12]],players=sq,
  arrows=[arr(pt(sq[0]),pt(sq[1]),'pass',1,1,12,12),arr(pt(sq[1]),pt(sq[2]),'pass',2,1,12,12),arr(pt(sq[2]),pt(sq[3]),'pass',3,1,12,12),arr(pt(sq[3]),pt(sq[0]),'pass',4,1,12,12)]))
# 20 Pasa y camina
F(20,VC,'Pasa y camina','Dos filas','7–13 años','6–16 jug.','18 × 8 m','5 min','Un cambio de lado cada 2 minutos.','Pase y movimiento a ritmo muy bajo.',
 'Dos filas frente a frente a 8 m. El primero de una fila tiene el balón.',
 'Pasa al primero de la otra fila y camina a colocarse al final de esa fila. Quien recibe controla, pasa y camina igual. El balón no se detiene.',
 'Sin puntuación. Cuentan pases seguidos sin fallo.','Pasa, camina y relaja los brazos.',
 'Filas a 6 m.','Pase de primeras.','Si son pocos, una sola pareja.',
 dict(field=[18,8],dashed=True,extent=ext(18,8),players=[P('A',3,3,0,True),P('A',3,6,0),P('A',15,3,180),P('A',15,6,180)],
  arrows=[arr([3,3],[15,3],'pass',1,1,12,12),arr([3,3.6],[3,6.4],'run',2,1,8,8)],labels=[[9,7.6,'PASA Y CAMINA','middle']]))
# 21 Lo mejor del día
rp = ring(7,5.5,4,3.4,8,'A',True)
F(21,VC,'Lo mejor del día','Corro','6–13 años','8–16 jug.','14 × 11 m','5 min','Una ronda.','Cerrar la sesión con algo positivo de cada uno.',
 'Corro sentado de 8 jugadores con un balón. El entrenador, dentro del corro.',
 'El jugador que tiene el balón dice en una frase lo mejor que ha hecho hoy o algo bueno de un compañero. Pasa el balón al de su derecha y así hasta dar la vuelta.',
 'Sin puntuación. Todos aplauden a quien acaba de hablar.','Di algo bueno y pasa.',
 'Solo decir un nombre y «gracias».','Decir también qué quieres mejorar.','Prebenjamín: contestan con una palabra.',
 dict(field=[14,11],dashed=True,extent=ext(14,11),players=rp+[P('C',7,5.5,90)],
  arrows=[arr(pt(rp[i]),pt(rp[(i+1)%8]),'pass',i+1 if i<3 else None,1,14,14) for i in range(4)]))
# 22 2v1 y relevo
F(22,SU,'2 contra 1 y relevo','2v1','10–13 años','6–12 jug.','20 × 12 m','10 min','6 turnos por pareja.','Aprovechar la superioridad con pase y desmarque.',
 'Campo de 20 × 12 m con una miniportería a la derecha. Dos atacantes salen de la izquierda y un defensor en el centro. Una fila de parejas espera al lado.',
 'Los dos atacantes intentan marcar. Si marcan o pierden el balón, vuelven a su fila y sale la siguiente pareja con un defensor nuevo, que es el último atacante que acabó.',
 'Gol, 1 punto. Si el defensor roba y pasa a la banda, 1 punto para él.','Pasa y desmárcate.',
 'Defensor solo hasta la línea del medio.','Limitar a 8 segundos cada ataque.','Con más gente, dos campos paralelos.',
 dict(field=[20,12],extent=ext(20,12),goals=[[20,6,'R']],players=[P('A',3,4,0,True),P('A',3,8.5,0),P('D',10,4,180)],
  arrows=[arr([3,4],[7,4.5],'cond',1,1,10,10),arr([3,8.5],[10,9.5],'run',2,-1,10,10),arr([7,4.5],[14,9.5],'pass',3,1,10,10)],labels=[[10,11.4,'2 ATACANTES · 1 DEFENSOR','middle']]),nivel='Medio')
# 23 3v2 por carriles
F(23,SU,'3 contra 2 por carriles','3v2','11–14 años','10–15 jug.','24 × 18 m','12 min','Turnos de 3 minutos.','Usar la anchura para crear superioridad.',
 'Campo de 24 × 18 m dividido en tres carriles de 6 m. Tres atacantes (uno por carril) frente a dos defensores. Portería de 6 m a la derecha.',
 'Los atacantes solo pueden cambiar de carril pasando el balón. Si un defensor roba, intenta pasar a una mini zona de 3 m a la izquierda para sumar. Rotan al terminar el turno.',
 'Gol, 1 punto. Robo y pase a la zona de salida, 1 punto defensor.','Pasa para cambiar de carril.',
 'Dejar un carril libre al defensor.','Máximo 6 pases por ataque.','Con 12 jugadores, 4 equipos y un ataque cada vez.',
 dict(field=[24,18],extent=ext(24,18),lines=[[[0,6],[24,6]],[[0,12],[24,12]]],porterias=[dict(x=24,y=9,lado='R',ancho=6,portero=True)],
  players=[P('A',3,3,0,True),P('A',3,9,0),P('A',3,15,0),P('D',13,6,180),P('D',13,12,180)],
  arrows=[arr([3,3],[9,9],'pass',1,1,10,10),arr([3,15],[10,12],'run',2,-1,10,10),arr([9,9],[19,12],'pass',3,1,10,10)]),nivel='Medio')
# 24 4v3 cambio de orientación
F(24,SU,'4 contra 3 con cambio','4v3','12–15 años','8–14 jug.','28 × 20 m','12 min','Tres turnos de 3 minutos.','Mover el balón al lado débil para finalizar.',
 'Campo de 28 × 20 m con dos miniporterías en las esquinas derechas. Cuatro atacantes frente a tres defensores.',
 'Los atacantes solo pueden marcar tras haber cambiado de lado, con un pase largo de banda a banda, al menos una vez en la jugada. Los defensores bloquean y roban.',
 'Gol tras cambio de lado, 2 puntos. Gol sin cambio, 0 (no vale).','Cambia de lado y finaliza.',
 'Un defensor menos al cambiar de lado.','Un toque obligatorio en el cambio.','Para grupos de 16, dos campos.',
 dict(field=[28,20],extent=ext(28,20),goals=[[28,3,'R'],[28,17,'R']],players=[P('A',4,3,0,True),P('A',4,17,0),P('A',9,7,0),P('A',9,13,0),P('D',16,5,180),P('D',16,10,180),P('D',16,15,180)],
  arrows=[arr([4,3],[4,17],'pass',1,1,12,12),arr([4,17],[9,13],'pass',2,1,12,12),arr([9,13],[20,16],'run',3,-1,10,10)],labels=[[14,19,'CAMBIO DE LADO','middle']]),nivel='Medio')
# 25 3v3 con comodín
F(25,SU,'3 contra 3 con comodín','3v3+1','10–15 años','7–14 jug.','24 × 16 m','12 min','Tres turnos de 3 minutos.','Crear superioridad con un comodín que siempre apoya al equipo con balón.',
 'Campo de 24 × 16 m con dos mini porterías. Dos equipos de 3 y un comodín (jugador blanco) que juega siempre con quien tiene el balón.',
 'El equipo con balón juega 4 contra 3. El comodín no puede marcar y no puede ser robado. Si se pierde el balón, el comodín pasa al otro equipo. Cambian de comodín cada 3 minutos.',
 'Gol, 1 punto. 5 pases seguidos, 1 punto.','Busca al comodín y avanza.',
 'El comodín puede marcar.','Comodín limitado a un toque.','Con 8, dos comodines.',
 dict(field=[24,16],extent=ext(24,16),goals=[[0,8,'L'],[24,8,'R']],players=[P('A',4,4,0,True),P('A',4,12,0),P('A',8,8,0),P('D',16,4,180),P('D',16,12,180),P('D',19,8,180),P('C',12,8,90)],
  arrows=[arr([4,4],[11,7.2],'pass',1,1,12,12),arr([12.8,8.8],[5,11.4],'pass',2,-1,12,12),arr([8,8.6],[14,14],'run',3,-1,10,10)]),nivel='Medio')


TXT = {
1:("Parejas con un balón, repartidas por un campo de 20 × 14 m. Todos van caminando; nadie corre en ningún momento.",
   "Dentro de la pareja se pasan el balón despacio, a unos 4 m, sin dejar de caminar. Después de 3 pases seguidos se paran: inspiran 4 segundos por la nariz, sueltan el aire otros 4 por la boca y siguen. Así durante 5 minutos.",
   "Sin puntuación. El entrenador avisa del final y todos se quedan quietos con una última respiración.","Pasa suave y respira hondo."),
2:("Parejas frente a frente, separadas 4 m, con un balón por pareja. Cada pareja ocupa una franja de unos 12 × 3 m.",
   "Se pasan el balón suave y, justo después de cada pase, los dos dan un paso atrás: se van alejando poco a poco hasta unos 12 m. Al llegar, vuelven acercándose un paso después de cada pase, hasta los 4 m del principio.",
   "Sin puntuación. Una ida y vuelta completa es una serie; hacen dos.","Pase suave, sin prisa."),
3:("Corro de 8 jugadores de pie, separados unos 3 m, con un balón. El jugador que lo tiene hace de guía en ese momento.",
   "El guía propone un estiramiento (muslo, gemelo o espalda) y lo enseña. Todos lo hacen y lo aguantan 15 segundos, sin rebotes. Después el guía pasa el balón al compañero de su derecha, que propone otro estiramiento distinto. Así hasta dar la vuelta.",
   "Sin puntuación. Termina cuando el balón vuelve al primer guía.","Estira sin dolor y respira."),
4:("Parejas frente a frente, a 2 m, sin balón. Uno es el guía y el otro el espejo.",
   "El guía hace movimientos muy lentos con brazos, piernas y tronco (levantar un brazo, dar un paso atrás, agacharse). El espejo los copia a la vez, como si fuera su reflejo. A los 2 minutos, a la señal del entrenador, cambian los papeles.",
   "Sin puntuación. Si el guía va demasiado rápido, el espejo se lo dice y el guía repite el movimiento más despacio.","Muévete despacio y mira a tu pareja."),
5:("Corro de 6 jugadores de pie, separados unos 4 m, con un balón.",
   "El que tiene el balón lo pasa a cualquier compañero que no sea el de al lado y se sienta en el suelo. Quien ya está sentado no recibe más pases. Siguen hasta que solo queda un jugador de pie con el balón; entonces todos se levantan y estiran los brazos hacia arriba.",
   "Sin puntuación. Se repite otra ronda empezando por un jugador distinto.","Pasa y siéntate."),
6:("Cada jugador tumbado boca arriba, en fila y separados 2 m, con un balón apoyado sobre la barriga. Basta un espacio de 10 × 8 m.",
   "Cierran los ojos y respiran hondo: el balón sube al inspirar y baja al soltar el aire. Hacen 10 respiraciones lentas contando en voz baja. Al terminar abren los ojos, se sientan despacio y esperan a que acaben los demás.",
   "Sin puntuación. Si el balón se cae, lo colocan otra vez y siguen contando.","Que el balón suba y baje despacio."),
7:("Filas de 4 jugadores, uno detrás de otro y separados 3 m. El último de la fila lleva el balón. Todos caminan hacia el otro lado del campo.",
   "Mientras caminan, el último pasa el balón al de delante, y este al siguiente, hasta llegar al primero. Cuando el balón llega al primero, este se retrasa, se coloca el último de la fila con el balón y empieza otra vez.",
   "Sin puntuación. Cuentan cuántas veces cruzan el campo sin que el balón se pare.","Camina y pasa con calma."),
8:("Cada jugador con su balón, repartidos por el campo con 3 m de espacio libre alrededor.",
   "Lanzan el balón con las manos a la altura del pecho y lo controlan con el empeine o la suela, sin dejar que se aleje. Cuentan en voz baja 10 toques seguidos. Si falla, empiezan otra vez desde 1. Hacen 3 tandas de 10, alternando el pie.",
   "Sin puntuación. Cada uno compite contra sí mismo para llegar a 10.","Toques suaves, sin prisa."),
9:("Corro de 6 jugadores de pie, separados 4 m, con un balón.",
   "Pasan el balón al segundo compañero de su derecha, saltándose al del lado. Así el balón dibuja una estrella dentro del corro. Quien recibe hace un estiramiento de 3 segundos antes de pasar. A mitad de ronda cambian el sentido.",
   "Sin puntuación. Termina cuando el balón vuelve al primer jugador.","Pase suave y mira a quien recibe."),
10:("Todos con un balón dentro de un campo de 20 × 14 m, sin conos. Nadie habla durante la actividad.",
   "Conducen caminando despacio por todo el campo, mirando a los lados y sin tocar a nadie. Cuando el entrenador silba suave, cambian de dirección y siguen. Si dos balones se acercan, los dos jugadores se paran un momento y se dejan paso.",
   "Sin puntuación. Dura 5 minutos.","Despacio y sin hablar."),
11:("Todos con balón en un campo de 20 × 14 m. El entrenador se coloca de pie en el centro, a la vista de todos.",
   "Conducen despacio. Cuando el entrenador levanta la mano, paran el balón con la suela y se quedan quietos como una estatua. El entrenador dice un estiramiento (gemelo, muslo, hombro) y todos lo hacen 15 segundos. Luego vuelven a conducir. Repiten 4 veces.",
   "Sin puntuación. Cada estatua bien hecha se premia con un aplauso del grupo.","Para, estira y respira."),
12:("Parejas frente a frente, a 4 m, con un balón por pareja y espacio libre alrededor.",
   "Se pasan el balón con el interior del pie mientras se mantienen sobre una sola pierna, con los brazos abiertos. Hacen 5 pases y cambian de pierna de apoyo. Si uno pierde el equilibrio y apoya el otro pie, la pareja vuelve a contar desde 1.",
   "Sin puntuación. Cada pareja intenta llegar a 10 pases seguidos.","Un pie en el suelo y pase suave."),
13:("Cada jugador con balón, de pie, con 2 m libres alrededor. No hace falta descalzarse.",
   "Pasan la suela por encima del balón y lo ruedan despacio: hacia delante, hacia atrás y hacia los lados. Lo hacen 20 segundos con cada pie, sin dejar que el balón se escape. Después lo paran y sacuden la pierna para soltar los músculos.",
   "Sin puntuación. Dura 4 minutos en total.","Pie relajado y balón suave."),
14:("Cinco conos en fila, separados 3 m, formando un camino de unos 18 m. Los jugadores esperan por turnos en un extremo, cada uno con su balón.",
   "Cada jugador conduce el balón caminando en zigzag entre los conos, pasando uno por cada lado. Al llegar al final, deja el balón y vuelve andando con los brazos hacia arriba, respirando hondo. Sale el siguiente cuando el anterior pasa el tercer cono.",
   "Sin puntuación. No se pisa ningún cono.","Camina y toca suave."),
15:("Tríos formando un triángulo de 4 m de lado, con un balón por trío. Cada trío ocupa su propio espacio.",
   "Se pasan el balón siguiendo las agujas del reloj. Después de cada pase, quien pasó camina un paso hacia el compañero que recibió, así el triángulo gira poco a poco. Cuando completan 6 pases, cambian de sentido.",
   "Sin puntuación. Cuentan los giros completos sin que el balón se pare.","Pasa y camina un paso."),
16:("Corro de 6 jugadores sentados en el suelo, con las piernas estiradas hacia el centro. Un balón.",
   "Pasan el balón con las manos al de su derecha. Quien lo recibe lo sube sobre su cabeza, estira la espalda y lo pasa al siguiente. Dan una vuelta completa y después otra en sentido contrario.",
   "Sin puntuación. El balón no puede tocar el suelo.","Sube el balón y estira."),
17:("Parejas frente a frente, a 3 m, con un balón por pareja.",
   "Uno sostiene el balón con las dos manos sobre la cabeza y se pone a un pie, como un árbol, durante 15 segundos. Después pasa el balón con las manos a su pareja, que repite el árbol sobre la otra pierna. Hacen 3 turnos cada uno.",
   "Sin puntuación. Gana el árbol que no se mueve.","Sube el balón y no te caigas."),
18:("Parejas frente a frente, a 5 m, con un balón por pareja.",
   "Uno pasa el balón y estira durante 10 segundos el músculo de la pierna con la que ha pasado (muslo o gemelo). Su pareja controla, pasa y estira igual con su pierna. Hacen 6 pases cada uno, estirando siempre justo después de pasar.",
   "Sin puntuación. Dura 5 minutos.","Pasa y estira la pierna."),
19:("Cuadrado de 12 m con un cono en cada esquina. Un jugador por esquina y un balón. Las esquinas se numeran de 1 a 4.",
   "El de la esquina 1 pasa a la 2 y camina hasta ocupar su sitio. El de la 2 controla, pasa a la 3 y camina hasta la esquina 3, y así sucesivamente. Cada vuelta completa cambian de sentido.",
   "Sin puntuación. Cuentan las vueltas sin parar el balón.","Pasa y camina a la siguiente esquina."),
20:("Dos filas frente a frente, a 8 m. El primero de una de ellas tiene el balón.",
   "Pasa al primero de la fila contraria y camina hasta colocarse al final de esa fila. Quien recibe controla, pasa de vuelta al primero de la fila de enfrente y camina igual. El balón va y viene sin pararse, todos a ritmo de paseo.",
   "Sin puntuación. Cuentan los pases seguidos sin fallo.","Pasa, camina y relaja los brazos."),
21:("Corro sentado de 8 jugadores, con un balón. El entrenador se sienta dentro del corro.",
   "El jugador que tiene el balón dice en una frase lo mejor que ha hecho hoy o algo bueno de un compañero. Después rueda el balón al de su derecha, y así hasta dar la vuelta completa. Todos aplauden al terminar cada intervención.",
   "Sin puntuación. Nadie está obligado a hablar: puede pasar el balón sin decir nada.","Di algo bueno y pasa."),
22:("Campo de 20 × 12 m con miniportería a la derecha. Dos atacantes salen de la izquierda y un defensor espera en el centro.",
   "Los dos atacantes intentan marcar. Si marcan o lo pierden, vuelven a la fila y sale la siguiente pareja. El defensor aguanta 3 ataques.",
   "Gol, 1 punto. Si el defensor roba y llega a la línea de salida, 1 punto para él.","Pasa y desmárcate."),
23:("Campo de 24 × 18 m en 3 carriles de 6 m. Un atacante por carril, 2 defensores y una portería de 6 m a la derecha.",
   "Los atacantes solo cambian de carril con un pase, nunca conduciendo. Los defensores se mueven por todos los carriles. Cada ataque dura 20 s como máximo y luego se rotan los papeles.",
   "Gol, 1 punto. Robo y balón a la línea de salida, 1 punto para los defensores.","Pasa para cambiar de carril."),
24:("Campo de 28 × 20 m con dos miniporterías en las esquinas del fondo derecho. Cuatro atacantes frente a tres defensores.",
   "Antes de marcar deben pasar el balón de una banda a la otra con un pase largo en esa jugada. Los defensores presionan y, si roban, llevan el balón a la línea de salida. Tras cada ataque rotan los papeles.",
   "Gol tras cambio de lado, 2 puntos. Gol sin cambio previo, no vale.","Cambia de lado y finaliza."),
25:("Campo de 24 × 16 m con miniportería en cada fondo. Dos equipos de 3 y un comodín (blanco) que juega siempre con el equipo que tiene el balón.",
   "El equipo con balón juega 4 contra 3. El comodín no puede marcar ni le pueden robar el balón. Si el balón cambia de equipo, el comodín cambia con él. Cada 3 minutos, otro jugador es comodín.",
   "Gol, 1 punto. 5 pases seguidos, 1 punto extra.","Busca al comodín y avanza."),
}
def shift(dg, dx, dy):
    for p_ in dg.get('players', []):
        p_['x'] = round(p_['x'] + dx, 2); p_['y'] = round(p_['y'] + dy, 2)
        if isinstance(p_['f'], list): p_['f'] = [p_['f'][0] + dx, p_['f'][1] + dy]
    for a in dg.get('arrows', []):
        a['a'] = [a['a'][0] + dx, a['a'][1] + dy]; a['b'] = [a['b'][0] + dx, a['b'][1] + dy]
    for k in ('cones', 'balls'): dg[k] = [[c[0] + dx, c[1] + dy] for c in dg.get(k, [])] if k in dg else dg.get(k)
    if dg.get('balls') is None: dg.pop('balls', None)
    if dg.get('cones') is None: dg.pop('cones', None)
    for l in dg.get('labels', []): l[0] += dx; l[1] += dy
for f in fichas:
    n_ = int(f['id'][-3:]); f['montaje'], f['juego'], f['punto'], f['consigna'] = TXT[n_]
    dg = f['diagrama']
    if dg['field'] == [14, 11]:            # corros: campo más ajustado
        shift(dg, -2, -1.5); dg['field'] = [10, 8]
    gl = 'goals' in dg or 'porterias' in dg
    pts = [(p_['x'], p_['y']) for p_ in dg.get('players', [])] + [(l[0], l[1]) for l in dg.get('labels', [])] + [tuple(c) for c in dg.get('cones', [])]
    W, H = dg['field']; m = 1.3 if gl else 0.9
    dg['extent'] = {'xmin': min([0] + [x for x, y in pts]) - m, 'xmax': max([W] + [x for x, y in pts]) + m,
                    'ymin': min([0] + [y for x, y in pts]) - m, 'ymax': max([H] + [y for x, y in pts]) + m}
for f in fichas:
    n = sum(len(f[k]) for k in ('montaje', 'juego', 'punto', 'consigna'))
    if not 330 <= n <= 440: print('LONGITUD', f['id'], n)
    json.dump(f, open(f"{ROOT}/ejercicios/{f['id']}.json", 'w'), ensure_ascii=False, indent=1)
print(len(fichas))
