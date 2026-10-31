from definiciones import *

#### Algunas funciones ya dadas

def son_posiciones_vecinas(pos1 : Posicion, pos2 : Posicion) -> bool: # pragma: no cover
    return (pos1.fila == pos2.fila and abs(pos1.columna - pos2.columna) == 1) \
        or (pos1.columna == pos2.columna and abs(pos1.fila - pos2.fila) == 1)

def direccion_desde_hasta(pos1 : Posicion, pos2 : Posicion) -> Direccion: # pragma: no cover
    assert son_posiciones_vecinas(pos1, pos2)
    if pos1.fila < pos2.fila:
       return NORTE
    elif pos1.fila > pos2.fila:
       return SUR
    elif pos1.columna < pos2.columna:
       return ESTE
    else:
       return OESTE

def pasar_turno(j : Juego) -> Juego: # pragma: no cover
    return Juego(j.tablero, oponente(j.turno), 0)

#### Ejercicio 1

def tablero_bien_formado(t : Tablero) -> bool:
    """
    Indica si el tablero tiene cantidad de filas ALTO y cada fila tiene ANCHO casillas

    PRE: True

    Args:
        t (Tablero): un tablero

    Returns:
        True si tiene el numero correcto de filas (ALTO) y todas sus filas tienen el numero correcto de elementos (ANCHO)
        False si no
    """
    # Coincide ALTO
    coincide_alto: bool = len(t) == ALTO

    # Coincide ANCHO
    coincide_ancho: bool = True
    for i in range(len(t)):
        if len(t[i]) != ANCHO:
            coincide_ancho = False

    return coincide_alto and coincide_ancho


def posicion_en_tablero(pos : Posicion) -> bool:
    """
    Indica si la posición se encuentra dentro de los límites del tablero

    PRE: True

    Args:
        pos (Posicion): posición en el tablero (fila, columna)

    Returns:
        True si sus coordenadas pertenecen a una casilla del tablero
        False si no
    """
    # fila válida
    fila_valida: bool = 0 <= pos.fila < ALTO

    # col válida
    col_valida: bool = 0 <= pos.columna < ANCHO

    return fila_valida and col_valida


def movimiento_bien_formado(m : Movimiento) -> bool:
    """
    Indica si el movimiento está bien formado: que su posición sea válida y que el número de pasos corresponda a la acción realizada

    PRE: True

    Args:
        m (Movimiento): movimiento (acción, origen, pasos)

    Returns:
        True si el movimiento está bien formado
        False si no
    """
    posicion_valida: bool = posicion_en_tablero(m.origen)
    movimiento_valido: bool

    if m.accion == MOVER_A_SECAS:
        movimiento_valido = len(m.pasos) == 1

    #  m.accion == ARRASTRAR or m.accion == EMPUJAR
    else:
        movimiento_valido = len(m.pasos) == 2

    return posicion_valida and movimiento_valido


def juego_bien_formado(j : Juego) -> bool:
    """
    Indica si el juego está bien formado (el tablero está bien formado y los pasos consumidos son mayores o igual a 0 y menores estrictos al máximo de pasos)

    PRE: True

    Args:
        j (Juego): Juego (tablero, turno, pasos_consumidos)

    Returns:
        True si el juego está bien formado
        False si no
    """
    tablero_valido: bool = tablero_bien_formado(j.tablero)

    pasos_consumidos_validos: bool = 0 <= j.pasos_consumidos < MAX_PASOS

    return tablero_valido and pasos_consumidos_validos

#### Ejercicio 2

### Funciones Auxiliares Ejercicio 2

def hayFiguraDeColor(t: Tablero, pos: Posicion, f: Figura, col: Color) -> bool:
    """
    Determina si en la posicion pos del tablero t hay una figura f de color col, si pos es válida.

    PRE: True

    Args:
        t (Tablero): un tablero
        pos (Posicion): una posición
        f (Figura): Elefante | Camello | Caballo | Perro | Gato | Conejo
        col (Color): Dorado | Plateado

    Returns:
        True si en la posición pos del tablero t hay una figura f de color col y pos es válida
        False si no
    """
    return hayPiezaDeColor(t, pos, col) and casilla_en_posicion(t, pos).figura == f


