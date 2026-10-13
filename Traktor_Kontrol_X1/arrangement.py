"""Zoom y scroll horizontal del Arrangement con los encoders superiores."""
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent

from . import views
from .listeners import ValueListeners
from .navigation import relative_direction


class ArrangementNavigationComponent(ControlSurfaceComponent):

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self._listeners = ValueListeners()

    def set_controls(self, zoom_encoder, scroll_encoder):
        self._listeners.listen(zoom_encoder, self._on_zoom)
        self._listeners.listen(scroll_encoder, self._on_scroll)

    def disconnect(self):
        self._listeners.clear()
        super().disconnect()

    def _on_zoom(self, value):
        # izquierda/derecha = zoom en el tiempo (todo el arrangement);
        # arriba/abajo cambiaria el alto de la pista seleccionada
        direction = relative_direction(value)
        if self._ready(direction):
            self.application().view.zoom_view(
                views.horizontal(direction), views.ARRANGER, False)

    def _on_scroll(self, value):
        direction = relative_direction(value)
        if self._ready(direction):
            self.application().view.scroll_view(
                views.horizontal(direction), views.ARRANGER, False)

    def _ready(self, direction):
        if not (self.is_enabled() and direction):
            return False
        views.focus(self.application().view, views.ARRANGER)
        return True
