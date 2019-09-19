import inspect
from typing import Any, Callable, Optional, Tuple, Union
from uuid import uuid4

import pytest

from hypothesis_auto.tester import Scenerio, auto_test_cases


def auto_pytest(
    auto_function_: Callable,
    *args,
    auto_allow_exceptions_: Union[Tuple[BaseException], Tuple] = (),
    auto_runs_: int = 50,
    auto_verify_: Optional[Callable] = None,
    **kwargs,
) -> None:
    """A decorator that marks a parameterized pytest function passing along a callable test case.
    The function should take a `test_case` parameter.

    By default auto_pytest uses type annotations to automatically decide on strategies via the
    hypothesis builds strategy. You can override individual strategies by passing them in under
    the corresponding `*arg` or `**kwarg` OR you can pass in specific values that must be used for
    certain parameters while letting others be auto generated.

    All `*arg` and `**kwargs` are automatically passed along to
    `hypothesis.strategies.builds` to enable this. Non strategies are automatically converted
    to strategies using `hypothesis.strategies.just`.

    Except for the following options:

    - *auto_allow_exceptions_*: A tuple of exceptions that are acceptable for the function to raise
      and will no be considered a test error.
    - *auto_runs_*: Number of strategies combinations to run the given function against.
    - *auto_verify_*: An optional callback function that will be called to allow custom verification
      of the functions return value. The callback function should raise an AssertionError if the
      return value does not match expectations.

    Example:

            def my_function(number_1: int, number_2: int) -> int:
                return number_1 + number_2


            @auto_pytest(my_function)
            def test_auto_pytest(test_case):
                test_case()

    -----
    """
    return pytest.mark.parametrize(
        "test_case",
        auto_test_cases(
            auto_function_,
            *args,
            auto_allow_exceptions_=auto_allow_exceptions_,
            auto_limit_=auto_runs_,
            auto_verify_=auto_verify_,
        ),
    )


def auto_pytest_magic(
    auto_function_: Callable,
    *args,
    auto_allow_exceptions_: Union[Tuple[BaseException], Tuple] = (),
    auto_runs_: int = 50,
    auto_verify_: Optional[Callable[[Scenerio], Any]] = None,
    **kwargs,
) -> None:
    """A convenience function that builds a new test function inside the calling module and
    passes into it test cases using the `auto_pytest` decorator. The least effort and most magical
    way to integrate with pytest.

    By default auto_pytest_magic uses type annotations to automatically decide on strategies via the
    hypothesis builds strategy. You can override individual strategies by passing them in under
    the corresponding `*arg` or `**kwarg` OR you can pass in specific values that must be used for
    certain parameters while letting others be auto generated.

    All `*arg` and `**kwargs` are automatically passed along to
    `hypothesis.strategies.builds` to enable this. Non strategies are automatically converted
    to strategies using `hypothesis.strategies.just`.

    Except for the following options:

    - *auto_allow_exceptions_*: A tuple of exceptions that are acceptable for the function to raise
      and will no be considered a test error.
    - *auto_runs_*: Number of strategies combinations to run the given function against.
    - *auto_verify_*: An optional callback function that will be called to allow custom verification
      of the functions return value. The callback function should raise an AssertionError if the
      return value does not match expectations.

    Example:

            def my_function(number_1: int, number_2: int) -> int:
                return number_1 + number_2


            auto_pytest_magic(my_function)
    """
    called_from = inspect.stack()[1]
    module = inspect.getmodule(called_from[0])

    def test_function(test_case):
        test_case()

    uuid = str(uuid4()).replace("-", "")
    test_function.__name__ = f"test_auto_{auto_function_.__name__}_{uuid}"

    setattr(module, test_function.__name__, test_function)

    pytest.mark.parametrize(
        "test_case",
        auto_test_cases(
            auto_function_,
            *args,
            auto_allow_exceptions_=auto_allow_exceptions_,
            auto_limit_=auto_runs_,
            auto_verify_=auto_verify_,
        ),
    )(test_function)
