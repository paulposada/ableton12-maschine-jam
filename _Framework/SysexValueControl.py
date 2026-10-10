from .InputControlElement import MIDI_SYSEX_TYPE, InputControlElement


class SysexValueControl(InputControlElement):
    ...
    ...

    def __init__(self, message_prefix=None, value_enquiry=None, default_value=None, *a, **k):
        super(SysexValueControl, self).__init__(msg_type=MIDI_SYSEX_TYPE, sysex_identifier=message_prefix, *a, **k)
        self._value_enquiry = value_enquiry
        self._default_value = default_value

    def send_value(self, value_bytes):
        self.send_midi(self.message_sysex_identifier() + value_bytes + (247,))

    def enquire_value(self):
        self.send_midi(self._value_enquiry)

    def reset(self):
        if self._default_value != None:
            self.send_value(self._default_value)
