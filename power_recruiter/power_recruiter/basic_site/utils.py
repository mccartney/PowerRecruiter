import weakref


def multiton(cls):
    """Multiton design pattern.
       Decorated classes must have a get_instance_name static method.
    """
    instances = weakref.WeakValueDictionary()

    def get_instance(*args, **kwargs):
        instance_name = cls.get_instance_name(*args, **kwargs)
        i = instances.get(instance_name)
        if i is None:
            i = instances[instance_name] = cls(*args, **kwargs)
        return i
    return get_instance
