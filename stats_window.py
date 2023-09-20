from PyQt6.QtWidgets import QMainWindow, QLabel
import datetime

from data_manager import get_classes, get_assignments, get_study_times

class StatsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(200, 200, 800, 600)

        # Label to show hours studied for each class
        self.class_hours_label = QLabel(self)
        self.class_hours_label.setGeometry(50, 50, 700, 200)
        # Fetch and show data here...

        # Label to show weekly study time
        self.weekly_study_label = QLabel(self)
        self.weekly_study_label.setGeometry(50, 300, 700, 200)
        # Fetch and show data here...

        self.load_data()  # Load the data when the window is initialized

        self.show()

    def load_data(self):
        # Hours studied for each class
        classes = get_classes()
        class_stats = "Hours studied for each class:\n"
        for c in classes:
            assignments = get_assignments(c)
            for a in assignments:
                total_time = sum(get_study_times(a, c))
                class_stats += f"{c} - {a}: {total_time:.2f} hours\n"

        self.class_hours_label.setText(class_stats)

        # Weekly study time
        # This would be a bit more complex as you'll need to filter by the timestamp for the given week
        # Placeholder logic is kept as it was originally
        today = datetime.date.today()
        start_week = today - datetime.timedelta(days=today.weekday())
        end_week = start_week + datetime.timedelta(days=6)
        weekly_hours = sum(get_study_times())  
        weekly_stats = f"Weekly study time ({start_week} to {end_week}): {weekly_hours} hours"

        self.weekly_study_label.setText(weekly_stats)