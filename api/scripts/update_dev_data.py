import json
from pathlib import Path
from datetime import datetime, timedelta


def update_day(timestamp: int, days_from_today: int) -> int:
    """Takes in a timestamp and returns a new one with the day updated relative to today."""
    new_date = datetime.now() + timedelta(days=days_from_today)
    return int(datetime.fromtimestamp(timestamp)
               .replace(year=new_date.year, month=new_date.month, day=new_date.day)
               .timestamp())

def main():
    script_dir = Path(__file__).parent.resolve()
    DATA_FILE = script_dir /".."/"nvdagen"/"fixtures"/"fixtures.json"

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    # Update listing and program dates
    for entry in data:
        fields = entry["fields"]

        if entry["model"] == "nvdagen.listing":
            # Set deadline 1 week from today
            entry["fields"]["deadline"] = (datetime.now() + timedelta(days=7)).isoformat()[:10]
        
        elif entry["model"] == "nvdagen.program":
            # Set event start for tomorrow and registration start to yesterday
            entry["fields"]["timeStart"] = update_day(fields["timeStart"], 1)
            entry["fields"]["timeEnd"] = update_day(fields["timeEnd"], 1)
            entry["fields"]["registrationStart"] = update_day(fields["registrationStart"], -1)
            entry["fields"]["registrationEnd"] = update_day(fields["registrationEnd"], 1)

    with open(DATA_FILE, "w") as f: 
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    main()