import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QComboBox, QListWidget, QTimeEdit, QMenu, QInputDialog
from PyQt6.QtCore import QTimer, Qt
import datetime
from stats_window import StatsWindow
from data_manager import add_study_time

from data_manager import add_class, add_assignment, get_classes, get_assignments, remove_class, remove_assignment

# ... [All the methods and functions related to the `App` class will go here] ...

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(100, 100, 800, 600)

        # Class dropdown
        self.class_dropdown = QComboBox(self)
        self.class_dropdown.setGeometry(50, 50, 200, 30)
        # Add classes from classes.csv here...

        # Assignment dropdown
        self.assignment_dropdown = QComboBox(self)
        self.assignment_dropdown.setGeometry(50, 100, 200, 30)
        # Add assignments from assignments.csv here...

        # Stopwatch
        self.stopwatch_label = QLabel('0:00:00', self)
        self.stopwatch_label.setGeometry(50, 150, 200, 30)

        # Stopwatch Timer
        self.stopwatch_timer = QTimer(self)
        self.stopwatch_timer.timeout.connect(self.update_stopwatch)
        self.elapsed_time = 0  # in seconds

        # Start Button
        self.start_button = QPushButton('Start', self)
        self.start_button.setGeometry(260, 100, 60, 30)
        self.start_button.clicked.connect(self.start_stopwatch)

        # Stop Button
        self.stop_button = QPushButton('Stop', self)
        self.stop_button.setGeometry(330, 100, 60, 30)
        self.stop_button.clicked.connect(self.stop_stopwatch)

        # Reset Button
        self.reset_button = QPushButton('Reset', self)
        self.reset_button.setGeometry(400, 100, 60, 30) 
        self.reset_button.clicked.connect(self.reset_stopwatch)

        # Submit button
        self.submit_button = QPushButton('Submit', self)
        self.submit_button.setGeometry(50, 200, 200, 30)
        self.submit_button.clicked.connect(self.submit_time)

        # Editable class list
        self.class_list = QListWidget(self)
        self.class_list.setGeometry(300, 200, 200, 200)

        # Editable assignment list
        self.assignment_list = QListWidget(self)
        self.assignment_list.setGeometry(550, 200, 200, 200)

        #TODO: find out if this should be after the self.show()
        # When class is changed, update assignment dropdown and assignment list
        self.class_dropdown.currentTextChanged.connect(self.update_assignment_dropdown)
        self.class_dropdown.currentTextChanged.connect(self.update_assignment_list)

        # Initially disable the submit button
        self.submit_button.setEnabled(False)

        # When class or assignment dropdown is changed, check for valid selection
        self.class_dropdown.currentTextChanged.connect(self.check_valid_selection)
        self.assignment_dropdown.currentTextChanged.connect(self.check_valid_selection)

        self.load_data()


        # Right-click context menu for class and assignment lists:
        self.class_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.class_list.customContextMenuRequested.connect(self.show_class_context_menu)

        self.assignment_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.assignment_list.customContextMenuRequested.connect(self.show_assignment_context_menu)

        # Add class and assignment buttons
        self.add_class_button = QPushButton('Add Class', self)
        self.add_class_button.setGeometry(300, 420, 200, 30)  # Moved down
        self.add_class_button.clicked.connect(self.add_new_class)

        self.add_assignment_button = QPushButton('Add Assignment', self)
        self.add_assignment_button.setGeometry(550, 420, 200, 30)  # Moved down
        self.add_assignment_button.clicked.connect(self.add_new_assignment)

        # Button to open the stats window
        self.stats_button = QPushButton('Show Stats', self)
        self.stats_button.setGeometry(300, 500, 200, 30)
        self.stats_button.clicked.connect(self.show_stats_window)

        self.show()

    def load_data(self):
        self.class_dropdown.addItems(get_classes())
        self.assignment_dropdown.addItems(get_assignments())
        self.class_list.addItems(get_classes())
        self.assignment_list.addItems(get_assignments())

    def submit_time(self):
        class_name = self.class_dropdown.currentText()
        assignment_name = self.assignment_dropdown.currentText()

        # Check if both the class and the assignment still exist in their respective CSVs
        if class_name not in get_classes() or assignment_name not in get_assignments():
            print("Error: The selected class or assignment has been deleted.")
            return

        # Compute the time studied in hours
        time_studied = self.elapsed_time / 3600.0

        # Generate a current timestamp
        current_timestamp = datetime.datetime.now().isoformat()

        add_study_time(assignment_name, class_name, time_studied, current_timestamp)

         # Reset the stopwatch after submitting
        self.reset_stopwatch()


    def update_assignment_dropdown(self):
        selected_class = self.class_dropdown.currentText()
        self.assignment_dropdown.clear()
        self.assignment_dropdown.addItems(get_assignments(selected_class))

    def update_assignment_list(self):
        selected_class = self.class_dropdown.currentText()
        self.assignment_list.clear()
        self.assignment_list.addItems(get_assignments(selected_class))

    def show_class_context_menu(self, position):
        menu = QMenu()
        remove_action = menu.addAction("Remove")
        remove_action.triggered.connect(self.remove_selected_class)
        menu.exec(self.class_list.mapToGlobal(position))

    def show_assignment_context_menu(self, position):
        menu = QMenu()
        remove_action = menu.addAction("Remove")
        remove_action.triggered.connect(self.remove_selected_assignment)
        menu.exec(self.assignment_list.mapToGlobal(position))

    def remove_selected_class(self):
        selected_class = self.class_list.currentItem().text()
        remove_class(selected_class)
        self.class_list.takeItem(self.class_list.currentRow())

    def remove_selected_assignment(self):
        selected_assignment = self.assignment_list.currentItem().text()
        remove_assignment(selected_assignment)
        self.assignment_list.takeItem(self.assignment_list.currentRow())

    def add_new_class(self):
        class_name, ok = QInputDialog.getText(self, 'Add Class', 'Enter class name:')
        if ok and class_name:
            if class_name not in get_classes():
                add_class(class_name)
                self.class_list.addItem(class_name)
                self.class_dropdown.addItem(class_name)
            else:
                print(f"Class '{class_name}' already exists.")

    def add_new_assignment(self):
        assignment_name, ok = QInputDialog.getText(self, 'Add Assignment', 'Enter assignment name:')
        if ok and assignment_name:
            class_name = self.class_dropdown.currentText()  # Assuming you want to add the assignment to the currently selected class
            existing_assignments = get_assignments(class_name)
            if assignment_name not in existing_assignments:
                add_assignment(assignment_name, class_name)
                self.assignment_list.addItem(assignment_name)
                self.assignment_dropdown.addItem(assignment_name)
            else:
                print(f"Assignment '{assignment_name}' already exists for class '{class_name}'.")

    def show_stats_window(self):
        self.stats_window = StatsWindow()
        self.stats_window.show()

    def start_stopwatch(self):
        self.stopwatch_timer.start(1000)

    def stop_stopwatch(self):
        self.stopwatch_timer.stop()

    def reset_stopwatch(self):
        self.stopwatch_timer.stop()
        self.elapsed_time = 0
        self.stopwatch_label.setText('0:00:00')

    def update_stopwatch(self):
        self.elapsed_time += 1
        hours = self.elapsed_time // 3600
        minutes = (self.elapsed_time % 3600) // 60
        seconds = self.elapsed_time % 60
        self.stopwatch_label.setText(f'{hours}:{minutes:02d}:{seconds:02d}')

    def check_valid_selection(self):
        # Check if both class and assignment dropdowns have valid selections
        if self.class_dropdown.currentText() and self.assignment_dropdown.currentText():
            self.submit_button.setEnabled(True)
        else:
            self.submit_button.setEnabled(False)