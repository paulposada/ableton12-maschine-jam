import Live

from .EncoderElement import EncoderElement
from .InputControlElement import MIDI_NOTE_TYPE


class SliderElement(EncoderElement):
    pass

    def __init__(self, msg_type, channel, identifier, *a, **k):
        super(SliderElement, self).__init__(
            msg_type, channel, identifier, map_mode=Live.MidiMap.MapMode.absolute, *a, **k
        )
