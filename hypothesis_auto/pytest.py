import inspect
from typing import Callable, Optional, Tuple, Union
from uuid import uuid4

import pytest

from hypothesis_auto.tester import auto_test_cases


def auto_pytest(
    _auto_function: Callable,
    *args,
    _auto_allow_exceptions: Union[Tuple[BaseException], Tuple] = (),
    _auto_runs: int = 50,
    _auto_verify: Optional[Callable] = None,
    **kwargs,
) -> None:
    return pytest.mark.parametrize(
        "test_case",
        auto_test_cases(
            _auto_function,
            *args,
            _auto_allow_exceptions=_auto_allow_exceptions,
            _auto_limit=_auto_runs,
            _auto_verify=_auto_verify,
        ),
    )


def auto_pytest_magic(
    _auto_function: Callable,
    *args,
    _auto_allow_exceptions: Union[Tuple[BaseException], Tuple] = (),
    _auto_runs: int = 50,
    _auto_verify: Optional[Callable] = None,
    **kwargs,
) -> None:
    called_from = inspect.stack()[1]
    module = inspect.getmodule(called_from[0])

    def test_function(test_case):
        test_case()

    uuid = str(uuid4()).replace("-", "")
    test_function.__name__ = f"test_auto_{_auto_function.__name__}_{uuid}"

    setattr(module, test_function.__name__, test_function)

    pytest.mark.parametrize(
        "test_case",
        auto_test_cases(
            _auto_function,
            *args,
            _auto_allow_exceptions=_auto_allow_exceptions,
            _auto_limit=_auto_runs,
            _auto_verify=_auto_verify,
        ),
    )(test_function)
