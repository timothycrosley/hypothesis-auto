from typing import Callable, Optional, Tuple, Union, get_type_hints

from hypothesis.strategies import builds
from pydantic import create_model


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
    function_model_name = getattr(_auto_function, "__name__", "ReturnVerification")
    strategy = builds(_auto_function, *args, **kwargs)

    for _ in range(_auto_runs):
        try:
            result = strategy.example()
        except _auto_allow_exceptions:  # type: ignore
            continue

        if return_type:
            create_model(function_model_name, returns=return_type)(returns=result)
        if _auto_verify:
            _auto_verify(result)
