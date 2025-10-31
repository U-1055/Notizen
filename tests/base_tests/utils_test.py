import pytest


@pytest.mark.parametrize(
    ('date', 'format_', 'elements', 'expecting_value'),
    (
        ('25&&06&&12', '%d.%m.%Y', 3, '25.06.0012'),
        ('25.06.2025', '%d.%m.%Y', 3, '25.06.2025'),
        ('25^&*#06^&*#2025', '%d.%m.%Y', 3, '25.06.2025'),
        ('25""""""dwadwa22', '%d.%m.%Y', 3, False),
        ('25//06//2025', '%d.%m.%Y', 3, '25.06.2025')
    )
)
def test_date_format_util(date: str, format_: str, elements: int, expecting_value: str | bool):
    from utils.utils import date_to_format
    result = date_to_format(date, format_, elements)
    assert result == expecting_value, f'Returned value: {result} must be equal to this value: {expecting_value}'


if __name__ == '__main__':
    pass