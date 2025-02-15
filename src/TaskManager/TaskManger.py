import csv
import hashlib
import os

# File paths for storing user credentials and tasks
USER_FILE = "users.csv"
TASK_FILE = "tasks.csv"

# Global variables
current_user = None

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to register a new user
def register():
    print("\nRegister a New User")
    username = input("Enter a username: ").strip()
    password = input("Enter a password: ").strip()

    # Check if the username already exists
    if os.path.exists(USER_FILE):
        with open(USER_FILE, mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == username:
                    print("Username already exists. Please choose a different username.")
                    return

    # Hash the password and save the user
    hashed_password = hash_password(password)
    with open(USER_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([username, hashed_password])
    print("Registration successful!")

# Function to log in a user
def login():
    global current_user
    print("\nLogin")
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()

    if not os.path.exists(USER_FILE):
        print("No users registered yet.")
        return

    # Validate credentials
    with open(USER_FILE, mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == username and row[1] == hash_password(password):
                current_user = username
                print("Login successful!")
                return
    print("Invalid username or password.")

# Function to add a task
def add_task():
    print("\nAdd a Task")
    if not current_user:
        print("You must be logged in to add a task.")
        return

    description = input("Enter the task description: ").strip()
    if not description:
        print("Task description cannot be empty.")
        return

    # Generate a unique task ID
    task_id = 1
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, mode="r") as file:
            reader = csv.reader(file)
            task_id = sum(1 for row in reader) + 1

    # Save the task
    with open(TASK_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([current_user, task_id, description, "Pending"])
    print("Task added successfully!")

# Function to view tasks
def view_tasks():
    print("\nView Tasks")
    if not current_user:
        print("You must be logged in to view tasks.")
        return

    if not os.path.exists(TASK_FILE):
        print("No tasks found.")
        return

    with open(TASK_FILE, mode="r") as file:
        reader = csv.reader(file)
        tasks = [row for row in reader if row[0] == current_user]

    if not tasks:
        print("No tasks found for the current user.")
        return

    for task in tasks:
        print(f"\nTask ID: {task[1]}")
        print(f"Description: {task[2]}")
        print(f"Status: {task[3]}")

# Function to mark a task as completed
def mark_task_completed():
    print("\nMark a Task as Completed")
    if not current_user:
        print("You must be logged in to mark a task as completed.")
        return

    task_id = input("Enter the task ID to mark as completed: ").strip()
    if not task_id.isdigit():
        print("Invalid task ID.")
        return

    tasks = []
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, mode="r") as file:
            reader = csv.reader(file)
            tasks = [row for row in reader]

    found = False
    for task in tasks:
        if task[0] == current_user and task[1] == task_id:
            task[3] = "Completed"
            found = True
            break

    if not found:
        print("Task not found.")
        return

    # Save updated tasks
    with open(TASK_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(tasks)
    print("Task marked as completed!")

# Function to delete a task
def delete_task():
    print("\nDelete a Task")
    if not current_user:
        print("You must be logged in to delete a task.")
        return

    task_id = input("Enter the task ID to delete: ").strip()
    if not task_id.isdigit():
        print("Invalid task ID.")
        return

    tasks = []
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, mode="r") as file:
            reader = csv.reader(file)
            tasks = [row for row in reader]

    updated_tasks = [task for task in tasks if not (task[0] == current_user and task[1] == task_id)]

    if len(updated_tasks) == len(tasks):
        print("Task not found.")
        return

    # Save updated tasks
    with open(TASK_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(updated_tasks)
    print("Task deleted successfully!")

# Function to display the task manager menu
def task_manager_menu():
    while True:
        print("\nTask Manager Menu")
        print("1. Add a Task")
        print("2. View Tasks")
        print("3. Mark a Task as Completed")
        print("4. Delete a Task")
        print("5. Logout")
        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            add_task()
        elif choice == '2':
            view_tasks()
        elif choice == '3':
            mark_task_completed()
        elif choice == '4':
            delete_task()
        elif choice == '5':
            global current_user
            current_user = None
            print("Logged out successfully!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

# Main program loop
def main():
    while True:
        print("\nWelcome to the Task Manager")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ").strip()

        if choice == '1':
            register()
        elif choice == '2':
            login()
            if current_user:
                task_manager_menu()
        elif choice == '3':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")

# Run the program
if __name__ == "__main__":
    main()