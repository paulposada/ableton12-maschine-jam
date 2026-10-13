"""Configuracion del Traktor Kontrol X1 MK1 (template "Basic").

Mapa fisico de CC (pagina Basic del Controller Editor):

    Seccion          Izquierda        Derecha
    Perillas         0 2 4 6          1 3 5 7
    ON / 1 / 2 / 3   8 / 10 / 12 / 14 9 / 11 / 13 / 15
    Encoder sup.     16               17
    FX1 / FX2        20 / 22          21 / 23
    Encoder inf.     26 (push 24)     27 (push 25)
    IN / OUT         28 / 30          29 / 31
    <BEAT / BEAT>    32 / 34          33 / 35
    CUE / CUP        36 / 38          37 / 39
    PLAY / SYNC      40 / 42          41 / 43

Para reasignar un control basta con cambiar su numero aqui.
"""
import Live

# Canal MIDI del X1. Live cuenta desde 0: 1 = Canal 2 en el Controller Editor.
CHANNEL = 1

# Encoders en Two's Complement: 1..63 = adelante, 65..127 = atras.
RELATIVE_MAP_MODE = Live.MidiMap.MapMode.relative_smooth_two_compliment
ABSOLUTE_MAP_MODE = Live.MidiMap.MapMode.absolute

# True = escribe en Log.txt todo el MIDI que llega (los 16 canales).
DEBUG_MIDI = False

LED_ON = 127
LED_OFF = 0
LED_SWEEP_TICKS = 5  # ~0.5 s encendidos al arrancar


class Transport:
    """Deck izquierdo: reproducir."""

    PLAY = 40        # PLAY   -> Play / Pausa
    METRONOME = 42   # SYNC   -> Metronomo
    STOP = 36        # CUE    -> Stop (2 veces = volver al inicio)
    TAP_TEMPO = 38   # CUP    -> Tap Tempo
    SEEK_BACK = 32   # <BEAT  -> Rebobinar (mantener)
    SEEK_FWD = 34    # BEAT>  -> Avanzar (mantener)
    LOOP = 28        # IN     -> Loop on/off
    FOLLOW = 30      # OUT    -> Follow


class Recording:
    """Deck derecho: grabar."""

    ARRANGEMENT = 41      # PLAY   -> Grabar en Arrangement
    SESSION = 43          # SYNC   -> Grabar en Session
    AUTOMATION_ARM = 37   # CUE    -> Automation Arm
    REENABLE_AUTO = 39    # CUP    -> Re-enable Automation
    UNDO = 33             # <BEAT  -> Undo
    REDO = 35             # BEAT>  -> Redo
    CAPTURE_MIDI = 29     # IN     -> Capture MIDI
    OVERDUB = 31          # OUT    -> Arrangement Overdub


class Views:
    """Botones FX: cada uno muestra / oculta una vista."""

    BROWSER = 20               # FX1 izq.
    SESSION_ARRANGEMENT = 22   # FX2 izq. (alterna)
    CLIP = 21                  # FX1 der.
    DEVICES = 23               # FX2 der.


class Browser:
    """Encoders inferiores."""

    SCROLL = 26    # giro izq. -> subir / bajar
    FOLDER = 27    # giro der. -> cerrar / abrir carpeta
    LOAD = 24      # push izq. -> cargar
    PREVIEW = 25   # push der. -> preescuchar


class Arrangement:
    """Encoders superiores."""

    ZOOM = 16     # zoom horizontal
    SCROLL = 17   # mover izquierda / derecha


class Device:
    """Seccion superior izquierda: device seleccionado."""

    KNOBS = (0, 1, 2, 3, 4, 5, 6, 7)  # orden de lectura
    ON_OFF = 8        # ON izq.
    BANK_PREV = 10    # 1 izq.
    BANK_NEXT = 11    # 1 der.
    PREV = 12         # 2 izq.
    NEXT = 14         # 3 izq.


class Track:
    """Seccion superior derecha: pista seleccionada."""

    ARM = 9      # ON der.
    PREV = 13    # 2 der.
    NEXT = 15    # 3 der.


class KnobModes:
    """Pagina Shift del template: SHIFT + boton ON."""

    MACROS = 52   # SHIFT + ON izq. -> perillas = macros del device
    SENDS = 53    # SHIFT + ON der. -> perillas = sends A..H


# Botones con LED de la pagina Basic (barrido de prueba al arrancar).
LED_CCS = (
    tuple(range(8, 16)) + tuple(range(20, 24)) + tuple(range(28, 44)))
