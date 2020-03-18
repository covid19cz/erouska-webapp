from src.btwa_api.app.detection import get_score


def test_get_score():
    # if signal <= 70:
    assert get_score(0) == 35;
    assert get_score(50) == 35;
    assert get_score(70) == 35;

    # if signal <= 75:
    assert get_score(74) == 25;
    assert get_score(75) == 25;

    # if signal <= 80:
    assert get_score(76) == 17;
    assert get_score(80) == 17;

    # if signal <= 85:
    assert get_score(84) == 10;
    assert get_score(85) == 10;

    # if signal <= 90:
    assert get_score(88) == 5;
    assert get_score(90) == 5;

    # else
    assert get_score(91) == 0;
    # assert get_score('test') != 0;

    assert get_score(1022261615165151151) == 0;
    assert get_score(----1022261615165151151) == 0;
    assert get_score(1022261615165151151556565656565665565656) == 0;