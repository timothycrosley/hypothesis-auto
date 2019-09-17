from inspect import isfunction, signature
from types import ModuleType
from typing import Callable, Optional, Tuple, Union, get_type_hints

from hypothesis.strategies import SearchStrategy, builds, just
from pydantic import BaseModel


def auto_test(
    _auto_function: Callable,
    *args,
    _auto_allow_exceptions: Union[Tuple[BaseException], Tuple] = (),
    _auto_runs: int = 50,
    _auto_verify: Optional[Callable] = None,
    **kwargs
) -> None:
    """A simple utility function for hypothesis that enables fully automatic testing for a
    type hinted callable, including return type verification.

    By default auto_test uses type annotations to automatically decide on strategies via the
    hypothesis builds strategy. You can override individual strategies by passing them in under
    the corresponding `*arg` or `**kwarg` OR you can pass in specific values that must be used for
    certain parameters while letting others be auto generated.

    All `*arg` and `**kwargs` are automatically passed along to
    `hypothesis.strategies.builds` to enable this. Non strategies are automatically converted
    to strategies using `hypothesis.strategies.just`.

    Except for the following options:

    - *_auto_allow_exceptions*: A tuple of exceptions that are acceptable for the function to raise
      and will no be considered a test error.
    - *_auto_runs*: Number of strategies combinations to run the given function against.
    - *_auto_verify*: An optional callback function that will be called to allow custom verification
      of the functions return value. The callback function should raise an AssertionError if the
      return value does not match expectations.
    """
    return_type = get_type_hints(_auto_function).get("return", None)

    strategy_args = [arg if isinstance(arg, SearchStrategy) else just(arg) for arg in args]
    strategy_kwargs = {
        name: value if isinstance(value, SearchStrategy) else just(value)
        for name, value in kwargs.items()
    }

    def pass_along_variables(*args, **kwargs):
        return args, kwargs

    pass_along_variables.__signature__ = signature(_auto_function)  # type: ignore
    pass_along_variables.__annotations__ = getattr(_auto_function, "__annotations__", {})
    strategy = builds(pass_along_variables, *strategy_args, **strategy_kwargs)

    for _ in range(_auto_runs):
        args, kwargs = strategy.example()
        try:
            result = _auto_function(*args, **kwargs)
        except _auto_allow_exceptions:  # type: ignore
            continue
        if return_type:

            class ReturnModel(BaseModel):
                __annotations__ = {"returns": return_type}

            ReturnModel(returns=result)
        if _auto_verify:
            _auto_verify(result)


def auto_test_module(module: ModuleType) -> None:
    """Attempts to automatically test every public function within a module."""
    for attribute_name in dir(module):
        if not attribute_name.startswith("_"):
            attribute = getattr(module, attribute_name)
            if isfunction(attribute):
                auto_test(attribute)
