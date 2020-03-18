from datetime import datetime, timedelta

NO_OF_DAYS_TO_COUNT = 14


def detect(input_data: list):
    date_n_days_ago = datetime.now() - timedelta(days=NO_OF_DAYS_TO_COUNT)
    timestamp_ms_n_days_ago = date_n_days_ago.timestamp() * 1000

    scores = {}
    for data in input_data:
        current_timestamp = data["timestamp"]
        buid = data["buid"]
        signal = data["medRssi"]

        # process only relevant data
        if current_timestamp < timestamp_ms_n_days_ago:
            continue

        # NEW MEETING
        if buid not in scores:
            scores[buid] = {
                "buid": buid,
                "score": get_score(signal),
                "last_timestamp": current_timestamp
            }
            continue

        # add score and update last timestamp
        scores[buid]["score"] += get_score(signal)
        scores[buid]["last_timestamp"] = current_timestamp

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

infected = detect(test_data)
print(infected)
