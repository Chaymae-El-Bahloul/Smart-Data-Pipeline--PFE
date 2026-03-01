THRESHOLD = 25

def select_processing_mode(data: dict) -> str:
    value = data.get("value", 0)

    if value < THRESHOLD:
        print("Mode NORMAL sélectionné")
        return "NORMAL"
    else:
        print("Mode HIGH_LOAD sélectionné (auto-adaptation)")
        return "HIGH_LOAD"

