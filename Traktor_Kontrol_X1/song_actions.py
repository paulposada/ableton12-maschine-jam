"""Acciones sobre la cancion (cada una, un comando sin argumentos)."""


class SongActions:
    """`song` es una funcion que devuelve el Song actual de Live."""

    def __init__(self, song):
        self._song = song

    # --- Comandos ---------------------------------------------------------

    def undo(self):
        song = self._song()
        if song.can_undo:
            song.undo()

    def redo(self):
        song = self._song()
        if song.can_redo:
            song.redo()

    def capture_midi(self):
        song = self._song()
        if song.can_capture_midi:
            song.capture_midi()

    def toggle_follow(self):
        view = self._song().view
        view.follow_song = not view.follow_song

    def toggle_arm(self):
        track = self._song().view.selected_track
        if track.can_be_armed:
            track.arm = not track.arm

    # --- Estados (para los LEDs) --------------------------------------------

    def is_following(self):
        return self._song().view.follow_song

    def can_capture_midi(self):
        return self._song().can_capture_midi

    def is_selected_track_armed(self):
        track = self._song().view.selected_track
        return track.can_be_armed and track.arm
