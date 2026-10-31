"""Puente entre la interfaz web (JS) y la lógica de arimaa.py.
Replica la lógica de selección/movimiento de interfaz.py (versión tkinter)."""
import json
import arimaa as aa

TABLERO_INICIAL = [
    'rrrrrrrr', 'ccddhhme', '--------', '--------',
    '--------', '--------', 'EMHHDDCC', 'RRRRRRRR',
]

juego = None
historia = []
idx = 0
sel = []


def nuevo():
    global juego, historia, idx, sel
    juego = aa.Juego(aa.leer_tablero(TABLERO_INICIAL), aa.DORADO, 0)
    historia = [juego]
    idx = 0
    sel = []


def _registrar():
    global historia, idx, sel
    historia = historia[:idx + 1]
    historia.append(juego)
    idx += 1
    sel = []


def _tratar_de_mover(posiciones, destino):
    global juego
    if len(posiciones) == 1:
        d = aa.direccion_desde_hasta(posiciones[0], destino)
        m = aa.Movimiento(aa.MOVER_A_SECAS, posiciones[0], [d])
    else:
        if aa.son_posiciones_vecinas(posiciones[0], destino):
            posiciones = [posiciones[1], posiciones[0]]
        col0 = aa.casilla_en_posicion(juego.tablero, posiciones[0]).color
        if col0 != juego.turno:
            d = aa.direccion_desde_hasta(posiciones[1], destino)
            d_arr = aa.direccion_desde_hasta(posiciones[0], posiciones[1])
            m = aa.Movimiento(aa.ARRASTRAR, posiciones[1], [d, d_arr])
        else:
            d = aa.direccion_desde_hasta(posiciones[0], posiciones[1])
            d_emp = aa.direccion_desde_hasta(posiciones[1], destino)
            m = aa.Movimiento(aa.EMPUJAR, posiciones[0], [d, d_emp])
    if not aa.hay_ganador_determinado(juego) and aa.puede_realizar_movimiento(juego, m):
        juego = aa.realizar_movimiento(juego, m)
        _registrar()


def click(fila, columna):
    global sel
    pos = aa.Posicion(fila, columna)
    vacia = aa.casilla_en_posicion(juego.tablero, pos) == aa.VACIA
    if len(sel) == 0:
        if not vacia:
            sel = [pos]
    elif len(sel) == 1:
        ultima = sel[-1]
        vecinas = aa.son_posiciones_vecinas(ultima, pos)
        if pos == ultima:
            sel = []
        elif vecinas and vacia:
            _tratar_de_mover(sel, pos)
            sel = []
        elif vecinas and not vacia:
            sel = sel + [pos]
        elif not vacia:
            sel = [pos]
        else:
            sel = []
    else:
        vecinas = aa.son_posiciones_vecinas(sel[0], pos) or aa.son_posiciones_vecinas(sel[1], pos)
        if vecinas and vacia:
            _tratar_de_mover(sel, pos)
            sel = []
        elif not vacia and pos not in sel:
            sel = [pos]
        else:
            sel = []


def undo():
    global juego, idx, sel
    if idx > 0:
        idx -= 1
        juego = historia[idx]
    sel = []


def redo():
    global juego, idx, sel
    if idx < len(historia) - 1:
        idx += 1
        juego = historia[idx]
    sel = []


def pasar():
    global juego
    if juego.pasos_consumidos > 0 and not aa.hay_ganador_determinado(juego):
        juego = aa.pasar_turno(juego)
        _registrar()


def estado():
    hay_ganador = aa.hay_ganador_determinado(juego)
    return json.dumps({
        "tablero": aa.mostrar_tablero(juego.tablero),  # de fila 7 a fila 0
        "turno": str(juego.turno),
        "pasos": aa.MAX_PASOS - juego.pasos_consumidos,
        "sel": [[p.fila, p.columna] for p in sel],
        "trampas": [[p.fila, p.columna] for p in aa.POSICIONES_TRAMPA],
        "undo": idx > 0,
        "redo": idx < len(historia) - 1,
        "pasar": juego.pasos_consumidos > 0 and not hay_ganador,
        "ganador": str(aa.ganador_del_juego(juego)) if hay_ganador else None,
    })

nuevo()
