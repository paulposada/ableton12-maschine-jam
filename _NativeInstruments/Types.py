
class TrackType:
    MIDI = 0
    AUDIO = 1
    GROUP = 2
    RETURN = 3
    MASTER = 4
    GENERIC = 5
    EMPTY = 6


class PlayingStatus:
    READY = 0
    TRIGGERED = 1
    PLAYING = 2
    ARMED = 3
    RECORDING = 4
    EMPTY = 5


def typeToString(my_class_num, the_class):
    try:
        return next((k for k, v in the_class.__dict__.items() if v == my_class_num))
    except OSError:
        return 'UNKNOWN'
