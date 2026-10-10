pass  # module docstring stripped in original bytecode

from .Util import find_if


class Disconnectable(object):
    pass  # docstring stripped in original bytecode

    def disconnect(self):
        pass


class CompoundDisconnectable(Disconnectable):
    pass  # docstring stripped in original bytecode

    def __init__(self, *a, **k):
        super(CompoundDisconnectable, self).__init__(*a, **k)
        self._registered_disconnectables = []

    def register_disconnectable(self, slot):
        if slot not in self._registered_disconnectables:
            self._registered_disconnectables.append(slot)
        return slot

    def unregister_disconnectable(self, slot):
        if slot in self._registered_disconnectables:
            self._registered_disconnectables.remove(slot)

    def disconnect_disconnectable(self, slot):
        if slot in self._registered_disconnectables:
            self._registered_disconnectables.remove(slot)
            slot.disconnect()

    def find_disconnectable(self, predicate):
        return find_if(predicate, self._registered_disconnectables)

    def has_disconnectable(self, slot):
        return slot in self._registered_disconnectables

    def disconnect(self):
        for slot in self._registered_disconnectables:
            slot.disconnect()
        self._registered_disconnectables = []
        super(CompoundDisconnectable, self).disconnect()


class disconnectable(object):
    pass  # docstring stripped in original bytecode

    def __init__(self, managed=None, *a, **k):
        super(disconnectable, self).__init__(*a, **k)
        self._managed = managed

    def __enter__(self):
        managed = self._managed
        return managed

    def __exit__(self, *a, **k):
        if self._managed is not None:
            self._managed.disconnect()
