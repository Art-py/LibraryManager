import pytest

from src.repositories.utils.utils import camel_case_to_snake_case


@pytest.mark.asyncio
async def test_convert_title():
    assert camel_case_to_snake_case('User') == 'user'
    assert camel_case_to_snake_case('UserBook') == 'user_book'
    assert camel_case_to_snake_case('UserBookSame') == 'user_book_same'
