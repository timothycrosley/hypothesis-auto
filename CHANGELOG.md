Install the latest
===================

To install the latest version of hypothesis-auto simply run:

`pip3 install hypothesis-auto`

OR

`poetry add hypothesis-auto`

OR

`pipenv install hypothesis-auto`

Changelog
=========
## 1.1.3 - 30 December 2019

- Added compatibility with latest pydantic release
- Updated to use cruft to keep project structure in sync with latest template

## 1.1.2 - 24 September 2019

- Fixed custom strategies not being passed through for pytest integration methods.

## 1.1.1 - 19 September 2019

- Fixed [Issue #5](https://github.com/timothycrosley/hypothesis-auto/issues/5): typo in Scenario class name

## 1.1.0 - 18 September 2019

!!! danger
    This release contains breaking changes. In particular to how parameters are passed in to testing functions.

- `_prefixing` for parameters was replaced with `suffixing_` to avoid private implication while still avoiding parameter name conflicts.
- Custom `auto_verify_` function now must take a single [`Scenario`](https://timothycrosley.github.io/hypothesis-auto/reference/hypothesis_auto/tester/#scenario) object.

## 1.0.0 - 17 September 2019
- Initial Release.
