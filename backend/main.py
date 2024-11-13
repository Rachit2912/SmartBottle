from user_profile import load_user_profile
from hydration_tracker import HydrationTracker
from hydration_reminder import HydrationReminder
from sensors import Sensor

def main():
    user = load_user_profile(user_id=1)
    tracker = HydrationTracker(user)
    reminder = HydrationReminder(interval=60)  # Reminds every 60 minutes

    while True:
        reminder.check_reminder()
        
        # Simulate a sensor detecting an intake event
        intake = Sensor.get_intake_amount()
        tracker.log_intake(intake)
        
        if tracker.is_goal_reached():
            print("Congratulations! You've reached your daily hydration goal.")
            break

if __name__ == "__main__":
    main()