def hayPiezaDeColor(t: Tablero, pos: Posicion, col: Color) -> bool:
    """
    Determina si en la posicion pos del tablero t hay una pieza de color col,
    y si pos es válida.

    PRE: True

    Args:
        t (Tablero): un tablero
        pos (Posicion): una posicion
        col (Color): color de la pieza en la posición del tablero

    Returns:
        True si hay una pieza de color col en la posicion del tablero
        False si no
    """
    return hayPieza(t, pos) and casilla_en_posicion(t, pos).color == col

### Problemas Ejercicio 2


def posicion_vecina_hacia(pos : Posicion, d : Direccion) -> Posicion:
    """
    Dada una posición inicial y una dirección de movimiento, devuelve la posición final

    PRE: True

    Args:
        pos (Posicion): posición inicial
        d (Direccion): dirección de movimiento

    Returns:
        pos' (Posición): posición final producto del movimiento desde pos en la dirección d
    """
    pos_final: Posicion

    if d == NORTE:
        pos_final = Posicion(pos.fila + 1, pos.columna)
    elif d == SUR:
        pos_final = Posicion(pos.fila - 1, pos.columna)
    elif d == ESTE:
        pos_final = Posicion(pos.fila, pos.columna + 1)
    # d == OESTE
    else:
        pos_final = Posicion(pos.fila, pos.columna - 1)

    return pos_final

def casilla_en_posicion(t : Tablero, p : Posicion) -> Casilla:
    """
    Toma un tablero t y una posición p y devuelve la casilla que se encuentra en la
    posición p del tablero t

    PRE: tablero_bien_formado(t) and posicion_en_tablero(p)

    Args:
        t (Tablero): un tablero
        p (Posicion): una posicion

    Returns:
        Casilla (Casilla): la casilla en la posición p del tablero t
    """
    return t[p.fila][p.columna]


def hay_casilla_vacia(t : Tablero, pos : Posicion) -> bool:
    """
    Dada una posición pos y un tablero t, verifica que la casilla en pos de t esté vacía

    PRE: tablero_bien_formado(t) and posicion_en_tablero(pos)

    Args:
        t (Tablero): un tablero
        pos (Posicion): una posicion

    Returns:
        True si la casilla en la posición pos del tablero t está vacía
        False si no
    """
    return t[pos.fila][pos.columna] == VACIA


def hay_pieza_de_color(t : Tablero, pos : Posicion, col : Color) -> bool:
    """
    Determina si en la posicion pos del tablero t hay una pieza de color col,
    y si pos es válida.

    PRE: tablero_bien_formado(t) and posicion_en_tablero(pos)

    Args:
        t (Tablero): un tablero
        pos (Posicion): una posicion
        col (Color): color de la pieza en la posición del tablero

    Returns:
        True si hay una pieza de color col en la posicion del tablero
        False si no
    """
    return hayPiezaDeColor(t, pos, col)



#### Ejercicio 3

### Funciones Auxiliares

def hayPieza(t: Tablero, pos: Posicion) -> bool:
    """
    Indica si hay una pieza en la posicion pos del tablero t

    PRE: tablero_bien_formado(t)

    Args:
        t (Tablero): un tablero
        pos (Posicion): una posicion

    Returns:
        True si hay una pieza en pos
        False si no
    """
    return posicion_en_tablero(pos) and t[pos.fila][pos.columna] != VACIA


