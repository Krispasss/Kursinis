import os
import shutil

class Action:
    def __init__(self):
        self.actions = []
        self.removed_file_content = []
        self.source_directory = []
        self.destination_directory = []

    def add_action(self, action):
        self.actions.append(action)

    def show_actions(self):
        if self.actions:
            print("Last action:", self.actions[-1])
        else:
            print("No actions performed yet.")



    def add_file(self, filename):
        if not os.path.exists(filename):
            with open(filename, 'w'):
                pass

            print("File was created successfully")
            action.add_action({'type': 'create_file', 'filename': filename})
        else:
            print("File already exists")

    def remove_file(self, file_name):
        file_path = os.path.join(os.getcwd(), file_name)
        self.save_file_contents_to_list(file_name)
        if os.path.isfile(file_path):
            self.add_action("Removed file: " + file_path)
            os.remove(file_path)
            print("File removed successfully.")
        else:
            print("File does not exist.")

    def show_files(self):
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        if files:
            print("Files in current directory:")
            for f in files:
                print(f)
        else:
            print("No files in current directory.")

    def save_file_contents_to_list(self, file_name):
        file_path = os.path.join(os.getcwd(), file_name)
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                self.removed_file_content.append(file.readlines())
            print(f"File '{file_name}' contents have been saved to a list.")
        else:
            print(f"File '{file_name}' does not exist in the current directory.")


    def copy_file(self, src, dest):
        if os.path.isfile(src):
            shutil.copy(src, dest)
            self.add_action("Copied file from {} to {}".format(src, dest))
            print("File copied successfully.")
        else:
            print("Source file does not exist.")


    def move_file(self, source, destination):
        if os.path.isfile(source):
            self.source_directory = os.getcwd()
            self.destination_directory = destination
            shutil.move(source, destination)
            self.add_action("Moved file from {} to {}".format(source, destination))
            print("File moved successfully.")
        else:
            print("Source file does not exist.")

    def create_directory(self, dir_name):
        os.makedirs(dir_name, exist_ok=True)
        self.add_action("Created directory: " + dir_name)
        print("Directory created successfully.")

    def undo_last_action(self):
        if self.actions:
            last_action = self.actions.pop()
            if last_action['type'] == 'create_file':
                self.remove_file(last_action['filename'])
            elif last_action['type'] == 'remove_file':
                self.add_file(last_action['filename'])
            elif last_action['type'] == 'create_directory':
                os.rmdir(last_action['directory'])
            elif last_action['type'] == 'remove_directory':
                self.create_directory(last_action['directory'])
            elif last_action['type'] == 'copy_file':
                self.remove_file(last_action['destination'])
            elif last_action['type'] == 'move_file':
                self.move_file(last_action['destination'], last_action['source'])




action = Action()

while True:
    print("\nChoose an action:")
    print("1. Add a file")
    print("2. Remove a file")
    print("3. Show files")
    print("4. Copy a file")
    print("5. Move a file")
    print("6. Create a directory")
    print("7. Show last action")
    print("8. Undo last action")
    print("9. Exit")

    choice = input("Enter your choice (1-9): ")

    if choice == '1':
        file_path = input("Enter the path of the file to add: ")
        action.add_file(file_path)
    elif choice == '2':
        file_path = input("Enter the path of the file to remove: ")
        action.remove_file(file_path)
    elif choice == '3':
        action.show_files()
    elif choice == '4':
        source = input("Enter the source file path: ")
        destination = input("Enter the destination file path: ")
        action.copy_file(source, destination)
    elif choice == '5':
        source = input("Enter the source file path: ")
        destination = input("Enter the destination file path: ")
        action.move_file(source, destination)
    elif choice == '6':
        dir_name = input("Enter the name of the directory to create: ")
        action.create_directory(dir_name)
    elif choice == '7':
        action.show_actions()
    elif choice == '8':
        action.undo_last_action()
    elif choice == '9':
        print("Exiting program.")
        break
    else:
        print("Invalid choice. Please enter a number between 1 and 9.")
