from _Framework.SceneComponent import SceneComponent
from _Framework.Util import nop
from .JamClipSlotComponent import JamClipSlotComponent


class JamSceneComponent(SceneComponent):
    """
    Special Scene Component for Maschine
    """

    clip_slot_component_type = JamClipSlotComponent

    def __init__(self, num_slots=0, tracks_to_use_callback=nop, *a, **k):
        super().__init__(num_slots, tracks_to_use_callback, *a, **k)
