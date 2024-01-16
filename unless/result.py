# Copyright (c) 2024 Itz-fork

import traceback

from asyncio import get_event_loop
from inspect import iscoroutinefunction
from typing import Generic, TypeVar, Callable, Any, Optional


T = TypeVar("T")


class Result(Generic[T]):
    """
    You can access following values,

        - `value`: Any - Result returned by the method
        - `error`: Exception - Error raised by the method
        - `handler`: Callable - Handler function
    """

    def __init__(self):
        self.value: Optional[T] = None
        self.error: Optional[Exception] = None
        self.handler: Optional[Callable] = self.__default_handler

    def unless(self, handler: Callable = None, **kwargs):
        """
        Used to handle errors conveniently

        Arguments:
            - handler: Callable (optional) - Handler function (supports both sync and async)
            - kwargs: Any - Arguments to pass to the handler function

        Example:
            ```py
            x.method().unless(lambda e: print(f"Purr: {e}"))
            ```
        """
        # set handler
        if handler:
            self.handler = handler

        # run handler
        if self.error:
            if iscoroutinefunction(self.handler):
                get_event_loop().run_until_complete(self.handler(self.error, **kwargs))
            else:
                self.handler(self.error, **kwargs)

        # return value incase it was set before raising the error
        return self.value

    @classmethod
    def from_func(res, func: Callable[..., T], rtype=Any, *args, **kwargs):
        """
        Used to bring Result to existing functions

        Arguments:
            - `func`: Callable - Function to call
            - `rtype`: Any - Return type of the function
            - `args`: Any - Arguments to pass to the function
            - `kwargs`: Any - Keyword arguments to pass to the function
        """
        to_return = res[rtype]()
        try:
            if iscoroutinefunction(func):
                to_return.value = get_event_loop().run_until_complete(
                    func(*args, **kwargs)
                )
            else:
                to_return.value = func(*args, **kwargs)
        except:
            to_return.error = traceback.format_exc()

        return to_return

    def __default_handler(self, error: Exception):
        "Default error handler"
        print(f"ERROR: {error}")
