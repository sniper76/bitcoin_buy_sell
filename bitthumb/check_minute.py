# main.py
import time
import json
from datetime import datetime, timedelta, timezone

def is_time_exceeded(created_at:str):
    """
    Checks if 10 minutes have passed since the given `created_at` timestamp.

    Args:
        created_at (str): The timestamp in ISO 8601 format (e.g., '2025-01-13T16:36:21+09:00').

    Returns:
        bool: True if 10 minutes have passed, False otherwise.
    """
    try:
        # Parse the created_at string into a timezone-aware datetime object
        created_at_dt = datetime.fromisoformat(created_at)

        # Define KST timezone (UTC+9)
        kst = timezone(timedelta(hours=9))

        # Get the current time in KST
        current_time = datetime.now(kst)

        # Check if the difference is greater than or equal to 10 minutes
        if current_time - created_at_dt >= timedelta(minutes=10):
            return True
        return False
    except ValueError as e:
        print(f"Error parsing created_at: {e}")
        return False

