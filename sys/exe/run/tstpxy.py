import os
import subprocess

# Get the current directory
directory = os.path.dirname(os.path.realpath(__file__))

# Get a list of all Python files in the directory (excluding pxy.py)
python_files = [f for f in os.listdir(directory) if f.endswith(".py") and f != "pxy.py" and f != "tstpxy.py" and f != "login_get_kite.py"]


# Variables to track success and failure
success_files = []
failed_files = {}

# Run each Python file and check for errors
for file in python_files:
    file_path = os.path.join(directory, file)
    print(f"Running {file}...")

    try:
        # Use subprocess to run the Python script
        subprocess.check_call(["python", file_path])
        print(f"{file} executed successfully.\n")
        success_files.append(file)
    except subprocess.CalledProcessError as e:
        print(f"Error running {file}: {e}\n")
        failed_files[file] = str(e)
    except Exception as e:
        print(f"An unexpected error occurred while running {file}: {e}\n")
        failed_files[file] = str(e)

# Print summary
print("\nSummary:")
if success_files:
    print(f"{len(success_files)} files ran successfully: {', '.join(success_files)}")
else:
    print("No files ran successfully.")

if failed_files:
    print(f"{len(failed_files)} files had problems:")
    for file, error_message in failed_files.items():
        print(f"{file}: {error_message}")
else:
    print("No files had problems.")
