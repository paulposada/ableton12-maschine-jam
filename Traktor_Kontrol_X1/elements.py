"""Fabrica de elementos MIDI del X1 (todos en el mismo canal)."""
from _Framework.ButtonElement import ButtonElement
from _Framework.EncoderElement import EncoderElement
from _Framework.InputControlElement import MIDI_CC_TYPE

from .config import ABSOLUTE_MAP_MODE, RELATIVE_MAP_MODE


class ElementFactory:
    """Crea los controles del X1 con el canal y los modos correctos."""

    def __init__(self, channel):
        self._channel = channel

    def button(self, cc):
        """Boton momentaneo (Gate: 127 al presionar, 0 al soltar)."""
        return ButtonElement(True, MIDI_CC_TYPE, self._channel, cc)

    def encoder(self, cc):
        """Encoder sin fin en modo relativo (Two's Complement)."""
        return EncoderElement(
            MIDI_CC_TYPE, self._channel, cc, RELATIVE_MAP_MODE)

    def knob(self, cc):
        """Perilla con recorrido absoluto (0..127)."""
        return EncoderElement(
            MIDI_CC_TYPE, self._channel, cc, ABSOLUTE_MAP_MODE)
