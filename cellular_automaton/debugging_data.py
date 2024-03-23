import time

time_decorator_data = {}


def time_decorator(frequency=10):
    def decorator(func):
        global time_decorator_data

        def wrapper(*args, **kwargs):
            start = time.time()
            func_name = func.__name__ + ":" + func.__qualname__
            if func_name not in time_decorator_data:
                time_decorator_data[func_name] = -1
            else:
                time_decorator_data[func_name] -= 1

            result = func(*args, **kwargs)

            if time_decorator_data[func_name] < 0:
                print(func_name, "->", (time.time() - start) * 1000, "ms")
                time_decorator_data[func_name] = frequency
            return result

        return wrapper

    return decorator
