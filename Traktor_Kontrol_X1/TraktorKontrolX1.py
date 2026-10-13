import os
import subprocess
import sys

import Live
from _Framework.ControlSurface import ControlSurface
from _Framework.TransportComponent import TransportComponent
from _Framework.SessionRecordingComponent import SessionRecordingComponent
from _Framework.ButtonElement import ButtonElement
from _Framework.EncoderElement import EncoderElement
from _Framework.InputControlElement import MIDI_CC_TYPE
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.ClipCreator import ClipCreator
from _Framework.ViewControlComponent import ViewControlComponent
from _Framework.DeviceComponent import DeviceComponent

# Canal MIDI del X1 (Live cuenta desde 0: 1 = Canal 2 en el Controller Editor)
CHANNEL = 1

# Modo de los encoders: 1..63 = adelante, 65..127 = atras (Two's Complement en el Controller Editor)
ENCODER_MAP_MODE = Live.MidiMap.MapMode.relative_smooth_two_compliment

# Pon DEBUG_MIDI = True para escribir en Log.txt todo el MIDI que llega (los 16 canales)
DEBUG_MIDI = False

NavDirection = Live.Application.Application.View.NavDirection

# ---------------------------------------------------------------------------
# Mapa de CC del template "Basic" del X1 MK1
#
#   Seccion        Izquierda        Derecha
#   Encoder sup.   16               17
#   FX1 / FX2      20 / 22          21 / 23
#   Encoder inf.   26 (push 24)     27 (push 25)
#   IN / OUT       28 / 30          29 / 31
#   <BEAT / BEAT>  32 / 34          33 / 35
#   CUE / CUP      36 / 38          37 / 39
#   PLAY / SYNC    40 / 42          41 / 43
# ---------------------------------------------------------------------------

# Deck izquierdo: reproducir
CC_PLAY = 40              # PLAY izq.   -> Play / Pausa
CC_METRONOME = 42         # SYNC izq.   -> Metronomo
CC_STOP = 36              # CUE izq.    -> Stop (2 veces = volver al inicio)
CC_TAP_TEMPO = 38         # CUP izq.    -> Tap Tempo
CC_SEEK_BACK = 32         # <BEAT izq.  -> Rebobinar (mantener)
CC_SEEK_FWD = 34          # BEAT> izq.  -> Avanzar (mantener)
CC_LOOP = 28              # IN izq.     -> Loop on/off
CC_FOLLOW = 30            # OUT izq.    -> Follow (la vista sigue la reproduccion)

# Deck derecho: grabar
CC_ARR_RECORD = 41        # PLAY der.   -> Grabar en Arrangement
CC_SESSION_RECORD = 43    # SYNC der.   -> Grabar en Session
CC_AUTOMATION_ARM = 37    # CUE der.    -> Automation Arm
CC_REENABLE_AUTO = 39     # CUP der.    -> Re-enable Automation
CC_UNDO = 33              # <BEAT der.  -> Undo
CC_REDO = 35              # BEAT> der.  -> Redo
CC_CAPTURE_MIDI = 29      # IN der.     -> Capture MIDI
CC_OVERDUB = 31           # OUT der.    -> Arrangement Overdub (MIDI +)

# Botones FX: vistas
CC_VIEW_BROWSER = 20      # FX1 izq.    -> Mostrar / ocultar Browser
CC_VIEW_SESSION_ARR = 22  # FX2 izq.    -> Session <-> Arrangement
CC_VIEW_DETAIL = 21       # FX1 der.    -> Mostrar / ocultar Detail
CC_VIEW_CLIP_DEVICE = 23  # FX2 der.    -> Detail: Clip <-> Devices

# Encoders inferiores: browser
CC_BROWSER_VERTICAL = 26  # Giro izq.   -> Subir / bajar
CC_BROWSER_LOAD = 24      # Push izq.   -> Cargar (o abrir carpeta)
CC_BROWSER_FOLDER = 27    # Giro der.   -> Cerrar / abrir carpeta
CC_BROWSER_PREVIEW = 25   # Push der.   -> Preescuchar

# Encoders superiores: arrangement
CC_ARR_ZOOM = 16          # Giro izq.   -> Zoom
CC_ARR_SCROLL = 17        # Giro der.   -> Mover izquierda / derecha

