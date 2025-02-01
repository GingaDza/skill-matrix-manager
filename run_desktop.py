# run_desktop.py
import sys
from datetime import datetime
from src.desktop.main import main

if __name__ == "__main__":
    current_time_utc = datetime(2025, 1, 31, 12, 38, 41)
    current_user = "GingaDza"
    
    print(f"Starting Skill Matrix Manager...")
    print(f"Current Time (UTC): {current_time_utc.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Current User: {current_user}")
    
    sys.exit(main())