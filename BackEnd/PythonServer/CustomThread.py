import threading


class CustomThread(threading.Thread):
    """
    Класс для создания потока, который возвращает значение после завершения.
    """

    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None):
        def new_target(*a, **kwa):
            self.local_result = target(*a, **kwa)

        super().__init__(group=group, target=new_target, name=name, args=args, kwargs=kwargs, daemon=daemon)

    def join(self, *args):
        super().join(*args)
        return self.local_result
