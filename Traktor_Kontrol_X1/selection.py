"""Seleccion de la pista y del device anterior / siguiente."""
from . import views
from .navigation import step_index


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
        """Solo recorre los devices del nivel principal de la pista."""
        song = self._song()
        track = song.view.selected_track
        devices = list(track.devices)
        index = step_index(devices, track.view.selected_device, direction)
        if index is None:
            self._notify(f'X1: la pista "{track.name}" no tiene devices')
            return
        device = devices[index]
        song.view.select_device(device)
        self._application().view.show_view(views.DEVICES)
        self._notify(f'X1 Device: {device.name} ({index + 1}/{len(devices)})')