def hayPiezaAmigaHacia (t: Tablero, pos: Posicion, d: Direccion) -> bool:
    """
    Indica si la pieza en la posición dada tiene una pieza adyacente del mismo color en la dirección dada

    PRE: tablero_bien_formado(t) and posicion_en_tablero(pos) and hayPieza(t, pos)

    Args:
        t (Tablero): un tablero
        pos (Posicion): posición de la pieza a la que le buscamos pieza amiga
        d (Direccion): indica en qué dirección buscamos la pieza amiga

    Returns:
        True si la pieza de pos tiene una pieza del mismo color en la casilla adyacente en la
        dirección dada y la casilla adyacente existe
        False si no
    """
    # Obtenemos el color de la pieza en pos
    color: Color = casilla_en_posicion(t, pos).color

    # Obtenemos la posición donde queremos buscar una pieza amiga
    pos_vecina: Posicion = posicion_vecina_hacia(pos, d)

    # Devolvemos True si hay una pieza del mismo color (amiga) en la posición vecina
    return hayPiezaDeColor(t, pos_vecina, color)


def hayPiezaEnemigaMasFuerteHacia(t : Tablero, pos : Posicion, d : Direccion) -> bool:
    """
    Analiza si en la direccion 'd' hay una figura enemiga mas fuerte que la pieza de origen (en pos)

    PRE: tablero_bien_formado(t) and posicion_en_tablero(pos) and hayPieza(t, pos)

    Args:
        t (Tablero): un tablero
        pos (Posicion): posicion de la pieza de origen
        d (Direccion): dirección en la cual buscamos una pieza enemiga más fuerte

    Returns:
        True si la vecina en 'd' existe, es enemiga y tiene más fuerza que la pieza de origen
        False si no
    """
    pieza_origen: Casilla = casilla_en_posicion(t, pos)
    pos_enemiga: Posicion = posicion_vecina_hacia(pos, d)

    return hayPiezaDeColor(t, pos_enemiga, oponente(pieza_origen.color)) \
        and fuerza(pieza_origen.figura) < fuerza(casilla_en_posicion(t, pos_enemiga).figura)


def hayCasillaVacia(t : Tablero, pos : Posicion) -> bool:
    """
    Dada una posición pos y un tablero t, verifica que la casilla en pos de t esté vacía

    PRE: tablero_bien_formado(t)

    Args:
        t (Tablero): un tablero
        pos (Posicion): una posicion

    Returns:
        True si pos es una posición válida y la casilla en la posición pos del tablero t está vacía
        False si no
    """
    return posicion_en_tablero(pos) and t[pos.fila][pos.columna] == VACIA

### Problemas Ejercicio 3

def hay_casilla_vacia_hacia(t : Tablero, pos : Posicion, d : Direccion) -> bool:
    """
    Indica si, dada una determinada casilla, existe una casilla vecina vacía en una dirección determinada

    PRE: tablero_bien_formado(t) and posicion_en_tablero(pos)

    Args:
        t (Tablero): el tablero en el que se busca la casilla
        pos (Posicion): Posición de la casilla de origen
        d (Direccion): Dirección hacia la que encontramos la casilla vecina

    Returns:
        True si la casilla vecina a pos en dirección d existe y está vacía.
        False si no
    """
    # Obtenemos la posición de la casilla vecina
    posicion_casilla_vecina: Posicion = posicion_vecina_hacia(pos, d)

    # hayCasillaVacia ya verifica de por sí posicion_en_tablero
    return hayCasillaVacia(t, posicion_casilla_vecina)



def hay_pieza_amiga_vecina(t : Tablero, pos : Posicion) -> bool:
    """
    Indica si hay una pieza del mismo color vecina a la pieza en la posición dada

    PRE: tablero_bien_formado(t) and posicion_en_tablero(pos) and hayPieza(t, pos)

    Args:
        t (Tablero): un tablero
        pos (Posicion): posición de la pieza a la que le buscamos una vecina aliada

    Returns:
        True si hay una pieza del mismo color vecina (en una casilla adyacente ortogonalmente)
        False si no
    """
    return hayPiezaAmigaHacia(t, pos, NORTE) or \
            hayPiezaAmigaHacia(t, pos, SUR) or \
            hayPiezaAmigaHacia(t, pos, ESTE) or \
            hayPiezaAmigaHacia(t, pos, OESTE)


