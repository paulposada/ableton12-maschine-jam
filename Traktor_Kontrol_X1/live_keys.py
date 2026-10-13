"""Envio de teclas a la ventana de Live.

La API de Live 12 no informa que esta seleccionado en el browser
(BrowserItem.is_selected siempre es False), asi que para cargar se hace lo
mismo que a mano: foco en el browser + tecla. La implementacion depende del
sistema operativo (patron Strategy, con Null Object donde no hay soporte).
"""
import os
import subprocess
import sys

ENTER = '{ENTER}'
RIGHT = '{RIGHT}'
# Atajos de Live 12 (^ = Ctrl, % = Alt). Cada uno muestra / oculta su vista
# sin afectar a la otra; la API solo permite ver una de las dos a la vez.
TOGGLE_CLIP_VIEW = '^%3'     # Ctrl+Alt+3
TOGGLE_DEVICE_VIEW = '^%4'   # Ctrl+Alt+4

_SEND_KEYS_SCRIPT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'send_keys.vbs')
_CREATE_NO_WINDOW = getattr(subprocess, 'CREATE_NO_WINDOW', 0x08000000)


class WindowsKeySender:
    """Usa send_keys.vbs, que activa la ventana de Live por su PID; asi la
    tecla nunca llega a otra aplicacion. `keys` usa la sintaxis de
    WScript.Shell.SendKeys."""

    def __init__(self, report):
        self._report = report

    def send(self, keys):
        command = ['wscript.exe', '//nologo', '//B', _SEND_KEYS_SCRIPT,
                   str(os.getpid()), keys]
        try:
            subprocess.Popen(
                command, creationflags=_CREATE_NO_WINDOW, close_fds=True)
        except OSError as error:
            self._report(f'X1: no se pudo enviar la tecla ({error})')


class UnsupportedKeySender:
    """Sistemas sin implementacion: solo avisa."""

    def __init__(self, report):
        self._report = report

    def send(self, keys):
        self._report('X1: cargar/preescuchar con el push solo funciona '
                     'en Windows')


def create_key_sender(report):
    if sys.platform == 'win32':
        return WindowsKeySender(report)
    return UnsupportedKeySender(report)
