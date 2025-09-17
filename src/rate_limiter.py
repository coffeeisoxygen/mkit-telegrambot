import time


def is_rate_limited(uid: int, limit: int = 5, window: int = 60) -> bool:
    """Cek apakah user melebihi quota dalam sliding window"""
    now = time.time()
    res = db.search(UserQ.user_id == uid)

    if not res:
        db.insert({"user_id": uid, "status": "pending", "events": [now]})
        return False

    events = res[0].get("events", [])
    # keep hanya event dalam window terakhir
    events = [t for t in events if now - t < window]
    events.append(now)
    db.update({"events": events}, UserQ.user_id == uid)

    return len(events) > limit