def hay_pieza_enemiga_mas_debil_hacia(t : Tablero, pos : Posicion, d : Direccion) -> bool:
    """
    Analiza si en la direccion 'd' hay una figura enemiga mas debil que la pieza de origen (en pos)

    PRE: tablero_bien_formado(t) and posicion_en_tablero(pos) and hayPieza(t, pos)

    Args:
        t (Tablero): un tablero
        pos (Posicion): posicion de la pieza de origen
        d (Direccion): dirección en la cual buscamos una pieza enemiga más debil

    Returns:
        True si la vecina en 'd' existe, es enemiga y tiene menos fuerza que la pieza de origen
        False si no
    """
    pieza_origen: Casilla = casilla_en_posicion(t, pos)
    pos_enemiga: Posicion = posicion_vecina_hacia(pos, d)

    return hayPiezaDeColor(t, pos_enemiga, oponente(pieza_origen.color)) \
        and fuerza(pieza_origen.figura) > fuerza(casilla_en_posicion(t, pos_enemiga).figura)


def hay_pieza_enemiga_mas_fuerte_vecina(t : Tablero, pos : Posicion) -> bool:
    """
    Indica si la pieza de origen (en pos) tiene una figura enemiga vecina más fuerte

    PRE: tablero_bien_formado(t) and posicion_en_tablero(pos) and hayPieza(t, pos)

    Args:
        t (Tablero): un tablero
        pos (Posicion): posicion de la pieza de origen

    Returns:
        True si existe una pieza vecina enemiga, con más fuerza que la pieza de origen
        False si no
    """
    return hayPiezaEnemigaMasFuerteHacia(t, pos, NORTE) or \
            hayPiezaEnemigaMasFuerteHacia(t, pos, SUR) or \
            hayPiezaEnemigaMasFuerteHacia(t, pos, ESTE) or \
            hayPiezaEnemigaMasFuerteHacia(t, pos, OESTE)



def hay_pieza_congelada(t : Tablero, pos : Posicion) -> bool:
    """
    Indica si una pieza esta congelada: existe, tiene un enemigo vecino mas fuerte
    y no tiene una pieza amiga vecina.

    PRE: tablero_bien_formado(t) and posicion_en_tablero(pos)

    Args:
        t (Tablero): un tablero
        pos (Posicion): una posicion

    Returns:
        True si la pieza esta congelada
        False si no
    """
    return hayPieza(t, pos) and hay_pieza_enemiga_mas_fuerte_vecina(t, pos) and not hay_pieza_amiga_vecina(t, pos)


#### Ejercicio 4

### Funciones auxiliares

def direccionDeMovimientoHabilitada(t : Tablero, pos : Posicion, d : Direccion) -> bool:
    """
    Verifica si la pieza en 'pos' tiene permitido moverse en la dirección 'd'.
    La única restricción para la dirección es que los conejos no pueden retroceder:
    los conejos dorados no pueden ir al Sur, y los plateados no al Norte.

    PRE: tablero_bien_formado(t) and posicion_en_tablero(pos) and hayPieza(t, pos)

    Args:
        t (Tablero): un tablero
        pos (Posicion): una posición con una pieza
        d (Direccion): dirección en que se quiere mover

    Returns:
        True si la pieza puede moverse en la dirección 'd'
        False si es un conejo intentando retroceder
    """
    casilla_actual: Casilla = casilla_en_posicion(t, pos)
    f: Figura = casilla_actual.figura
    col: Color = casilla_actual.color

    res: bool = True

    if f == CONEJO and col == DORADO and d == SUR:
        res = False
    elif f == CONEJO and col == PLATEADO and d == NORTE:
        res = False

    return res

