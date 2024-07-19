import datetime
import subprocess

def is_sprint_end():
    # Replace this logic with your sprint schedule check
    today = datetime.date.today()
    sprint_end_dates = [
        datetime.date(2024, 7, 19),
        datetime.date(2024, 7, 26),
        datetime.date(2024, 8, 9),
        datetime.date(2024, 8, 23),
        # Add more sprint end dates here
    ]
    return today in sprint_end_dates

if is_sprint_end():
    subprocess.run(['python', 'scripts/everyfriday.py'])
