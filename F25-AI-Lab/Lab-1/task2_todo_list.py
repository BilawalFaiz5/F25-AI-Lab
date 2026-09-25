tasks = []

while True:
    print("\n--- TO-DO LIST ---")
    print("1. Add Task")
    print("2. Remove Task")
    print("3. View Tasks")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        task = input("Enter a task: ")
        tasks.append(task)
        print("Task added successfully.")

    elif choice == "2":
        if len(tasks) == 0:
            print("No tasks available.")
        else:
            print("\nYour Tasks:")
            for i, task in enumerate(tasks, 1):
                print(f"{i}. {task}")

            number = int(input("Enter task number to remove: "))

            if 1 <= number <= len(tasks):
                removed_task = tasks.pop(number - 1)
                print(f"Removed: {removed_task}")
            else:
                print("Invalid task number.")

    elif choice == "3":
        if len(tasks) == 0:
            print("No tasks available.")
        else:
            print("\n--- YOUR TASKS ---")
            for i, task in enumerate(tasks, 1):
                print(f"{i}. {task}")

    elif choice == "4":
        print("Program ended.")
        break

    else:
        print("Invalid choice. Please try again.")