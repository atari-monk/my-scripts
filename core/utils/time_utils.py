from datetime import datetime

def minutes_between_times(start_time, end_time):
    start = datetime.strptime(start_time, "%H:%M")
    end = datetime.strptime(end_time, "%H:%M")
    delta = end - start
    return delta.seconds // 60

def minutes_to_hhmm(minutes):
    return f"{minutes // 60:02}:{minutes % 60:02}"