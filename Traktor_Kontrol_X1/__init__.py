"""Traktor Kontrol X1 MK1 - MIDI Remote Script para Ableton Live 12."""
from .TraktorKontrolX1 import TraktorKontrolX1


def create_instance(c_instance):
    return TraktorKontrolX1(c_instance)
