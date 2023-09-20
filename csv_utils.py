import csv

def create_csv_if_not_exists(filename, headers):
    """Create a CSV file with given headers if it doesn't exist."""
    try:
        with open(filename, 'x', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
    except FileExistsError:
        pass
