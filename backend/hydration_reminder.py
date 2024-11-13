from datetime import datetime, timedelta

class HydrationReminder:
    def __init__(self, interval=60):
        self.interval = timedelta(minutes=interval)
        self.last_reminder = datetime.now()

    def check_reminder(self):
        if datetime.now() >= self.last_reminder + self.interval:
            print("Time to hydrate!")
            self.last_reminder = datetime.now()
