from core.utils.time_utils import get_last_wake_time

if __name__ == "__main__":
    wake_time = get_last_wake_time()
    print(f"Your computer was last turned on at: {wake_time}")