# Seccion superior: device seleccionado
#   Perillas en orden de lectura (izq->der, arriba->abajo) = parametros 1..8
CC_DEVICE_PARAMS = (0, 1, 2, 3, 4, 5, 6, 7)
#   Botones: columna izquierda = atras, columna derecha = adelante
CC_DEVICE_ON_OFF = 8      # ON izq.     -> Encender / apagar device
CC_TRACK_ARM = 9          # ON der.     -> Armar pista seleccionada
CC_BANK_PREV = 10         # 1 izq.      -> Banco de parametros anterior
CC_BANK_NEXT = 11         # 1 der.      -> Banco de parametros siguiente
CC_DEVICE_PREV = 12       # 2 izq.      -> Device anterior
CC_DEVICE_NEXT = 13       # 2 der.      -> Device siguiente
CC_TRACK_PREV = 14        # 3 izq.      -> Pista anterior
CC_TRACK_NEXT = 15        # 3 der.      -> Pista siguiente


def relative_direction(value):
    """Two's Complement: 1..63 = +1, 65..127 = -1, 0/64 = 0."""
    if 0 < value < 64:
        return 1
    if value > 64:
        return -1
    return 0


SEND_KEYS_SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'send_keys.vbs')


def send_keys_to_live(keys, report=None):
    """Envia teclas a la ventana de Live (solo Windows) con send_keys.vbs.
    El VBS activa la ventana por el PID de Live, asi nunca escribe en otra aplicacion.
    `keys` usa la sintaxis de WScript.Shell.SendKeys ('{ENTER}', '{RIGHT}' = flecha derecha)."""
    if sys.platform != 'win32':
        if report:
            report('X1: cargar/preescuchar con el push solo esta soportado en Windows')
        return
    try:
        subprocess.Popen(
            ['wscript.exe', '//nologo', '//B', SEND_KEYS_SCRIPT, str(os.getpid()), keys],
            creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0x08000000),
            close_fds=True)
    except Exception as e:
        if report:
            report('X1: no se pudo enviar la tecla (%r)' % (e,))


class BrowserNavigationComponent(ControlSurfaceComponent):
    """Navega el browser con los encoders inferiores. Cualquier accion le da el foco al
    browser, asi no hace falta hacer click en el para que respondan las perillas."""

    def __init__(self, *a, **k):
        super(BrowserNavigationComponent, self).__init__(*a, **k)
        self._listeners = []

    def set_controls(self, vertical_encoder, folder_encoder, load_button, preview_button):
        self._listen(vertical_encoder, self._scroll_vertical)
        self._listen(folder_encoder, self._scroll_folder)
        self._listen(load_button, self._load)
        self._listen(preview_button, self._preview)

    def _listen(self, control, callback):
        control.add_value_listener(callback)
        self._listeners.append((control, callback))

    def disconnect(self):
        for control, callback in self._listeners:
            if control.value_has_listener(callback):
                control.remove_value_listener(callback)
        self._listeners = []
        super(BrowserNavigationComponent, self).disconnect()

    def focus_browser(self):
        app_view = self.application().view
        if not app_view.is_view_visible('Browser'):
            app_view.show_view('Browser')
        app_view.focus_view('Browser')

    def _scroll_vertical(self, value):
        direction = relative_direction(value)
        if self.is_enabled() and direction:
            self.focus_browser()
            self.application().view.scroll_view(
                NavDirection.down if direction > 0 else NavDirection.up, 'Browser', False)

    def _scroll_folder(self, value):
        direction = relative_direction(value)
        if self.is_enabled() and direction:
            self.focus_browser()
            self.application().view.scroll_view(
                NavDirection.right if direction > 0 else NavDirection.left, 'Browser', False)

    def _load(self, value):
        if self.is_enabled() and value:
            # La API de Live 12 no informa que esta seleccionado en el browser
            # (BrowserItem.is_selected siempre es False), asi que hacemos lo mismo que a mano:
            # foco en el browser + tecla Enter.
            self.focus_browser()
            send_keys_to_live('{ENTER}', self._report)

    def _preview(self, value):
        if self.is_enabled() and value:
            self.focus_browser()
            # Flecha derecha: en un archivo lo preescucha, en una carpeta la abre
            send_keys_to_live('{RIGHT}', self._report)

    def _report(self, message):
        # Mensaje en la barra de estado de Live y en Log.txt
        surface = self.canonical_parent
        if surface is not None:
            surface.show_message(message)
            surface.log_message(message)


