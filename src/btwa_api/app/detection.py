from datetime import datetime, timedelta

NO_OF_DAYS_TO_COUNT = 14


def detect(csv_rows: list, now: datetime):
    date_n_days_ago = now - timedelta(days=NO_OF_DAYS_TO_COUNT)
    timestamp_ms_n_days_ago = date_n_days_ago.timestamp() * 1000

    scores = {}
    for row in csv_rows:
        current_timestamp = row["timestamp"]
        buid = row["buid"]
        signal = row["medRssi"]

        # process only relevant data
        if current_timestamp < timestamp_ms_n_days_ago:
            continue

        score = scores.get(buid)

        if score is None:
            # new meeting
            score = {
                "buid": buid,
                "score": get_score(signal),
                "last_timestamp": current_timestamp
            }
        else:
            # already met - add score and update last timestamp
            score["score"] += get_score(signal)
            score["last_timestamp"] = current_timestamp

        scores[buid] = score

    return scores


def get_score(signal):
    if signal <= 70:
        return 35

    if signal <= 75:
        return 25

    if signal <= 80:
        return 17

    if signal <= 85:
        return 10

    if signal <= 90:
        return 5

    return 0


# list of tuples (timestamp_ms, buid, expositionSeconds, maxRssi, avgRssi, medRssi)
test_data = [
    {"timestamp": 1000, "buid": "foo", "expositionSeconds": 1, "maxRssi": 5, "avgRssi": 15, "medRssi": 12},
    {"timestamp": 1000, "buid": "bar", "expositionSeconds": 1, "maxRssi": 5, "avgRssi": 15, "medRssi": 12},
    {"timestamp": 1000, "buid": "baz", "expositionSeconds": 1, "maxRssi": 5, "avgRssi": 15, "medRssi": 12},
    {"timestamp": 1000, "buid": "foo", "expositionSeconds": 1, "maxRssi": 5, "avgRssi": 15, "medRssi": 12},
    {"timestamp": 1000, "buid": "bar", "expositionSeconds": 1, "maxRssi": 5, "avgRssi": 15, "medRssi": 12},
    {"timestamp": 1000, "buid": "baz", "expositionSeconds": 1, "maxRssi": 5, "avgRssi": 15, "medRssi": 12},
]

infected = detect(test_data, datetime.now())
print(infected)
