from btwa_api.app.detection import get_score, detect
from datetime import datetime, timedelta


def test_get_score():
    # if signal <= 70:
    assert get_score(0) == 35
    assert get_score(50) == 35
    assert get_score(70) == 35

    # if signal <= 75:
    assert get_score(74) == 25
    assert get_score(75) == 25

    # if signal <= 80:
    assert get_score(76) == 17
    assert get_score(80) == 17

    # if signal <= 85:
    assert get_score(84) == 10
    assert get_score(85) == 10

    # if signal <= 90:
    assert get_score(88) == 5
    assert get_score(90) == 5

    # else
    assert get_score(91) == 0

    assert get_score(1022261615165151151) == 0
    assert get_score(----1022261615165151151) == 0
    assert get_score(1022261615165151151556565656565665565656) == 0


def test_detect():
    ONE_DAY = 1
    TWO_DAY = 2
    FIFTEEN_DAY = 15

    now = datetime.now()

    date_n_days_ago = now - timedelta(days=ONE_DAY)
    timestamp_ms_n_one_day_ago = date_n_days_ago.timestamp() * 1000

    date_n_days_ago2 = now - timedelta(days=TWO_DAY)
    timestamp_ms_n_one_day_ago2 = date_n_days_ago2.timestamp() * 1000

    date_no_days_to_count = now - timedelta(days=FIFTEEN_DAY)
    timestamp_date_no_days_to_count = date_no_days_to_count.timestamp() * 1000

    # bad data, timestamp is in the past
    bad_data = [
        {"buid": "foo", "timestampStart": 1000, "timestampEnd": 1, "maxRssi": 5, "avgRssi": 15, "medRssi": 12},
    ]

    assert detect(bad_data, now) == {}

    # good data, he met one person
    good_data = [
        {"buid": "foo", "timestampStart": timestamp_ms_n_one_day_ago, "timestampEnd": 1, "maxRssi": 5, "avgRssi": 15,
         "medRssi": 12},
    ]

    assert detect(good_data, now) == {'foo': {'buid': 'foo', 'last_timestamp': timestamp_ms_n_one_day_ago, 'score': 35}}

    # good data, he met one person twice
    good_data2 = [
        {"buid": "foo", "timestampStart": timestamp_ms_n_one_day_ago, "timestampEnd": 1, "maxRssi": 5, "avgRssi": 15,
         "medRssi": 12},
        {"buid": "foo", "timestampStart": timestamp_ms_n_one_day_ago, "timestampEnd": 1, "maxRssi": 5, "avgRssi": 15,
         "medRssi": 70},
    ]

    assert detect(good_data2, now) == {'foo': {'buid': 'foo', 'last_timestamp': timestamp_ms_n_one_day_ago, 'score': 70}}

    # good data, he met two person twice
    good_data3 = [
        {"buid": "foo", "timestampStart": timestamp_ms_n_one_day_ago, "timestampEnd": 1, "maxRssi": 5, "avgRssi": 15,
         "medRssi": 12},
        {"buid": "foo", "timestampStart": timestamp_ms_n_one_day_ago2, "timestampEnd": 1, "maxRssi": 5, "avgRssi": 15,
         "medRssi": 90},
        {"buid": "baz", "timestampStart": timestamp_ms_n_one_day_ago, "timestampEnd": 1, "maxRssi": 5, "avgRssi": 15,
         "medRssi": 80},
        {"buid": "baz", "timestampStart": timestamp_ms_n_one_day_ago, "timestampEnd": 1, "maxRssi": 5, "avgRssi": 15,
         "medRssi": 77},
    ]

    assert detect(good_data3, now) == {'foo': {'buid': 'foo', 'last_timestamp': timestamp_ms_n_one_day_ago2, 'score': 40},
                         'baz': {'buid': 'baz', 'last_timestamp': timestamp_ms_n_one_day_ago, 'score': 34}}

    # good data, he met one person twice and one person also twice but once FIFTEEN_DAY ago
    good_data4 = [
        {"buid": "foo", "timestampStart": timestamp_date_no_days_to_count, "timestampEnd": 1, "maxRssi": 5,
         "avgRssi": 15,
         "medRssi": 12},
        {"buid": "foo", "timestampStart": timestamp_ms_n_one_day_ago2, "timestampEnd": 1, "maxRssi": 5, "avgRssi": 15,
         "medRssi": 90},
        {"buid": "baz", "timestampStart": timestamp_ms_n_one_day_ago, "timestampEnd": 1, "maxRssi": 5, "avgRssi": 15,
         "medRssi": 80},
        {"buid": "baz", "timestampStart": timestamp_ms_n_one_day_ago, "timestampEnd": 1, "maxRssi": 5, "avgRssi": 15,
         "medRssi": 77},
    ]

    assert detect(good_data4, now) == {'foo': {'buid': 'foo', 'last_timestamp': timestamp_ms_n_one_day_ago2, 'score': 5},
                        'baz': {'buid': 'baz', 'last_timestamp': timestamp_ms_n_one_day_ago, 'score': 34}}

    # good data, he met one person twice and one person also twice but twice FIFTEEN_DAY ago
    good_data5 = [
        {"buid": "foo", "timestampStart": timestamp_date_no_days_to_count, "timestampEnd": 1, "maxRssi": 5,
         "avgRssi": 15,
         "medRssi": 12},
        {"buid": "foo", "timestampStart": timestamp_date_no_days_to_count, "timestampEnd": 1, "maxRssi": 5, "avgRssi": 15,
         "medRssi": 90},
        {"buid": "baz", "timestampStart": timestamp_ms_n_one_day_ago, "timestampEnd": 1, "maxRssi": 5, "avgRssi": 15,
         "medRssi": 80},
        {"buid": "baz", "timestampStart": timestamp_ms_n_one_day_ago, "timestampEnd": 1, "maxRssi": 5, "avgRssi": 15,
         "medRssi": 77},
    ]

    assert detect(good_data5, now) == {'baz': {'buid': 'baz', 'last_timestamp': timestamp_ms_n_one_day_ago, 'score': 34}}