def puedeMoverASecas(t : Tablero, pos : Posicion, d : Direccion) -> bool:
    """
    Verifica si una pieza en 'pos' puede moverse a secas en la dirección 'd'
    (es decir, si la casilla vecina en esa dirección está vacía).

    PRE: tablero_bien_formado(t) and posicion_en_tablero(pos)

    Args:
        t (Tablero): un tablero
        pos (Posicion): una posición
        d (Direccion): dirección en que se quiere mover

    Returns:
        True si la casilla vecina en la dirección 'd' está vacía
        False si está ocupada o fuera del tablero
    """
    return hay_casilla_vacia_hacia(t, pos, d)


def puedeArrastrar(t : Tablero, pos : Posicion, d : Direccion, dArrastre: Direccion) -> bool:
    """
    Verifica si la pieza en 'pos' puede arrastrar a un enemigo al moverse
    en la dirección 'd', arrastrándolo en la dirección 'dArrastre'.

    PRE: tablero_bien_formado(t) and posicion_en_tablero(pos) and hayPieza(t, pos)

    Args:
        t (Tablero): un tablero
        pos (Posicion): una posición con una pieza
        d (Direccion): dirección hacia donde se mueve la pieza
        dArrastre (Direccion): dirección hacia donde se arrastra al enemigo

    Returns:
        True si se cumplen ambas condiciones:
            - La casilla vecina en la dirección 'd' está vacía
            - Hay un enemigo más débil en la dirección opuesta a 'dArrastre'
        False si alguna de las condiciones no se cumple
    """
    return hay_casilla_vacia_hacia(t, pos, d) \
        and hay_pieza_enemiga_mas_debil_hacia(t, pos, opuesta(dArrastre))


def puedeEmpujar(t : Tablero, pos : Posicion, d : Direccion, dEmpuje: Direccion) -> bool:

    """
    Verifica si la pieza en 'pos' puede empujar a un enemigo al moverse
    en la dirección 'd', empujándolo en la dirección 'dEmpuje'.

    PRE: tablero_bien_formado(t) and posicion_en_tablero(pos) and hayPieza(t, pos)

    Args:
        t (Tablero): un tablero
        pos (Posicion): una posición con una pieza
        d (Direccion): dirección hacia donde se mueve la pieza (y donde está el enemigo a empujar)
        dEmpuje (Direccion): dirección hacia donde se empuja al enemigo

    Returns:
        True si se cumplen ambas condiciones:
            - Hay un enemigo más débil en la dirección 'd'
            - La casilla detrás del enemigo (en la dirección 'dEmpuje') está vacía
        False si alguna de las condiciones no se cumple
    """
    return hay_pieza_enemiga_mas_debil_hacia(t, pos, d) \
       and hay_casilla_vacia_hacia(t, posicion_vecina_hacia(pos, d), dEmpuje)


def puedeRealizarAccion(t: Tablero, m: Movimiento) -> bool:
    """
    Verifica si la acción descrita en el movimiento 'm' es posible en el tablero 't',
    según el tipo de acción, la posición de origen y la cantidad de pasos.

    PRE: tablero_bien_formado(t) and movimiento_bien_formado(m) and hayPieza(t, m.origen)

    Args:
        t (Tablero): un tablero
        m (Movimiento): movimiento (acción, origen, pasos)

    Returns:
        True si la acción es posible de acuerdo al reglamento
        False si la acción no es posible o no es válida
    """
    res: bool = False

    if m.accion == MOVER_A_SECAS:
        res = puedeMoverASecas(t, m.origen, m.pasos[0])
    elif m.accion == ARRASTRAR:
        res = puedeArrastrar(t, m.origen, m.pasos[0], m.pasos[1])
    # m.accion == EMPUJAR
    else:
        res = puedeEmpujar(t, m.origen, m.pasos[0], m.pasos[1])

    return res

### Problema 4

