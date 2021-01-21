from time import time, gmtime

def string_from_epoh(seconds):
    if seconds > 60:
        seconds = gmtime(seconds)
        seconds, hours, minutes = seconds.tm_sec, seconds.tm_hour, seconds.tm_min
        return f'{hours:02d}:{minutes:02d}:{seconds:02d}'
    else:
        return f'{round(seconds, 3)} seconds'

def time_taken(function):
    """Computes the total time taken for a function to complete and prints it out
    use as a decorator:
        ```
        @time_taken_seconds
        def foo():
            ...
        ```

    Args:
        function (function): Timered function
    """
    def func_wrapper(*args, **kwargs):
        start_time = time()
        function(*args, **kwargs)
        end_time = time()

        elapsed = end_time - start_time

        print(f'Function "{function.__name__}()"   |   Elapsed {string_from_epoh(elapsed)}')

    return func_wrapper

