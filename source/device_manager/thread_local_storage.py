import threading

__storage = threading.local()


def get_storage():
    val = getattr(__storage, 'val', None)
    if val is None:
        __storage.val = {}
    return __storage.val
