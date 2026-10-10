
from .ControlElement import ControlElement
from .SubjectSlot import Subject, SubjectEvent


class NotifyingControlElement(Subject, ControlElement):
    pass
    __subject_events__ = (
        SubjectEvent(
            name='value',
            doc=' Called when the control element receives a MIDI value\n                             from the hardware '),)
