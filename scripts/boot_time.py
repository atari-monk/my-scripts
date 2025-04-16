import subprocess

def get_last_wake_time():
    try:
        command = 'powershell -Command "Get-WinEvent -FilterHashtable @{LogName=\'System\'; ID=1} | Select-Object -First 1 -ExpandProperty TimeCreated"'
        output = subprocess.check_output(command, shell=True).decode().strip()
        return output
    except subprocess.CalledProcessError as e:
        return f"Error fetching wake-up time: {e}"

if __name__ == "__main__":
    wake_time = get_last_wake_time()
    print(f"Your computer was last turned on at: {wake_time}")
