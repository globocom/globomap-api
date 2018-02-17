import functools


def permission_classes(permission_classes):
    def outer(func):
        @functools.wraps(func)
        def inner(self, *args, **kwargs):
            for permission_class in permission_classes:
                permission_class()
            return func(self, *args, **kwargs)
        return inner
    return outer
