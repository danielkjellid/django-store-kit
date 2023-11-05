import pytest

from store_kit.utils import camelize, decamelize, is_camelcase, is_snakecase


@pytest.mark.parametrize(
    "input_str, output_str",
    (
        ("snake_case_string", "snakeCaseString"),
        ("camelCaseString", "camelCaseString"),
    ),
)
def test_camelize(input_str, output_str) -> None:
    assert camelize(input_str) == output_str


@pytest.mark.parametrize(
    "input_str, output_str",
    (
        ("snake_case_string", "snake_case_string"),
        ("camelCaseString", "camel_case_string"),
    ),
)
def test_decamelize(input_str, output_str) -> None:
    assert decamelize(input_str) == output_str


@pytest.mark.parametrize(
    "input_str, output",
    (
        ("snake_case_string", True),
        ("camelCaseString", False),
    ),
)
def test_is_snakecase(input_str, output):
    assert is_snakecase(input_str) == output


@pytest.mark.parametrize(
    "input_str, output",
    (
        ("snake_case_string", False),
        ("camelCaseString", True),
    ),
)
def test_is_camelcase(input_str, output):
    assert is_camelcase(input_str) == output
