import pandas as pd

from csv_utils import create_csv_if_not_exists

# ... [All the functions related to data management like `add_class`, `add_assignment`, etc. will go here] ...

def add_class(class_name):
    class_name = str(class_name)  # Ensure the class name is a string

    create_csv_if_not_exists('classes.csv', ['class_name'])
    classes = pd.read_csv('classes.csv', index_col=False)

    # Check if class already exists
    if class_name in classes['class_name'].values:
        print(f"Class '{class_name}' already exists.")
        return

    classes = classes._append({'class_name': class_name}, ignore_index=True)
    classes.to_csv('classes.csv', index=False)

def add_assignment(assignment_name, class_name):
    assignment_name = str(assignment_name)  # Ensure the assignment name is a string
    class_name = str(class_name)  # Ensure the class name is a string

    create_csv_if_not_exists('assignments.csv', ['assignment_name', 'class_name'])
    assignments = pd.read_csv('assignments.csv', index_col=False)

    # Check if assignment with that name already exists for the class
    existing_assignment = assignments[(assignments['assignment_name'] == assignment_name) & 
                                      (assignments['class_name'] == class_name)]
    
    if not existing_assignment.empty:
        print(f"Assignment '{assignment_name}' already exists for class '{class_name}'.")
        return

    assignments = assignments._append({'assignment_name': assignment_name, 'class_name': class_name}, ignore_index=True)
    assignments.to_csv('assignments.csv', index=False)

def add_study_time(assignment_name, class_name, time_studied, timestamp):
    create_csv_if_not_exists('study_times.csv', ['assignment_name', 'class_name', 'time_studied', 'timestamp'])
    study_times = pd.read_csv('study_times.csv', index_col=False)
    study_times = study_times._append({'assignment_name': assignment_name, 'class_name': class_name, 'time_studied': time_studied, 'timestamp': timestamp}, ignore_index=True)
    study_times.to_csv('study_times.csv', index=False)

def get_classes():
    try:
        classes = pd.read_csv('classes.csv')
        return classes['class_name'].tolist()
    except FileNotFoundError:
        return []

def get_assignments(class_name=None):
    try:
        assignments = pd.read_csv('assignments.csv')
        if class_name:
            return assignments[assignments['class_name'] == class_name]['assignment_name'].tolist()
        else:
            return assignments['assignment_name'].tolist()
    except FileNotFoundError:
        return []

def get_study_times(assignment_name=None, class_name=None):
    try:
        study_times = pd.read_csv('study_times.csv')
        if assignment_name:
            study_times = study_times[study_times['assignment_name'] == assignment_name]
        if class_name:
            study_times = study_times[study_times['class_name'] == class_name]
        return study_times['time_studied'].tolist()
    except FileNotFoundError:
        return []
    
def remove_class(class_name):
    classes = pd.read_csv('classes.csv')
    classes = classes[classes['class_name'] != class_name]
    classes.to_csv('classes.csv', index=False)
    
    # Remove relevant assignments
    assignments = pd.read_csv('assignments.csv')
    assignments_to_remove = assignments[assignments['class_name'] == class_name]['assignment_name'].tolist()
    assignments = assignments[assignments['class_name'] != class_name]
    assignments.to_csv('assignments.csv', index=False)
    
    # Remove relevant study_times for the assignments of the removed class
    study_times = pd.read_csv('study_times.csv')
    for assignment in assignments_to_remove:
        study_times = study_times[study_times['assignment_name'] != assignment]
    study_times.to_csv('study_times.csv', index=False)


def remove_assignment(assignment_name):
    assignments = pd.read_csv('assignments.csv')
    assignments = assignments[assignments['assignment_name'] != assignment_name]
    assignments.to_csv('assignments.csv', index=False)
    
    # Remove relevant study_times
    study_times = pd.read_csv('study_times.csv')
    study_times = study_times[study_times['assignment_name'] != assignment_name]
    study_times.to_csv('study_times.csv', index=False)