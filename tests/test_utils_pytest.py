import pytest

from btwa_api.app.api.utils import get_or_404
from fastapi import HTTPException


# return a value
def test_get_or_404():
    assert get_or_404('value') == 'value'


# define my Exception a value
@pytest.fixture
def user():
    return HTTPException(status_code=404, detail='detail')


# return HttpException
def test_get_or_404_2(user):
    try:
        # print('expected = ',user.status_code, user.detail)
        get_or_404(None, 'detail')
    except HTTPException as myex:
        print('exception')
        assert user.status_code == myex.status_code
        assert user.detail == myex.detail
