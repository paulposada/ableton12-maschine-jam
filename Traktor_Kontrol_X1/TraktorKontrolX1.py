"""Control Surface de Ableton Live 12 para el Traktor Kontrol X1 MK1.

Esta clase solo ensambla las piezas (composition root): cada seccion del
controlador se configura en su propio metodo `_setup_*`, y la logica vive
en los modulos del paquete.
"""
from _Framework.ClipCreator import ClipCreator
from _Framework.ControlSurface import ControlSurface
from _Framework.DeviceComponent import DeviceComponent
from _Framework.MixerComponent import MixerComponent
from _Framework.SessionRecordingComponent import SessionRecordingComponent
from _Framework.TransportComponent import TransportComponent
from _Framework.ViewControlComponent import ViewControlComponent

from . import config, live_keys, midi_debug, views
from .actions import ActionButtons
from .arrangement import ArrangementNavigationComponent
from .browser import BrowserNavigationComponent
from .config import (Arrangement, Browser, Device, KnobModes, Recording,
                     Track, Transport, Views)
from .elements import ElementFactory
from .feedback import StateLeds
from .knob_modes import KnobModeSelector, MacrosMode, SendsMode
from .live_keys import create_key_sender
from .selection import SelectionNavigator
from .song_actions import SongActions


class TraktorKontrolX1(ControlSurface):

    _state_leds = None  # update_display puede llegar antes de __init__

    def __init__(self, c_instance):
        super().__init__(c_instance)
        self._elements = ElementFactory(config.CHANNEL)
        self._state_leds = StateLeds()
        self._actions = ActionButtons(self._elements, self._state_leds)
        self._song_actions = SongActions(self.song)
        self._key_sender = create_key_sender(self._report)
        self._selection = SelectionNavigator(
            self.song, self.application, self.show_message)
        with self.component_guard():
            self._setup_transport()
            self._setup_recording()
            self._setup_browser()
            self._setup_views()
            self._setup_arrangement()
            self._setup_device()
            self._setup_knob_modes()
            self._setup_track()
        self._start_led_sweep()

    # --- Deck izquierdo: reproducir ------------------------------------------

    def _setup_transport(self):
        button = self._elements.button
        # Modelo identidad: PLAY alterna entre Play y Pausa
        self._transport = TransportComponent(
            play_toggle_model_transform=lambda value: value, name='Transport')
        self._transport.set_play_button(button(Transport.PLAY))
        self._transport.set_stop_button(button(Transport.STOP))
        self._transport.set_metronome_button(button(Transport.METRONOME))
        self._transport.set_tap_tempo_button(button(Transport.TAP_TEMPO))
        self._transport.set_seek_buttons(
            button(Transport.SEEK_FWD), button(Transport.SEEK_BACK))
        self._transport.set_loop_button(button(Transport.LOOP))
        self._actions.bind(Transport.FOLLOW, self._song_actions.toggle_follow,
                           state=self._song_actions.is_following)

    # --- Deck derecho: grabar ------------------------------------------------

    def _setup_recording(self):
        button = self._elements.button
        # Necesita ClipCreator y ViewControlComponent: sin ellos falla en
        # __init__ y Live descarta el script entero.
        recording = SessionRecordingComponent(
            ClipCreator(), ViewControlComponent(), name='Session_Recording')
        recording.set_automation_button(button(Recording.AUTOMATION_ARM))
        recording.set_re_enable_automation_button(
            button(Recording.REENABLE_AUTO))
        self._transport.set_record_button(button(Recording.ARRANGEMENT))
        self._transport.set_session_record_button(button(Recording.SESSION))
        self._transport.set_arrangement_overdub_button(
            button(Recording.OVERDUB))
        self._actions.bind(Recording.UNDO, self._song_actions.undo)
        self._actions.bind(Recording.REDO, self._song_actions.redo)
        self._actions.bind(Recording.CAPTURE_MIDI,
                           self._song_actions.capture_midi,
                           state=self._song_actions.can_capture_midi)

    # --- Encoders inferiores: browser ----------------------------------------

    def _setup_browser(self):
        self._browser = BrowserNavigationComponent(
            self._key_sender, name='Browser_Navigation')
        self._browser.set_controls(
            self._elements.encoder(Browser.SCROLL),
            self._elements.encoder(Browser.FOLDER),
            self._elements.button(Browser.LOAD),
            self._elements.button(Browser.PREVIEW))

    # --- Botones FX: vistas --------------------------------------------------

    def _setup_views(self):
        self._actions.bind(Views.BROWSER, self._browser.toggle,
                           state=self._view_state(views.BROWSER))
        self._actions.bind(Views.SESSION_ARRANGEMENT,
                           self._toggle_session_arrangement,
                           state=self._view_state(views.ARRANGER))
        # Clip y Devices se alternan con los atajos de Live 12: la API solo
        # deja ver una de las dos vistas a la vez
        self._actions.bind(Views.CLIP,
                           self._shortcut(live_keys.TOGGLE_CLIP_VIEW),
                           state=self._view_state(views.CLIP))
        self._actions.bind(Views.DEVICES,
                           self._shortcut(live_keys.TOGGLE_DEVICE_VIEW),
                           state=self._view_state(views.DEVICES))

    def _toggle_session_arrangement(self):
        views.toggle_session_arrangement(self.application().view)

    def _shortcut(self, keys):
        return lambda: self._key_sender.send(keys)

    def _view_state(self, view_name):
        return lambda: views.is_visible(self.application().view, view_name)

    # --- Encoders superiores: arrangement ------------------------------------

    def _setup_arrangement(self):
        self._arrangement = ArrangementNavigationComponent(
            name='Arrangement_Navigation')
        self._arrangement.set_controls(
            self._elements.encoder(Arrangement.ZOOM),
            self._elements.encoder(Arrangement.SCROLL))

    # --- Seccion superior izquierda: device ----------------------------------

    def _setup_device(self):
        button = self._elements.button
        # Sigue al device seleccionado (la "mano azul" de Live)
        self._device = DeviceComponent(
            device_selection_follows_track_selection=True, name='Device')
        self._device.set_on_off_button(button(Device.ON_OFF))
        self._device.set_bank_nav_buttons(
            button(Device.BANK_PREV), button(Device.BANK_NEXT))
        self.set_device_component(self._device)
        self._actions.bind(Device.PREV,
                           lambda: self._selection.step_device(-1))
        self._actions.bind(Device.NEXT,
                           lambda: self._selection.step_device(1))

    # --- Perillas: macros / sends --------------------------------------------

    def _setup_knob_modes(self):
        knobs = tuple(self._elements.knob(cc) for cc in Device.KNOBS)
        modes = {
            KnobModes.MACROS: MacrosMode(self._device),
            KnobModes.SENDS: SendsMode(MixerComponent(name='Mixer')),
        }
        self._knob_modes = KnobModeSelector(knobs, modes, self.show_message)
        self._knob_modes.select(KnobModes.MACROS, announce=False)
        for cc in modes:
            self._actions.bind(cc, self._knob_mode_selector(cc),
                               state=self._knob_mode_state(cc))

    def _knob_mode_selector(self, key):
        return lambda: self._knob_modes.select(key)

    def _knob_mode_state(self, key):
        return lambda: self._knob_modes.is_active(key)

    # --- Seccion superior derecha: pista -------------------------------------

    def _setup_track(self):
        self._actions.bind(Track.ARM, self._song_actions.toggle_arm,
                           state=self._song_actions.is_selected_track_armed)
        self._actions.bind(Track.PREV, lambda: self._selection.step_track(-1))
        self._actions.bind(Track.NEXT, lambda: self._selection.step_track(1))

    # --- LEDs ----------------------------------------------------------------

    def update_display(self):
        # Live la llama ~10 veces por segundo: mantiene los LEDs de estado al
        # dia aunque el cambio se haga con el mouse
        super().update_display()
        if self._state_leds is not None:
            with self.component_guard():
                self._state_leds.refresh()

    def _start_led_sweep(self):
        """Enciende todos los LEDs ~0.5 s: prueba visual de que el X1 recibe
        el feedback. Luego se restaura el estado real de cada boton."""
        self._state_leds.paused = True
        self._send_to_all_leds(config.LED_ON)
        self.schedule_message(config.LED_SWEEP_TICKS, self._end_led_sweep)

    def _end_led_sweep(self):
        self._send_to_all_leds(config.LED_OFF)
        self._state_leds.paused = False
        self.refresh_state()
        self._state_leds.refresh()

    def _send_to_all_leds(self, value):
        status = 0xB0 | config.CHANNEL
        for cc in config.LED_CCS:
            self._send_midi((status, cc, value))

    # --- Mensajes y depuracion -----------------------------------------------

    def _report(self, message):
        """Barra de estado de Live + Log.txt."""
        self.show_message(message)
        self.log_message(message)

    def build_midi_map(self, midi_map_handle):
        super().build_midi_map(midi_map_handle)
        if config.DEBUG_MIDI:
            midi_debug.forward_everything(
                self._c_instance.handle(), midi_map_handle,
                self._forwarding_registry)
            self.log_message('DEBUG: escuchando todo el MIDI (16 canales)')

    def receive_midi(self, midi_bytes):
        if config.DEBUG_MIDI:
            self.log_message(midi_debug.describe(midi_bytes))
        super().receive_midi(midi_bytes)

    def disconnect(self):
        self._actions.disconnect()
        super().disconnect()
