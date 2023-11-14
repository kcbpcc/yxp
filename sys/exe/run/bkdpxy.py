import pandas as pd

def sum_booked_values(file_path):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)

    # Filter rows where the last column ("Status") is "Booked"
    booked_rows = df[df.iloc[:, -1] == "Booked"]

    # Sum the values in the last column of the filtered rows
    total_booked_sum = booked_rows.iloc[:, -2].sum()

    return total_booked_sum

if __name__ == "__main__":
    file_path = "filePnL.csv"
    booked_sum = sum_booked_values(file_path)
    print(f"Total sum of 'Booked' values: {booked_sum}")
