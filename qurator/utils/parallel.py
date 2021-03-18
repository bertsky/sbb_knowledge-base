from multiprocessing import Pool, get_context
import gc


def run(tasks, method='fork', **kwargs):

    if 'processes' in kwargs:

        if kwargs['processes'] == 0:

            if 'initializer' in kwargs:

                if 'initargs' in kwargs:
                    kwargs['initializer'](*kwargs['initargs'])
                else:
                    kwargs['initializer']()

            for ta in tasks:
                ret = ta()

                yield ret

                del ret
                del ta

            return

    def run_in_pool(pool):
        for it, result in enumerate(pool.imap(_run, tasks)):

            yield result

            del result

            if it % 1000 == 0:
                gc.collect()

    if method == 'spawn':
        with get_context('spawn').Pool(**kwargs) as _pool:
            run_in_pool(_pool)
    else:
        with Pool(**kwargs) as _pool:
            run_in_pool(_pool)


def run_unordered(tasks, **kwargs):

    if 'processes' in kwargs:

        if kwargs['processes'] == 0:

            if 'initializer' in kwargs:

                if 'initargs' in kwargs:
                    kwargs['initializer'](*kwargs['initargs'])
                else:
                    kwargs['initializer']()

            for ta in tasks:
                ret = ta()

                yield ret

                del ret
                del ta

            return

    with Pool(**kwargs) as pool:

        for it, result in enumerate(pool.imap_unordered(_run, tasks)):

            yield result

            del result

            if it % 1000 == 0:
                gc.collect()


def _run(t):

    if t is None:
        return None

    ret = t()

    del t

    return ret

