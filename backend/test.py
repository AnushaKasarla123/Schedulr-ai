import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from calendar_utils import list_events, create_event

# 📅 Show upcoming events
print("\n📅 Fetching upcoming Google Calendar events...")
list_events()

# 📅 Create a test event
print("\n📅 Creating a test calendar event...")
create_event(
    "TailorTalk Test Meeting",
    "2025-06-27T15:00:00",
    "2025-06-27T15:30:00"
)
