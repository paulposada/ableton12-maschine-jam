"""LEDs que reflejan un estado de Live."""
from .config import LED_OFF, LED_ON


def led_value(is_on):
    return LED_ON if is_on else LED_OFF


def _read_state(state):
    """Evalua `state()`; si el objeto de Live ya no existe, el LED se apaga."""
    try:
        return bool(state())
    except (RuntimeError, AttributeError):
        return False


class StateLeds:
    """Botones cuyo LED muestra un estado de Live (Observer por sondeo).

    Live no notifica todos los cambios que nos interesan (vistas, follow...),
    asi que `refresh()` se llama periodicamente. `send_value` no reenvia
    valores repetidos, por lo que refrescar es barato.
    """

    def __init__(self):
        self._bindings = []
        self.paused = False

    def track(self, button, state):
        self._bindings.append((button, state))

    def refresh(self):
        if self.paused:
            return
        for button, state in self._bindings:
            button.send_value(led_value(_read_state(state)))