def puede_realizar_movimiento(j : Juego, m : Movimiento) -> bool:

    """
    Indica si el movimiento 'm' es válido para el juego 'j' en su estado actual.
    Verifica que la pieza sea del turno, que no esté congelada, que la dirección
    esté habilitada, que no se exceda el máximo de pasos y que la acción sea posible.

    PRE: juego_bien_formado(j) and movimiento_bien_formado(m)

    Args:
        j (Juego): un juego (tablero, turno, pasos_consumidos)
        m (Movimiento): movimiento (acción, origen, pasos)

    Returns:
        True si se cumplen todas las condiciones:
            - Hay una pieza del color del turno en 'm.origen'
            - La pieza no está congelada
            - La dirección 'm.pasos[0]' está habilitada para la pieza
            - Los pasos consumidos más los del movimiento no exceden MAX_PASOS
            - La acción (mover a secas, arrastrar o empujar) es posible
        False si alguna de las condiciones no se cumple
    """
    return hay_pieza_de_color(j.tablero, m.origen, j.turno) \
        and not hay_pieza_congelada(j.tablero, m.origen) \
        and direccionDeMovimientoHabilitada(j.tablero, m.origen, m.pasos[0]) \
        and (j.pasos_consumidos + len(m.pasos)) <= MAX_PASOS \
        and puedeRealizarAccion(j.tablero, m)

#### Ejercicio 5

### Funciones auxiliares Ejercicio 5

def copiarTablero(t: Tablero) -> Tablero:
    """
    Devuelve una copia del tablero

    PRE: True

    Args:
        t (Tablero): tablero que se desea copiar

    Returns:
        tablero (Tablero): copia del tablero dado
    """
    tablero_resultante: Tablero = []

    for fila in t:
        nueva_fila: list[Casilla] = []
        for casilla in fila:
            nueva_fila.append(casilla)
        tablero_resultante.append(nueva_fila)
    return tablero_resultante

def trampaDebeVaciarse(t: Tablero, pos_trampa: Posicion) -> bool:
    """
    Indica si la pieza en la trampa pos_trampa debe retirarse: hay una pieza
    y no tiene piezas amigas vecinas.

    PRE: tablero_bien_formado(t) and posicion_en_tablero(pos_trampa)

    Args:
        t (Tablero): tablero
        pos_trampa (Posicion): posición de la trampa

    Returns:
        True si en la posición de la trampa hay una pieza sin piezas amigas vecinas
        False si no hay pieza o tiene amigas vecinas.
    """
    return hayPieza(t, pos_trampa) and not hay_pieza_amiga_vecina(t, pos_trampa)

### Problema 5

def activar_trampas(t : Tablero) -> Tablero:
    """
    Devuelve un nuevo tablero después de activar todas las trampas, siguiendo el orden de
    POSICIONES_TRAMPA.

    PRE: tablero_bien_formado(t)

    Args:
        t (Tablero): tablero sobre el que se activan las trampas.

    Returns:
        tablero (Tablero): tablero con las trampas activadas en las posiciones de POSICIONES_TRAMPA
    """
    tablero_resultante: Tablero = copiarTablero(t)

    pos_trampa: Posicion
    for pos_trampa in POSICIONES_TRAMPA:
        if trampaDebeVaciarse(tablero_resultante, pos_trampa):
            tablero_resultante[pos_trampa.fila][pos_trampa.columna] = VACIA

    return tablero_resultante

#### Ejercicio 6

### Funciones Auxiliares

def trasladarPieza(t: Tablero, origen: Posicion, destino: Posicion) -> None:
    """
    Traslada la pieza de 'origen' a 'destino',
    dejando vacía la posición de origen

    PRE: tablero_bien_formado(t) and hayPieza(t, origen) and hay_casilla_vacia(t, destino)

    Args:
        t (Tablero): tablero que se modifica
        origen (Posicion): posición inicial de la pieza
        destino (Posicion): posición final de la pieza

    Returns:
        None: modifica el tablero recibido.
    """
    t[destino.fila][destino.columna] = t[origen.fila][origen.columna]
    t[origen.fila][origen.columna] = VACIA


