"""Modos de las 8 perillas (patron State).

Cada modo sabe conectar y soltar las perillas; el selector solo cambia
cual esta activo. Para agregar un modo nuevo basta con otra clase con
`label`, `attach` y `detach`.
"""


class MacrosMode:
    """Perillas = parametros / macros del device seleccionado."""

    label = 'Macros / parametros del device'

    def __init__(self, device_component):
        self._device = device_component

    def attach(self, knobs):
        self._device.set_parameter_controls(knobs)

    def detach(self):
        self._device.set_parameter_controls(None)


class SendsMode:
    """Perillas = sends A..H de la pista seleccionada."""

    label = 'Sends A-H de la pista seleccionada'

    def __init__(self, mixer_component):
        # El canal "seleccionado" del mixer sigue a la pista seleccionada
        self._strip = mixer_component.selected_strip()

    def attach(self, knobs):
        self._strip.set_send_controls(knobs)

    def detach(self):
        self._strip.set_send_controls(None)


class KnobModeSelector:

    def __init__(self, knobs, modes, notify):
        self._knobs = knobs
        self._modes = modes
        self._notify = notify
        self._active = None

    def select(self, key, announce=True):
        if key == self._active:
            return
        if self._active is not None:
            self._modes[self._active].detach()
        self._active = key
        mode = self._modes[key]
        mode.attach(self._knobs)
        if announce:
            self._notify(f'X1 Perillas: {mode.label}')

    def is_active(self, key):
        return key == self._active
