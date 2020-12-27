import time
import functools


def timing_decorator(f):
    @functools.wraps(f)
    def wrapper(instance, *args, **kwargs):
        start_time = time.time()
        return_value = f(instance, *args, **kwargs)
        end_time = time.time()
        print(f'{instance.__class__.__name__} duration: {end_time - start_time} seconds')
        return return_value
    return wrapper
