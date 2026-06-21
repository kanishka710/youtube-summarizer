def time_to_seconds(time_str):
    """Converts 'MM:SS' or 'HH:MM:SS' to total seconds."""
    parts = list(map(int, time_str.split(':')))
    if len(parts) == 2: # MM:SS
        return parts[0] * 60 + parts[1]
    elif len(parts) == 3: # HH:MM:SS
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    return 0