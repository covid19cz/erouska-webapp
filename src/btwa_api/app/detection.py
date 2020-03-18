SCAN_PERIOD = 2 * 60 * 1000  # 2 minutes in milliseconds
BREAK_MEETING_TRESHOLD = 60 * 60 * 1000  # 1 hour in milliseconds
SCORE_DEDUCTION_ON_MEETING_BREAK = 3
INFECTED_SCORE_TRESHOLD = 100


def detect(input_data):
    scores = {}
    for data in input_data:
        current_timestamp = data[0]
        buid = data[1]
        signal = data[5]  # median signal

        # NEW MEETING
        if buid not in scores:
            scores[buid] = {
                "score": get_score(signal),
                "last_timestamp": current_timestamp
            }
            continue

        # ALREADY MET
        # meeting was broken, counting from 0
        if current_timestamp - scores[buid]["last_timestamp"] > BREAK_MEETING_TRESHOLD:
            scores[buid] = {
                "score": get_score(signal),
                "last_timestamp": current_timestamp
            }
            continue

        # every 2 minutes they were apart, reduce score by 3
        i = scores[buid]["last_timestamp"] + SCAN_PERIOD
        while i < current_timestamp:
            scores[buid]["score"] = max(0, scores[buid]["score"] - SCORE_DEDUCTION_ON_MEETING_BREAK)
            i += SCAN_PERIOD

        # add score and update last timestamp
        scores[buid]["score"] += get_score(signal)
        scores[buid]["last_timestamp"] = current_timestamp

    booleanized = decide_infected(scores)

    return booleanized


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


def decide_infected(scores):
    booleanized = []
    for buid in scores:
        booleanized.append({"buid": buid, "infected": scores[buid]["score"] >= INFECTED_SCORE_TRESHOLD})

    return booleanized


# list of tuples (timestamp_ms, buid, expositionSeconds, maxRssi, avgRssi, medRssi)
test_data = [
    (1000, "foo", 1, 5, 15, 12),
    (1000, "bar", 1, 5, 15, 12),
    (1000, "baz", 1, 5, 15, 12),
    (3000, "foo", 1, 5, 15, 12),
    (3000, "bar", 1, 5, 15, 12),
    (3000, "baz", 1, 5, 15, 12),
]

infected = detect(test_data)
print(infected)
