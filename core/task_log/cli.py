import sys
from core.utils.json_utils import print_json
from core.task_log.args import get_file_path, get_file_paths
from core.task_log.end_task import update_end_time_for_active_tasks
from core.task_log.new_task import add_new_task
from core.task_log.report import generate_markdown_report
from core.task_log.stats import calculate_days_stats

def main():
    choice = show_menu()

    if choice == 1:
        new_task()
    elif choice == 2:
        end_task()
    elif choice == 3:
        update_stats()
    elif choice == 4:
        report_name = input("Enter report name: ")
        sys.argv.append(report_name)
        generate_report()
    else:
        print("Invalid choice. Please try again.")

def show_menu():
    print("1. Add new task")
    print("2. End active task")
    print("3. Update statistics")
    print("4. Generate report")
    
    try:
        choice = int(input("Enter your choice (1-5): "))
        return choice
    except ValueError:
        print("Please enter a number between 1 and 5")
        return show_menu()

config = {
    'base_directory': r'C:\atari-monk\code\text-data\project_tracker',
    'filename': 'tasks.json',
    'filename_1': 'tasks.json',
    'filename_2': 'stats.json'
}

def new_task():
    file_path = get_file_path(config, sys.argv)
    add_new_task(file_path)
    print_json(file_path)

def end_task():
    file_path = get_file_path(config, sys.argv)
    update_end_time_for_active_tasks(file_path)
    print_json(file_path)

def update_stats():
    file_1_path, file_2_path = get_file_paths(config, sys.argv)
    calculate_days_stats(file_1_path, file_2_path)
    print_json(file_2_path)

def generate_report():
    if len(sys.argv) < 2:
        print("Please provide a report name as argument")
        return
    
    file_1_path, file_2_path = get_file_paths(config, sys.argv)
    report_path = generate_markdown_report(file_1_path, file_2_path, sys.argv[1])
    
    if report_path:
        print(f"Markdown report saved to: {report_path}")
    else:
        print("Error generating the report.")
        
if __name__ == "__main__":
    main()