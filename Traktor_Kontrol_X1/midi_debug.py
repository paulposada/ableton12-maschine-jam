"""Herramientas de depuracion: escuchar y registrar todo el MIDI entrante."""
import Live

_CC_STATUS = 0xB0
_ALL_CHANNELS = range(16)
_ALL_NUMBERS = range(128)


def forward_everything(script_handle, midi_map_handle, already_forwarded):
    """Pide a Live que reenvie al script todos los CC y notas (16 canales)."""
    for channel in _ALL_CHANNELS:
        for number in _ALL_NUMBERS:
            if (_CC_STATUS | channel, number) not in already_forwarded:
                Live.MidiMap.forward_midi_cc(
                    script_handle, midi_map_handle, channel, number)
            Live.MidiMap.forward_midi_note(
                script_handle, midi_map_handle, channel, number)


def describe(midi_bytes):
    status, number, value = midi_bytes[:3]
    return (f'MIDI IN: status={status & 0xF0} (canal {(status & 0x0F) + 1}) '
            f'cc/nota={number} valor={value}')
