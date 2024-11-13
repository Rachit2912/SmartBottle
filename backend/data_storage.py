import pandas as pd

def save_intake_data(intake_log):
    intake_log.to_csv("intake_log.csv", index=False)

def load_intake_data():
    try:
        return pd.read_csv("intake_log.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["user_id", "timestamp", "amount"])
    