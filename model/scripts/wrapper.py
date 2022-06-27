import time


def timer(func):
    """
    Decorator para mostrar o tempo de execução de uma função.

    Args:
        func (callable): A função a ser decorada.

    Returns:
        callable: A função decorada.
    """

    def wrapper(*args, **kwargs):
        t_start = time.time()
        result = func(*args, **kwargs)
        t_total = time.time() - t_start
        print('{} levou {}s'.format(func.__name__, t_total))
        return result
    return wrapper
