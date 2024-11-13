from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime

app = Flask(__name__)

# Load user data and intake log from CSV
USER_DATA_FILE = 'users.csv'  # Path to the users CSV file
INTAKE_LOG_FILE = 'intake_log.csv'  # Path to the intake log CSV file

# Helper functions
def load_user_data():
    """Load user data from the CSV file."""
    return pd.read_csv(USER_DATA_FILE)

def load_intake_log():
    """Load intake log data from the CSV file."""
    return pd.read_csv(INTAKE_LOG_FILE)

def save_intake_log(data):
    """Save the updated intake log to the CSV file."""
    data.to_csv(INTAKE_LOG_FILE, index=False)

def add_intake(user_id, amount):
    """Add a new intake record for the given user."""
    log = load_intake_log()
    new_entry = pd.DataFrame({
        "user_id": [user_id],
        "timestamp": [datetime.now()],
        "amount": [amount]
    })
    log = pd.concat([log, new_entry], ignore_index=True)
    save_intake_log(log)

# Routes
@app.route('/')
def index():
    """Render the index page with a list of users."""
    users = load_user_data()
    return render_template('index.html', users=users)

@app.route('/track/<int:user_id>', methods=['GET', 'POST'])
def track(user_id):
    """Track water intake for a specific user."""
    if request.method == 'POST':
        # Add new water intake when form is submitted
        amount = float(request.form['amount'])
        add_intake(user_id, amount)
        return redirect(url_for('track', user_id=user_id))
    
    user_data = load_user_data()
    user = user_data[user_data['user_id'] == user_id].iloc[0]  # Get user data
    intake_log = load_intake_log()
    user_log = intake_log[intake_log['user_id'] == user_id]  # Get log for this user
    total_intake = user_log['amount'].sum()

    # Generate daily intake graph
    img = io.BytesIO()
    daily_intake = user_log.groupby(pd.to_datetime(user_log['timestamp']).dt.date)['amount'].sum()
    plt.figure(figsize=(10, 10))
    plt.plot(daily_intake.index, daily_intake.values, marker='o', color='b')
    plt.title(f"Daily Water Intake for {user['name']}")
    plt.xlabel("Date")
    plt.ylabel("Water Intake (ml)")
    plt.grid()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()  # Convert plot to base64 for embedding in HTML

    # Render the track page with user data, total intake, and the daily intake graph
    return render_template('track.html', user=user, total_intake=total_intake, plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)
