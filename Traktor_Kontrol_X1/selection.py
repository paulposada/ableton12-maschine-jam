"""Seleccion de la pista y del device anterior / siguiente."""
from . import views
from .navigation import step_index


def visible_devices(devices):
    """Devices en el orden en que se ven en la cadena de la pista.

    Despues de cada Rack vienen los devices de la cadena que muestra
    desplegada (en un Drum Rack, la del pad seleccionado), a cualquier
    profundidad.
    """
    for device in devices:
        yield device
        yield from visible_devices(_shown_chain_devices(device))


def _shown_chain_devices(device):
    if not device.can_have_chains:
        return ()
    view = device.view
    if not view.is_showing_chain_devices:
        return ()
    chain = view.selected_chain
    return chain.devices if chain else ()


class SelectionNavigator:
    """`song` y `application` devuelven los objetos actuales de Live;
    `notify` muestra un mensaje en la barra de estado."""

    def __init__(self, song, application, notify):
        self._song = song
        self._application = application
        self._notify = notify

    def step_track(self, direction):
        song = self._song()
        tracks = (list(song.visible_tracks) + list(song.return_tracks)
                  + [song.master_track])
        index = step_index(tracks, song.view.selected_track, direction)
        song.view.selected_track = tracks[index]

    def step_device(self, direction):
        song = self._song()
        track = song.view.selected_track
        devices = list(visible_devices(track.devices))
        index = step_index(devices, track.view.selected_device, direction)
        if index is None:
            self._notify(f'X1: la pista "{track.name}" no tiene devices')
            return
        device = devices[index]
        song.view.select_device(device)
        self._application().view.show_view(views.DEVICES)
        self._notify(f'X1 Device: {device.name} ({index + 1}/{len(devices)})')
