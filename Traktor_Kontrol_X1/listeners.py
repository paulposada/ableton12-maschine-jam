"""Registro de value listeners, para quitarlos todos al desconectar."""


class ValueListeners:
    """Agrupa los value listeners de varios controles."""

    def __init__(self):
        self._bindings = []

    def listen(self, control, callback):
        control.add_value_listener(callback)
        self._bindings.append((control, callback))

    def clear(self):
        for control, callback in self._bindings:
            if control.value_has_listener(callback):
                control.remove_value_listener(callback)
        self._bindings = []
