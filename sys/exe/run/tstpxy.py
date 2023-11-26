import os
import subprocess

# Get a list of all Python files in the directory
python_files = [f for f in os.listdir(directory) if f.endswith(".py")]

# Run each Python file and check for errors
for file in python_files:
    file_path = os.path.join(directory, file)
    print(f"Running {file}...")
    
    try:
        # Use subprocess to run the Python script
        subprocess.check_call(["python", file_path])
        print(f"{file} executed successfully.\n")
    except subprocess.CalledProcessError as e:
        print(f"Error running {file}: {e}\n")
    except Exception as e:
        print(f"An unexpected error occurred while running {file}: {e}\n")
