# 1
# events = [
#     {"event_id": "e1", "payload": {"attempt": 1}}
# ]

# copied = events.copy()
# copied[0]["payload"]["attempt"] = 2
# copied.append({"event_id": "e2", "payload": {}})

# print(len(events))
# print(events[0]["payload"]["attempt"])

# 2
# - event_id가 비어 있지 않은 문자열이면 정상입니다.
# - (정상 목록, 오류 목록)을 반환하세요.
# - 오류 목록에는 원본 행과 오류 이유를 함께 담으세요. 구조는 직접 정하세요.
# - 입력을 변경하지 않고, 빈 입력도 처리하세요.
# - 정상·오류·빈 입력을 확인하는 assert를 각각 하나 이상 작성하세요.
rows = [
    {"event_id": "e1", "event_type": "SESSION_STARTED"},
    {"event_type": "SEAT_VIEWED"},
    {"event_id": "", "event_type": "SESSION_ENDED"},
    {"event_id": "e2", "event_type": "SEAT_VIEWED"},
]

def split_events(rows):
    valid_events = []
    error_events = []
    for row in rows:
      event_id = row.get("event_id")
      if isinstance(event_id, str) and event_id != "":
        valid_events.append(row)
      else:
        error_events.append({"row": row, "error": "event_id is empty or not a string"})
    return valid_events, error_events

valid, errors = split_events(rows)
print(valid)
print(errors)
assert len(valid) == 2, "There should be 2 valid events"
assert len(errors) == 2, "There should be 2 error events"

empty_valid, empty_errors = split_events([])

assert empty_valid == [], "Valid events should be empty"
assert empty_errors == [], "Error events should be empty" 