def logger(function):
    from functools import wraps
    @wraps(function)
    def wrapper(*args, **kwargs):
        print(f"----- {function.__name__}: start -----")
        output = function(*args, **kwargs)
        print(f"----- {function.__name__}: end -----")
        return output
    return wrapper


def timeit(func):
    import time
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f'{func.__name__} took {end - start:.6f} seconds to complete')
        return result
    return wrapper

def countcall(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.count += 1
        result = func(*args, **kwargs)
        print(f'{func.__name__} has been called {wrapper.count} times')
        return result
    wrapper.count = 0
    return wrapper