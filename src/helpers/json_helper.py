from datetime import timedelta


def encoder(obj):
    if isinstance(obj, timedelta):
        total_seconds = obj.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    return obj
