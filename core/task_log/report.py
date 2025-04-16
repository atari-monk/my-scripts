from datetime import datetime
from core.utils.json_utils import load_json
from core.utils.time_utils import minutes_to_hhmm

def generate_markdown_report(data_file_path, stats_file_path, month):
    data = load_json(data_file_path)
    stats_data = load_json(stats_file_path)

    if data is None or stats_data is None:
        return "No data found."

    today = datetime.now()
    current_year, current_month = today.year, today.month
    
    if month:
        try:
            month = int(month)
            if not (1 <= month <= 12):
                raise ValueError("Invalid month value. It should be between 1 and 12.")
            current_month = month
        except ValueError:
            return "Invalid month format. Please provide an integer between 1 and 12."

    report = f"# Report for {current_year}-{current_month:02d}\n\n"
    
    total_estimate = 0
    total_minutes = 0
    found_data = False

    tasks_by_day = {}

    for day_entry in data:
        entry_date = datetime.strptime(day_entry["date"], "%Y-%m-%d")
        
        if entry_date.year == current_year and entry_date.month == current_month:
            if entry_date not in tasks_by_day:
                tasks_by_day[entry_date] = []
            tasks_by_day[entry_date].append(day_entry)

    for entry_date, tasks in tasks_by_day.items():
        found_data = True
        report += f"## Day: {entry_date.strftime('%Y-%m-%d')}\n"
        
        daily_estimate = 0
        daily_minutes = 0

        report += "| Project | Task | Start | End | Estimated Time | Minutes |\n"
        report += "|---------|------|-------|-----|----------------|---------|\n"
        
        for record in tasks:
            start_time = record.get("start_time", "")
            end_time = record.get("end_time", "")
            minutes = record.get("actual_minutes", 0)
            estimated_time = record.get("estimate_minutes", 0)

            estimated_time_str = f"{estimated_time // 60:02}:{estimated_time % 60:02}"

            report += f"| {record['project']} | {record['task']} | {start_time} | {end_time} | {estimated_time_str} | {minutes} |\n"

            daily_estimate += estimated_time
            daily_minutes += minutes

        report += "\n| Day Stats             | Value   |\n"
        report += "|-------------------|---------|\n"
        report += f"| Estimated Time    | {minutes_to_hhmm(daily_estimate)} |\n"
        report += f"| Total Time Spent  | {minutes_to_hhmm(daily_minutes)} |\n"
        report += "\n"

        total_estimate += daily_estimate
        total_minutes += daily_minutes

    if not found_data:
        report = "No records found for this month."
    else:
        report += "## Month Stats\n"
        report += "| Stat              | Value   |\n"
        report += "|-------------------|---------|\n"
        report += f"| Total Estimated Time | {minutes_to_hhmm(total_estimate)} |\n"
        report += f"| Total Time Spent    | {minutes_to_hhmm(total_minutes)} |\n"

    markdown_report_path = f"{data_file_path.replace('.json', '')}_report.md"
    with open(markdown_report_path, "w") as file:
        file.write(report)
    
    return markdown_report_path
