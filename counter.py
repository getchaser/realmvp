import json
import os
from datetime import date

DAILY_LIMIT = 200


def check_and_increment() -> bool:
    path = "usage.json"
    today = str(date.today())
    data = json.loads(open(path).read()) if os.path.exists(path) else {}
    count = data.get(today, 0)
    if count >= DAILY_LIMIT:
        return False
    data[today] = count + 1
    with open(path, "w") as f:
        json.dump(data, f)
    return True
