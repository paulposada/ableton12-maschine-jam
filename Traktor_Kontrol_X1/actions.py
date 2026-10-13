"""Botones que ejecutan una accion (patron Command) y su LED."""
from .feedback import led_value
from .listeners import ValueListeners


class ActionButtons:
    """Asocia un boton del X1 a una accion sin argumentos.

    LED: si se indica `state` (funcion -> bool) el LED muestra ese estado;
    si no, se enciende mientras el boton esta presionado.
    """

    def __init__(self, elements, state_leds):
        self._elements = elements
        self._state_leds = state_leds
        self._listeners = ValueListeners()

    def bind(self, cc, command, state=None):
        button = self._elements.button(cc)
        if state is None:
            listener = self._momentary_listener(button, command)
        else:
            listener = self._stateful_listener(command)
            self._state_leds.track(button, state)
        self._listeners.listen(button, listener)

    def disconnect(self):
        self._listeners.clear()

    @staticmethod
    def _momentary_listener(button, command):
        def listener(value):
            if value:
                command()
            button.send_value(led_value(value), force=True)
        return listener

    def _stateful_listener(self, command):
        def listener(value):
            if value:
                command()
            self._state_leds.refresh()
        return listener
