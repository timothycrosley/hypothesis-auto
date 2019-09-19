from hypothesis_auto.tester import (
    Scenerio,
    auto_parameters,
    auto_test,
    auto_test_cases,
    auto_test_module,
)

try:
    from hypothesis_auto.pytest import auto_pytest, auto_pytest_magic
except ImportError:  # pragma: no cover
    pass

__version__ = "1.1.0"
