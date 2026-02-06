THRESHOLD = 300

def choose_processing_mode(data: dict) -> str:
    """
    Décide du mode de traitement selon la charge
    """
    value = data.get("value", 0)

    if value < THRESHOLD:
        print(" Mode NORMAL sélectionné")
        return "NORMAL"
    else:
        print(" Mode HAUTE CHARGE sélectionné (auto-adaptation)")
        return "HIGH_LOAD"

