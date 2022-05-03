def to_int(data) -> int:
    try:
        return int(data)
    except Exception:
        return data


def to_float(data) -> float:
    try:
        return float(data)
    except Exception:
        return 0
