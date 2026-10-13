"""Utilidades puras de navegacion (sin dependencias de Live)."""


RELATIVE_CENTER = 64  # Two's Complement: <64 adelante, >64 atras


def relative_direction(value):
    """Two's Complement: 1..63 -> +1, 65..127 -> -1, 0 y 64 -> 0."""
    if 0 < value < RELATIVE_CENTER:
        return 1
    if value > RELATIVE_CENTER:
        return -1
    return 0


def step_index(items, current, direction):
    """Indice del elemento vecino de `current` en `items`, sin salirse.

    Si `current` no esta en la lista empieza por el extremo segun la
    direccion. Devuelve None si la lista esta vacia.
    """
    if not items:
        return None
    last = len(items) - 1
    index = next((i for i, item in enumerate(items) if item == current), None)
    if index is None:
        return 0 if direction > 0 else last
    return max(0, min(last, index + direction))
