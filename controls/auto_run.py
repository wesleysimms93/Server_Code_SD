import sys

def process_file(file_path):
    try:
        with open(file_path, 'r') as file:
            commands = file.readlines()
            for command in commands:
                print(f"Executing command: {command.strip()}")
                # Add logic to process each command
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python auto_run.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    process_file(file_path)