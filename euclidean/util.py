from collections import deque


def normalize_coefficients(*coefficients):
    """normalize coefficients such that all equivants can be directly compared.

    Raises:
        ValueError: If all coefficients are 0.


    Args:
        *coefficients (List[numbers.Real]):

    Returns:
        (Tuple[numbers.Real]): The equivalent coefficients in normalized form.
    """
    divisor = 0
    normalized = deque()
    for c in reversed(coefficients):
        if divisor:
            normalized.appendleft(c / divisor)
        elif c != 0:
            divisor = c
            normalized.appendleft(1)
        else:
            normalized.appendleft(0)

    if divisor == 0:
        raise ValueError("All coefficients are 0.")

    return tuple(normalized)


def methods(*meths):
    """A decorator for attaching generic methods to a class.

    Args:
        *meths:

    Returns:

    """

    def decorator(cls):
        for meth in meths:
            setattr(cls, meth.__name__, meth)
        return cls

    return decorator
