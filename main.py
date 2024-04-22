import os
import shutil


class Action:
    def __init__(self):
        self.__actions = []
        self.__removed_file_content = []
        self.__source_directory = []
        self.__destination_directory = []
        self.__last_file_name = []


    def get_actions(self):
        return self.__actions
    def get_removed_file_name(self):
        return self.__last_file_name
    def get_source_directory(self):
        return self.__source_directory
    def get_destination_directory(self):
        return  self.__destination_directory
    def get_removed_file_content(self):
        return self.__removed_file_content
    def add_action(self, action):
        self.__actions.append(action)

    def show_actions(self):
        if self.__actions:
            print("Last action:", self.__actions[-1])
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
            action.add_action({'type': 'remove_file', 'filename': file_name})
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

            with open(file_name) as file:
                for line in file:
                    line = line.strip()  # or some other preprocessing

                    self.__removed_file_content.append(line)

            print(f"File '{file_name}' contents have been saved to a list.")
        else:
            print(f"File '{file_name}' does not exist in the current directory.")

    def copy_file(self, source, destination):
        if os.path.exists(source):
            shutil.copy(source, destination)
            print(f"File {source} was transfered to {destination}.")
            self.add_action({'type': 'move_file', 'source': source, 'destination': destination})
        else:
            print(f"Error: File {source} does not exist.")

    def move_file(self, source, destination):
        self.__last_file_name = source
        self.__source_directory = os.getcwd()
        self.__destination_directory = destination
        shutil.move(source, destination)
        action.add_action({'type': 'move_file', 'source': source, 'destination': destination})
        print("File moved successfully.")

    def create_directory(self, directory_name):
        os.makedirs(directory_name, exist_ok=True)
        action.add_action({'type': 'create_directory', 'directory': directory_name})
        print("Directory created successfully.")

class Restore(Action):
    def __init__(self, __actions, file_name, file_source, file_destination, removed_file_content):
        super().__init__()
        self.history = __actions
        self.__source_directory = file_source
        self.__destination_directory = file_destination
        self.__last_file_name = file_name
        self.__removed_file_content = removed_file_content


    def undo_last_action(self):

        if self.history:
            last_action = (self.history.pop())
            if last_action['type'] == 'create_file':
                self.remove_file(last_action['filename'])
            elif last_action['type'] == 'remove_file':
                self.restore_file(last_action['filename'])
            elif last_action['type'] == 'create_directory':
                os.rmdir(last_action['directory'])
            elif last_action['type'] == 'remove_directory':
                self.create_directory(last_action['directory'])
            elif last_action['type'] == 'copy_file':
                self.remove_file(last_action['destination'])
            elif last_action['type'] == 'move_file':
                self.move_file("source", "dsa")

    def move_file(self, source, destination):
        source = os.path.join(os.getcwd(), self.__destination_directory, self.__last_file_name)
        self.__source_directory = os.getcwd()
        shutil.move(source, self.__source_directory)
        action.add_action({'type': 'move_file', 'source': source, 'destination': destination})
        print("File moved successfully.")

    def restore_file (self, file_name):

        file = open(file_name, 'w')
        for line in self.__removed_file_content:
            file.write(line + "\n")
        file.close()



action = Action()
def main():

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
            file_path = input("Enter the file name to add: ")
            action.add_file(file_path)
        elif choice == '2':
            file_path = input("Enter the file name to remove: ")
            action.remove_file(file_path)
        elif choice == '3':
            action.show_files()
        elif choice == '4':
            source = input("Enter the file name: ")
            destination = input("Enter the destination file path: ")
            action.copy_file(source, destination)
        elif choice == '5':
            source = input("Enter the file name: ")
            destination = input("Enter the destination file path: ")
            action.move_file(source, destination)
        elif choice == '6':
            dir_name = input("Enter the name of the directory to create: ")
            action.create_directory(dir_name)
        elif choice == '7':
            action.show_actions()
        elif choice == '8':
            restore = Restore(action.get_actions(), action.get_removed_file_name(), action.get_source_directory(), action.get_destination_directory(), action.get_removed_file_content())
            restore.undo_last_action()
            print("Restored last action.")
        elif choice == '9':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 9.")



if __name__ == "__main__":
    main()