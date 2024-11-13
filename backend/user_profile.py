import pandas as pd

class UserProfile:
    def __init__(self, user_id, name, age, weight, activity_level):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.weight = weight
        self.activity_level = activity_level
        self.daily_goal = self.calculate_daily_goal()
    
    def calculate_daily_goal(self):
        base_amount = 2000  # Base daily intake in ml
        activity_factor = {"low": 1.0, "medium": 1.2, "high": 1.5}
        return base_amount * activity_factor.get(self.activity_level, 1.0)

def load_user_profile(user_id):
    # Load profile from CSV
    users_df = pd.read_csv('users.csv')
    user_data = users_df[users_df['user_id'] == user_id].iloc[0]
    return UserProfile(user_data['user_id'], user_data['name'], user_data['age'],
                       user_data['weight'], user_data['activity_level'])
