from _Framework.ClipSlotComponent import ClipSlotComponent
from _Framework.SubjectSlot import subject_slot


class JamClipSlotComponent(ClipSlotComponent):
    """
    Clip Slot Component for Maschine Jam
    """

    _modifier = None

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.__index = (0, 0)

    def set_modifier(self, modifier):
        self._modifier = modifier

    def set_index(self, index):
        self.__index = index

    def get_index(self):
        return self.__index

    def get_track(self):
        if self._clip_slot is not None:
            return self._clip_slot.canonical_parent
        return None

    @subject_slot('value')
    def _launch_button_value(self, value):
        if self.is_enabled():
            if self._modifier and self._modifier.in_spec_mode():
                self._modifier.handle_edit(self, value)
            elif self._clip_slot is not None:
                self._do_launch_clip(value)
        return

    def get_launch_button(self):
        return self._launch_button_value_slot.subject
