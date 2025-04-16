from datetime import datetime
from core.utils.json_utils import format_json, load_json, save_json

def add_new_task(file_path):
    data = load_json(file_path)
    if data is None:
        return
    
    project = input("Enter project name: ")
    task = input("Enter task description: ")
    estimate_minutes = int(input("Enter estimated minutes: "))
    current_time = datetime.now().strftime("%H:%M")
    today = datetime.now()
    
    new_task = {
        "date": today.strftime("%Y-%m-%d"),
        "project": project,
        "task": task,
        "estimate_minutes": estimate_minutes,
        "start_time": current_time,
        "end_time": "",
        "actual_minutes": 0
    }
    
    data.append(new_task)
    json_string = format_json(data)
    save_json(file_path, json_string)
