import pytest
from hypothesis import strategies

from hypothesis_auto import (
    Scenerio,
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
    auto_test(my_function, auto_verify_=lambda test_call: int(test_call.result))

    with pytest.raises(TypeError):
        auto_test(my_function, number_1=strategies.text())

    with pytest.raises(ValueError):
        auto_test(my_raise_function)
    auto_test(my_raise_function, auto_allow_exceptions_=(ValueError,))


auto_pytest_magic(my_function)


def my_custom_verifier(scenerio: Scenerio):
    if scenerio.kwargs["number_1"] > 0 and scenerio.kwargs["number_2"] > 0:
        assert scenerio.result > scenerio.kwargs["number_1"]
        assert scenerio.result > scenerio.kwargs["number_1"]
    elif scenerio.kwargs["number_1"] < 0 and scenerio.kwargs["number_2"] < 0:
        assert scenerio.result < scenerio.kwargs["number_1"]
        assert scenerio.result < scenerio.kwargs["number_1"]
    else:
        assert scenerio.result >= min(scenerio.kwargs.values())
        assert scenerio.result <= max(scenerio.kwargs.values())


auto_pytest_magic(my_function, auto_verify_=my_custom_verifier)


@pytest.mark.parametrize("test_case", auto_test_cases(my_function))
def test_test_case_generation(test_case):
    test_case()


@auto_pytest(my_function)
def test_auto_pytest(test_case):
    test_case()


def test_auto_test_module():
    auto_test_module(example_module)