class ArrangementNavigationComponent(ControlSurfaceComponent):
    """Zoom y scroll horizontal del Arrangement con los encoders superiores."""

    def __init__(self, *a, **k):
        super(ArrangementNavigationComponent, self).__init__(*a, **k)
        self._listeners = []

    def set_controls(self, zoom_encoder, scroll_encoder):
        for control, callback in ((zoom_encoder, self._zoom), (scroll_encoder, self._scroll)):
            control.add_value_listener(callback)
            self._listeners.append((control, callback))

    def disconnect(self):
        for control, callback in self._listeners:
            if control.value_has_listener(callback):
                control.remove_value_listener(callback)
        self._listeners = []
        super(ArrangementNavigationComponent, self).disconnect()

    def _focus_arranger(self):
        app_view = self.application().view
        if not app_view.is_view_visible('Arranger'):
            app_view.show_view('Arranger')
        app_view.focus_view('Arranger')

    def _zoom(self, value):
        direction = relative_direction(value)
        if self.is_enabled() and direction:
            self._focus_arranger()
            # izquierda/derecha = zoom horizontal (tiempo, todo el arrangement);
            # arriba/abajo seria el alto de la pista seleccionada
            self.application().view.zoom_view(
                NavDirection.right if direction > 0 else NavDirection.left, 'Arranger', False)

    def _scroll(self, value):
        direction = relative_direction(value)
        if self.is_enabled() and direction:
            self._focus_arranger()
            self.application().view.scroll_view(
                NavDirection.right if direction > 0 else NavDirection.left, 'Arranger', False)


