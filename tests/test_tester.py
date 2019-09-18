import pytest
from hypothesis import strategies

from hypothesis_auto import (
    auto_pytest,
    auto_pytest_magic,
    auto_test,
    auto_test_cases,
    auto_test_module,
)

from . import example_module


def my_function(number_1: int, number_2: int) -> int:
    return number_1 + number_2


def my_raise_function(number_1: int, number_2: int) -> int:
    if number_1 < 0 or number_2 < 0:
        raise ValueError("Negative numbers are not allowed")

    return number_1 + number_2


def test_auto_test():
    auto_test(my_function)
    auto_test(my_function, _auto_verify=lambda result: int(result))

    with pytest.raises(TypeError):
        auto_test(my_function, number_1=strategies.text())

    with pytest.raises(ValueError):
        auto_test(my_raise_function)
    auto_test(my_raise_function, _auto_allow_exceptions=(ValueError,))


auto_pytest_magic(my_function)


@pytest.mark.parametrize("test_case", auto_test_cases(my_function))
def test_test_case_generation(test_case):
    test_case()


@auto_pytest(my_function)
def test_auto_pytest(test_case):
    test_case()


def test_auto_test_module():
    auto_test_module(example_module)
