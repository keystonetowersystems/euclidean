def methods(*meths):
    def decorator(cls):
        for meth in meths:
            setattr(cls, meth.__name__, meth)
        return cls

    return decorator
