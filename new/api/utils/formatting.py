from datetime import datetime

def format_timestamp(iso_timestamp: str) -> str:
    """Format ISO timestamp to human readable format"""
    dt = datetime.fromisoformat(iso_timestamp.replace('Z', '+00:00'))
    return dt.strftime("%d %b %Y at %H:%M")

def format_duration(nanoseconds: float) -> str:
    """Format nanoseconds duration to human readable format"""
    seconds = nanoseconds / 1_000_000_000
    minutes = int(seconds // 60)
    remaining_seconds = seconds % 60
    return f"{minutes}m {remaining_seconds:.2f}s" if minutes > 0 else f"{remaining_seconds:.2f}s"