def tableroTrasTrasladarPiezas(t: Tablero, m: Movimiento) -> Tablero:
    """
    Devuelve una copia de 't' con las piezas de 'm'
    trasladadas, sin activar las trampas

    PRE: tablero_bien_formado(t) and movimiento_bien_formado(m) and puedeRealizarAccion(t, m) and hayPieza(t, m.origen)

    Args:
        t (Tablero): tablero anterior al movimiento
        m (Movimiento): movimiento que se realiza

    Returns:
        tablero (Tablero): tablero con los traslados realizados
    """
    res: Tablero = copiarTablero(t)
    origen: Posicion = m.origen
    enemiga: Posicion
    destino: Posicion

    if m.accion == MOVER_A_SECAS:
        destino = posicion_vecina_hacia(origen, m.pasos[0])

        trasladarPieza(res, origen, destino)

    elif m.accion == ARRASTRAR:
        destino = posicion_vecina_hacia(origen, m.pasos[0])

        enemiga = posicion_vecina_hacia(origen, opuesta(m.pasos[1]))

        trasladarPieza(res, origen, destino)
        trasladarPieza(res, enemiga, origen)

    # m.accion == EMPUJAR:
    else:
        enemiga = posicion_vecina_hacia(origen, m.pasos[0])

        destino = posicion_vecina_hacia(enemiga, m.pasos[1])

        trasladarPieza(res, enemiga, destino)
        trasladarPieza(res, origen, enemiga)

    return res


def hayQueCambiarDeTurno(j: Juego, m: Movimiento) -> bool:
    """
    Indica si el movimiento completa los pasos
    disponibles en el turno actual

    PRE: True

    Args:
        j (Juego): estado anterior al movimiento
        m (Movimiento): movimiento que se realiza

    Returns:
        True si los pasos consumidos más los pasos del movimiento son exactamente MAX_PASOS
        False si no
    """
    return j.pasos_consumidos + len(m.pasos) == MAX_PASOS

### Problema 6

def realizar_movimiento(j: Juego, m: Movimiento) -> Juego:
    """
    Aplica el movimiento 'm' al juego 'j' y devuelve
    el nuevo estado del juego. Traslada las piezas,
    activa todas las trampas y actualiza los pasos
    consumidos y el turno cuando corresponda.

    PRE: juego_bien_formado(j) and movimiento_bien_formado(m) and puede_realizar_movimiento(j, m)

    Args:
        j (Juego): el juego antes del movimiento
        m (Movimiento): el movimiento que se realiza

    Returns:
        juego (Juego): el estado resultante del juego
    """
    t: Tablero = tableroTrasTrasladarPiezas(j.tablero, m)

    t = activar_trampas(t)

    pasos: int = j.pasos_consumidos + len(m.pasos)

    res: Juego

    if hayQueCambiarDeTurno(j, m):
        res = Juego(t, oponente(j.turno), 0)
    else:
        res = Juego(t, j.turno, pasos)

    return res

#### Ejercicio 7

### Funciones auxiliares Ejercicio 7

def filaInicial(col: Color) -> int:
    """
    Devuelve el número de fila inicial del jugador de color 'col':
    0 para DORADO y la última fila del tablero para PLATEADO.

    PRE: True

    Args:
        col (Color): color del jugador

    Returns:
        0 si col es DORADO
        ALTO - 1 si col es PLATEADO
    """
    fila : int = 0
    if col == PLATEADO:
        fila = ALTO - 1
    return fila

def esInicioDeTurno(j: Juego, col: Color) -> bool:
    """
    Indica si es el inicio del turno para el color indicado.

    PRE: True

    Args:
        j (Juego): un juego
        col (Color): color del jugador a verificar

    Returns:
        True si es el turno de 'col' y no se consumieron pasos
        False si no
    """
    return j.turno == col \
        and j.pasos_consumidos == 0


def hayConejoEnFila(t: Tablero, fila: int, col: Color) -> bool:
    """
    Verifica si hay al menos un conejo del color 'col' en la fila 'fila' del tablero.

    PRE: tablero_bien_formado(t)

    Args:
        t (Tablero): un tablero
        fila (int): número de fila a revisar
        col (Color): color del conejo a buscar

    Returns:
        True si hay al menos un conejo de ese color en esa fila
        False si no
    """
    hay_conejo: bool = False
    columna: int
    for columna in range(ANCHO):
        hay_conejo = hay_conejo or hayFiguraDeColor(t, Posicion(fila, columna), CONEJO, col)
    return hay_conejo


