import sys

def main():
    if len(sys.argv) < 2:
        print("No action provided")
        return

    action = sys.argv[1]
    if action == 'up':
        print("Moving up")
    elif action == 'down':
        print("Moving down")
    elif action == 'left':
        print("Moving left")
    elif action == 'right':
        print("Moving right")
    elif action == 'home':
        print("Returning to home position")
    elif action == 'emergency_stop':
        print("Emergency stop activated!")
    else:
        print(f"Unknown action: {action}")

if __name__ == "__main__":
    main()