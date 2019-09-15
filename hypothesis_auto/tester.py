from typing import Callable, Optional, Tuple, Union, get_type_hints

from hypothesis.strategies import builds
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
    the corresponding *arg or **kwarg.

    All *arg and **kwargs are automatically passed along to hypothesis build to enable this.

    Except for the following options:

    - *_auto_allow_exceptions*: A tuple of exceptions that are acceptable for the function to raise
      and will no be considered a test error.
    - *_auto_runs*: Number of strategies combinations to run the given function against
    - *_auto_verify*: An optional callback function that will be called to allow custom verification
      of the functions return value. The callback function should raise an AssertionError if the
      return value does not match expectations
    """
    return_type = get_type_hints(_auto_function).get("return", None)
    strategy = builds(_auto_function, *args, **kwargs)

    for _ in range(_auto_runs):
        try:
            result = strategy.example()
        except _auto_allow_exceptions:  # type: ignore
            continue

        if return_type:

            class ReturnModel(BaseModel):
                __annotations__ = {"returns": return_type}

            ReturnModel(returns=result)
        if _auto_verify:
            _auto_verify(result)
