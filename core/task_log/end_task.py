from datetime import datetime
from core.utils.json_utils import format_json, load_json, save_json
from core.utils.time_utils import minutes_between_times

def update_end_time_for_active_tasks(file_path):
    data = load_json(file_path)
    if data is None:
        return
    
    current_time = datetime.now().strftime("%H:%M")
    record = get_active(data)

    if record:
        record["end_time"] = current_time
        record["actual_minutes"] = minutes_between_times(record["start_time"], record["end_time"])

        note = input("Would you like to add a note? (Press Enter to skip): ").strip()
        if note:
            record["note"] = note
        else:
            record["note"] = ""

    json_string = format_json(data)
    save_json(file_path, json_string)

def get_active(data):
    active_records = [entry for entry in data if not entry.get("end_time") and "start_time" in entry]
    return active_records[-1] if active_records else None
