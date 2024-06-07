import threading


class CustomThread(threading.Thread):
    """
    Класс для создания потока, который возвращает значение после завершения.
    """
    __local_result = None

    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None) -> object:
        def new_target(*a, **kwa):
            self.__local_result = target(*a, **kwa)

        super().__init__(group=group, target=new_target, name=name, args=args, kwargs=kwargs, daemon=daemon)

    def join(self, *args) -> None:
        super().join(*args)

    def get_res(self):
        print(self.__local_result)
        return self.__local_result
