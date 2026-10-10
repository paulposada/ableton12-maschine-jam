from functools import partial, wraps

ENABLE_PROFILING = False

if ENABLE_PROFILING:
    import cProfile

    PROFILER = cProfile.Profile()


def profile(fn):
    pass  # docstring stripped in original bytecode

    if ENABLE_PROFILING:

        @wraps(fn)
        def wrapper(self, *a, **k):
            if PROFILER:
                return PROFILER.runcall(partial(fn, self, *a, **k))
            else:
                print('Can not profile (%s), it is probably reloaded' % fn.__name__)
                return fn(*a, **k)

        return wrapper
    else:
        return fn


def dump(name='default'):
    import pstats

    fname = name + '.profile'
    PROFILER.dump_stats(fname)

    def save_human_data(sort):
        s = pstats.Stats(fname, stream=open(f'{fname!s}.{sort!s}.txt', 'w'))
        s.sort_stats(sort)
        s.print_stats()

    save_human_data('time')
    save_human_data('cumulative')
