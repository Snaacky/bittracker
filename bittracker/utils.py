def format_bytes(size: int) -> str:
    """Convert an integer of bytes into an appropriately sized unit string."""
    if size == 0:
        return "0 B"

    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    size_float = float(size)
    for unit in units:
        if size_float < 1024:
            return f"{size_float:.2f} {unit}"
        size_float /= 1024

    return f"{size_float:.2f} {units[-1]}"