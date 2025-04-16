from datetime import datetime
import subprocess

def minutes_between_times(start_time, end_time):
    start = datetime.strptime(start_time, "%H:%M")
    end = datetime.strptime(end_time, "%H:%M")
    delta = end - start
    return delta.seconds // 60

def minutes_to_hhmm(minutes):
    return f"{minutes // 60:02}:{minutes % 60:02}"

def get_last_wake_time():
    try:
        command = 'powershell -Command "Get-WinEvent -FilterHashtable @{LogName=\'System\'; ID=1} | Select-Object -First 1 -ExpandProperty TimeCreated"'
        output = subprocess.check_output(command, shell=True).decode().strip()
        return output
    except subprocess.CalledProcessError as e:
        return f"Error fetching wake-up time: {e}"