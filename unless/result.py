# Copyright (c) 2024 Itz-fork

import functools
import types
import logging
import traceback

from asyncio import get_event_loop
from typing import Generic, Tuple, Type, TypeVar, Callable, Any, Optional, Union


T = TypeVar("T")


class Result(Generic[T]):
    """
    You can access following values,

        - `value`: Any - Result returned by the method
        - `error`: Exception - Error raised by the method
        - `handler`: Callable - Handler function
    """

    __slots__ = ("value", "error", "handler")

    def __init__(self):
        self.value: Optional[T] = None
        self.error: Optional[
            Union[Tuple[Optional[Type[BaseException]], Optional[str]], str]
        ] = (None, None)
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
        self.handler = handler or self.handler

        # run handler
        if self.error:
            if isinstance(self.handler, types.CoroutineType):
                get_event_loop().run_until_complete(self.handler(self.error, **kwargs))
            else:
                self.handler(self.error, **kwargs)

        # return value incase it was set before raising the error
        return self.value

    @classmethod
    def from_func(cls, func: Callable[..., T] = None, rtype=Any, *args, **kwargs):
        """
        Used to integrate Result to existing functions

        Arguments:
            - `func`: Callable - Function to call
            - `rtype`: Any - Return type of the function
            - `args`: Any - Arguments to pass to the function
            - `kwargs`: Any - Keyword arguments to pass to the function
        """

        # for non-decorators
        if func is None:
            return functools.partial(cls.from_func, rtype=rtype, *args, **kwargs)

        to_return = cls[rtype]()

        def fn_wrapper(*fargs, **fkwargs):  # goofy ahh
            try:
                if isinstance(func, types.CoroutineType):
                    to_return.value = get_event_loop().run_until_complete(
                        func(*fargs, **fkwargs)
                    )
                else:
                    to_return.value = func(*fargs, **fkwargs)
            except Exception as e:
                to_return.error = type(e), traceback.format_exc()

            return to_return

        if args or kwargs:
            return fn_wrapper(*args, **kwargs)
        else:
            return fn_wrapper

    def __default_handler(self, error: Exception):
        "Default error handler"
        logging.error(f"ERROR: {error}")