def hayConejoEnTablero(j: Juego, col: Color) -> bool:
    """
    Verifica si hay al menos un conejo del color 'col' en el tablero.

    PRE: juego_bien_formado(j)

    Args:
        j (Juego): un juego
        col (Color): color del conejo a buscar

    Returns:
        True si hay al menos un conejo de ese color en el tablero
        False si no
    """
    hay_conejo: bool = False
    fila: int
    for fila in range(ALTO):
        hay_conejo = hay_conejo or hayConejoEnFila(j.tablero, fila, col)
    return hay_conejo


def hayConejoEnFilaInicialOponente(j: Juego, col: Color) -> bool:
    """
    Verifica si el jugador 'col' tiene un conejo en la fila inicial del oponente.

    PRE: juego_bien_formado(j)

    Args:
        j (Juego): un juego
        col (Color): color del jugador a verificar

    Returns:
        True si hay un conejo de 'col' en la fila inicial del oponente
        False si no
    """
    return hayConejoEnFila(j.tablero, filaInicial(oponente(col)), col)


def reuneCondicionesDeGanar(j: Juego, col: Color) -> bool:
    """
    Indica si el jugador 'col' cumple las condiciones para ganar (sin exclusividad).

    PRE: juego_bien_formado(j)

    Args:
        j (Juego): un juego
        col (Color): color del jugador a verificar

    Returns:
        True si 'col' tiene un conejo en la fila inicial del oponente o si el oponente no tiene conejos
        False si no
    """
    return hayConejoEnFilaInicialOponente(j, col) \
    or not hayConejoEnTablero(j, oponente(col))

def reuneCondicionesDeGanarExclusivas(j: Juego, col: Color) -> bool:
    """
    Indica si el jugador 'col' cumple las condiciones para ganar de forma exclusiva
    (él cumple, pero su oponente no).

    PRE: juego_bien_formado(j)

    Args:
        j (Juego): un juego
        col (Color): color del jugador a verificar

    Returns:
        True si 'col' cumple las condiciones y su oponente no
        False si no
    """
    return reuneCondicionesDeGanar(j, col) and not reuneCondicionesDeGanar(j, oponente(col))

def esJugadorGanador(j: Juego, col: Color) -> bool:
    """
    Determina si el jugador 'col' es el ganador en el estado actual del juego.

    PRE: juego_bien_formado(j)

    Args:
        j (Juego): un juego
        col (Color): color del jugador a verificar

    Returns:
        True si 'col' es el ganador según las reglas del juego
        False si no
    """
    gano_en_su_jugada: bool = esInicioDeTurno(j, oponente(col)) and reuneCondicionesDeGanar(j, col)

    gano_por_jugada_enemiga: bool = esInicioDeTurno(j, col) and reuneCondicionesDeGanarExclusivas(j, col)

    return gano_en_su_jugada or gano_por_jugada_enemiga

### Problema 7

def hay_ganador_determinado(j : Juego) -> bool:
    """
    Indica si hay un ganador determinado en el juego.

    PRE: juego_bien_formado(j)

    Args:
        j (Juego): un juego

    Returns:
        True si alguno de los dos jugadores es ganador
        False si no
    """
    return esJugadorGanador(j, DORADO) or esJugadorGanador(j, PLATEADO)

def ganador_del_juego(j : Juego) -> Color:
    """
    Devuelve el color del jugador ganador del juego.

    PRE: juego_bien_formado(j) and hay_ganador_determinado(j)

    Args:
        j (Juego): un juego con un ganador determinado

    Returns:
        El color del jugador ganador (DORADO o PLATEADO)
    """
    ganador: Color = PLATEADO
    if esJugadorGanador(j, DORADO):
        ganador = DORADO
    return ganador
