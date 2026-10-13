"""Nombres de las vistas de Live y operaciones sobre Application.View."""
import Live

BROWSER = 'Browser'
ARRANGER = 'Arranger'
SESSION = 'Session'
CLIP = 'Detail/Clip'
DEVICES = 'Detail/DeviceChain'

NavDirection = Live.Application.Application.View.NavDirection


def is_visible(app_view, view_name):
    return app_view.is_view_visible(view_name)


def focus(app_view, view_name):
    """Muestra la vista (si hace falta) y le da el foco del teclado."""
    if not app_view.is_view_visible(view_name):
        app_view.show_view(view_name)
    app_view.focus_view(view_name)


def toggle_session_arrangement(app_view):
    target = ARRANGER if app_view.is_view_visible(SESSION) else SESSION
    app_view.show_view(target)


def horizontal(direction):
    return NavDirection.right if direction > 0 else NavDirection.left


def vertical(direction):
    return NavDirection.down if direction > 0 else NavDirection.up
