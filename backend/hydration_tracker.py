from datetime import datetime
import pandas as pd
from data_storage import save_intake_data

class HydrationTracker:
    def __init__(self, user_profile):
        self.user_profile = user_profile
        self.intake_log = pd.DataFrame(columns=["user_id", "timestamp", "amount"])

    def log_intake(self, amount):
        timestamp = datetime.now()
        new_entry = pd.DataFrame({"user_id": [self.user_profile.user_id], "timestamp": [timestamp], "amount": [amount]})
        self.intake_log = pd.concat([self.intake_log, new_entry], ignore_index=True)
        save_intake_data(self.intake_log)
    
    def calculate_total_intake(self):
        return self.intake_log['amount'].sum()

    def is_goal_reached(self):
        return self.calculate_total_intake() >= self.user_profile.daily_goal