class TraktorKontrolX1(ControlSurface):

    def __init__(self, c_instance):
        super(TraktorKontrolX1, self).__init__(c_instance)
        self._action_listeners = []
        with self.component_guard():
            self._setup_transport()
            self._setup_recording()
            self._setup_actions()
            self._setup_browser()
            self._setup_arrangement()
            self._setup_device()

    # --- Elementos -----------------------------------------------------------

    def _button(self, cc):
        return ButtonElement(True, MIDI_CC_TYPE, CHANNEL, cc)

    def _encoder(self, cc):
        return EncoderElement(MIDI_CC_TYPE, CHANNEL, cc, ENCODER_MAP_MODE)

    def _action_button(self, cc, action):
        """Boton que ejecuta `action()` al presionarse."""
        button = self._button(cc)

        def listener(value):
            if value:
                action()

        button.add_value_listener(listener)
        self._action_listeners.append((button, listener))

    # --- Deck izquierdo: reproducir ------------------------------------------

    def _setup_transport(self):
        # play_toggle_model_transform identidad -> PLAY alterna entre Play y Pausa
        self._transport = TransportComponent(
            play_toggle_model_transform=lambda value: value, name='Transport')
        self._transport.set_play_button(self._button(CC_PLAY))
        self._transport.set_stop_button(self._button(CC_STOP))
        self._transport.set_metronome_button(self._button(CC_METRONOME))
        self._transport.set_tap_tempo_button(self._button(CC_TAP_TEMPO))
        self._transport.set_seek_buttons(self._button(CC_SEEK_FWD), self._button(CC_SEEK_BACK))
        self._transport.set_loop_button(self._button(CC_LOOP))
        self._action_button(CC_FOLLOW, self._toggle_follow)

    # --- Deck derecho: grabar ------------------------------------------------

    def _setup_recording(self):
        # SessionRecordingComponent necesita un ClipCreator y un ViewControlComponent;
        # sin ellos falla en __init__ y Live descarta el script entero.
        self._session_recording = SessionRecordingComponent(
            ClipCreator(), ViewControlComponent(), name='Session_Recording')
        self._transport.set_record_button(self._button(CC_ARR_RECORD))
        self._transport.set_session_record_button(self._button(CC_SESSION_RECORD))
        self._transport.set_arrangement_overdub_button(self._button(CC_OVERDUB))
        self._session_recording.set_automation_button(self._button(CC_AUTOMATION_ARM))
        self._session_recording.set_re_enable_automation_button(self._button(CC_REENABLE_AUTO))
        self._action_button(CC_UNDO, self._undo)
        self._action_button(CC_REDO, self._redo)
        self._action_button(CC_CAPTURE_MIDI, self._capture_midi)

    # --- Botones FX: vistas --------------------------------------------------

    def _setup_actions(self):
        self._action_button(CC_VIEW_BROWSER, self._toggle_browser)
        self._action_button(CC_VIEW_SESSION_ARR, self._toggle_session_arrangement)
        self._action_button(CC_VIEW_DETAIL, self._toggle_detail)
        self._action_button(CC_VIEW_CLIP_DEVICE, self._toggle_clip_device)

    # --- Encoders ------------------------------------------------------------

    def _setup_browser(self):
        self._browser = BrowserNavigationComponent(name='Browser_Navigation')
        self._browser.set_controls(
            self._encoder(CC_BROWSER_VERTICAL),
            self._encoder(CC_BROWSER_FOLDER),
            self._button(CC_BROWSER_LOAD),
            self._button(CC_BROWSER_PREVIEW))

    def _setup_arrangement(self):
        self._arrangement = ArrangementNavigationComponent(name='Arrangement_Navigation')
        self._arrangement.set_controls(self._encoder(CC_ARR_ZOOM), self._encoder(CC_ARR_SCROLL))

    # --- Seccion superior: device seleccionado ------------------------------

    def _setup_device(self):
        # El DeviceComponent sigue al device seleccionado (la "mano azul" de Live)
        self._device = DeviceComponent(
            device_selection_follows_track_selection=True, name='Device')
        self._device.set_parameter_controls(tuple(
            EncoderElement(MIDI_CC_TYPE, CHANNEL, cc, Live.MidiMap.MapMode.absolute)
            for cc in CC_DEVICE_PARAMS))
        self._device.set_on_off_button(self._button(CC_DEVICE_ON_OFF))
        self._device.set_bank_nav_buttons(self._button(CC_BANK_PREV), self._button(CC_BANK_NEXT))
        self.set_device_component(self._device)
        self._action_button(CC_TRACK_ARM, self._toggle_arm)
        self._action_button(CC_DEVICE_PREV, lambda: self._select_device(-1))
        self._action_button(CC_DEVICE_NEXT, lambda: self._select_device(1))
        self._action_button(CC_TRACK_PREV, lambda: self._select_track(-1))
        self._action_button(CC_TRACK_NEXT, lambda: self._select_track(1))

    def _toggle_arm(self):
        track = self.song().view.selected_track
        if track.can_be_armed:
            track.arm = not track.arm

    def _select_device(self, direction):
        app_view = self.application().view
        app_view.show_view('Detail/DeviceChain')
        app_view.scroll_view(
            NavDirection.right if direction > 0 else NavDirection.left, 'Detail/DeviceChain', False)

    def _select_track(self, direction):
        song = self.song()
        tracks = list(song.visible_tracks) + list(song.return_tracks) + [song.master_track]
        current = song.view.selected_track
        index = next((i for i, t in enumerate(tracks) if t == current), 0)
        song.view.selected_track = tracks[max(0, min(len(tracks) - 1, index + direction))]

    # --- Acciones ------------------------------------------------------------

    def _toggle_follow(self):
        self.song().view.follow_song = not self.song().view.follow_song

    def _undo(self):
        if self.song().can_undo:
            self.song().undo()

    def _redo(self):
        if self.song().can_redo:
            self.song().redo()

    def _capture_midi(self):
        if self.song().can_capture_midi:
            self.song().capture_midi()

    def _toggle_browser(self):
        app_view = self.application().view
        if app_view.is_view_visible('Browser'):
            app_view.hide_view('Browser')
        else:
            self._browser.focus_browser()

    def _toggle_session_arrangement(self):
        app_view = self.application().view
        app_view.show_view('Arranger' if app_view.is_view_visible('Session') else 'Session')

    def _toggle_detail(self):
        app_view = self.application().view
        if app_view.is_view_visible('Detail'):
            app_view.hide_view('Detail')
        else:
            app_view.show_view('Detail')

    def _toggle_clip_device(self):
        app_view = self.application().view
        if app_view.is_view_visible('Detail/Clip'):
            app_view.show_view('Detail/DeviceChain')
        else:
            app_view.show_view('Detail/Clip')

    # --- Debug ---------------------------------------------------------------

    def build_midi_map(self, midi_map_handle):
        super(TraktorKontrolX1, self).build_midi_map(midi_map_handle)
        if DEBUG_MIDI:
            # Escuchar TODOS los CC y notas en los 16 canales para ver que envia el X1
            handle = self._c_instance.handle()
            for channel in range(16):
                for number in range(128):
                    if (0xB0 | channel, number) not in self._forwarding_registry:
                        Live.MidiMap.forward_midi_cc(handle, midi_map_handle, channel, number)
                    Live.MidiMap.forward_midi_note(handle, midi_map_handle, channel, number)
            self.log_message('DEBUG: escuchando todos los CC/notas en los 16 canales')

    def receive_midi(self, midi_bytes):
        if DEBUG_MIDI:
            status = midi_bytes[0]
            self.log_message('MIDI IN: status=%d (canal %d) cc/nota=%d valor=%d' % (
                status & 0xF0, (status & 0x0F) + 1, midi_bytes[1], midi_bytes[2]))
        super(TraktorKontrolX1, self).receive_midi(midi_bytes)

    def disconnect(self):
        for button, listener in self._action_listeners:
            if button.value_has_listener(listener):
                button.remove_value_listener(listener)
        self._action_listeners = []
        super(TraktorKontrolX1, self).disconnect()
