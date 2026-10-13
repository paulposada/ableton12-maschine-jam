"""Navegacion del browser con los encoders inferiores."""
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent

from . import live_keys, views
from .listeners import ValueListeners
from .navigation import relative_direction


class BrowserNavigationComponent(ControlSurfaceComponent):
    """Cualquier accion le da el foco al browser, asi las perillas responden
    sin tener que hacer click en el."""

    def __init__(self, key_sender, *a, **k):
        super().__init__(*a, **k)
        self._key_sender = key_sender
        self._listeners = ValueListeners()

    def set_controls(self, scroll_encoder, folder_encoder,
                     load_button, preview_button):
        self._listeners.listen(scroll_encoder, self._on_scroll)
        self._listeners.listen(folder_encoder, self._on_folder)
        self._listeners.listen(load_button, self._on_load)
        self._listeners.listen(preview_button, self._on_preview)

    def disconnect(self):
        self._listeners.clear()
        super().disconnect()

    def focus(self):
        views.focus(self.application().view, views.BROWSER)

    def toggle(self):
        app_view = self.application().view
        if views.is_visible(app_view, views.BROWSER):
            app_view.hide_view(views.BROWSER)
        else:
            self.focus()

    def _on_scroll(self, value):
        self._scroll(views.vertical, relative_direction(value))

    def _on_folder(self, value):
        self._scroll(views.horizontal, relative_direction(value))

    def _on_load(self, value):
        self._press_key(value, live_keys.ENTER)

    def _on_preview(self, value):
        # Flecha derecha: en un archivo lo preescucha, en una carpeta la abre
        self._press_key(value, live_keys.RIGHT)

    def _scroll(self, to_nav_direction, direction):
        if self.is_enabled() and direction:
            self.focus()
            self.application().view.scroll_view(
                to_nav_direction(direction), views.BROWSER, False)

    def _press_key(self, value, key):
        if self.is_enabled() and value:
            self.focus()
            self._key_sender.send(key)
