import time

def timeit(func):
    def wrapped(*args, **kwargs):
        start = time.time()
        ret = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__}: {end - start:.4f}s")
        return ret
    return wrapped
