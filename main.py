import os
import shutil
from abc import ABC, abstractmethod
import time


class History:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(History, cls).__new__(cls)
        return cls._instance

    def save_history_to_file(self, token):
        file = open("action_history.txt", 'a')
        file.write(
            "Program initiated action:: " + token['type'] + "  :: File::  " + token[
                'filename'] + "  ::Source folder:: " + token['source'] + " ::destination:: " + token[
                'destination'] + '\n')
        # file.write((',' * 160 + '\n'))
        file.close()

    def read_last_action(self):
        file = open("action_history.txt", 'r')
        line = file.readline()

        for line in file:
            pass
        while line:
            parts = line.split('::')
            action_type = parts[1].strip()
            filename = parts[3].strip()  # Splitting by space to get the filename
            source_folder = parts[4].strip()  # Splitting by space to get the source folder
            destination_folder = parts[7].strip()

            return action_type, filename, source_folder, destination_folder


class Command(ABC):

    @abstractmethod
    def execute(self):
        pass


class Action():
    def __init__(self):
        self.__actions = []
        self.removed_file_content = []
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
        return self.__destination_directory

    def get_removed_file_content(self):

        return self.removed_file_content

    def add_action(self, action, ):
        history = History()

        self.__actions.append(action)
        token = self.__actions.pop()

        history.save_history_to_file(token)
        self.__actions.append(token)

    def show_actions(self):
        history = History()
        action_type, filename, source_folder, destination_folder = history.read_last_action()
        print(
            "Last action: " + action_type + " File used: " + filename + " Source: " + source_folder + " Destination: " + destination_folder)

    def execute_action(self, case, file_name, destination=None):

        self.__last_file_name = file_name
        self.__source_directory = os.getcwd()
        if (destination == None):
            self.__destination_directory = ""
            destination = ""
        else:
            self.__destination_directory = destination

        if case == 1:
            self.add_action(
                {'type': 'create_file', 'filename': self.__last_file_name, 'source': self.__source_directory,
                 'destination': os.getcwd() + "\\" + destination})
            add_file_command = AddFile(self.__last_file_name)
            add_file_command.execute()

        elif case == 2:
            self.add_action(
                {'type': 'remove_file', 'filename': self.__last_file_name, 'source': self.__source_directory,
                 'destination': os.getcwd() + "\\" + destination})
            self.save_file_contents_to_list(self.__last_file_name)
            remove_file_command = RemoveFile(self.__last_file_name)
            remove_file_command.execute()

        elif case == 4:
            if destination is None:
                raise ValueError("Destination must be provided for copying a file.")
            self.add_action({'type': 'copy_file', 'filename': self.__last_file_name, 'source': self.__source_directory,
                             'destination': os.getcwd() + "\\" + destination})
            copy_file_command = CopyFile(self.__last_file_name, self.__source_directory, destination)
            self.__destination_directory = destination
            copy_file_command.execute()


        elif case == 5:
            if destination is None:
                raise ValueError("Destination must be provided for moving a file.")
            print(self.__last_file_name)
            self.add_action({'type': 'move_file', 'filename': self.__last_file_name, 'source': self.__source_directory,
                             'destination': os.getcwd() + "\\" + destination})
            move_file_command = MoveFile(self.__last_file_name, self.__source_directory, destination)
            move_file_command.execute()

        elif case == 6:
            self.add_action(
                {'type': 'create_directory', 'filename': self.__last_file_name, 'source': self.__source_directory,
                 'destination': os.getcwd() + "\\" + self.__last_file_name})
            create_directory_command = CreateDirectory(self.__last_file_name)

            create_directory_command.execute()

        else:
            raise ValueError("Invalid action case.")

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

                    self.removed_file_content.append(line)

            print(f"File '{file_name}' contents have been saved to a list.")
        else:
            print(f"File '{file_name}' does not exist in the current directory.")


class Restore(Action):
    def __init__(self, __actions, file_name, file_source, file_destination, removed_file_content):
        super().__init__()
        self.history = __actions
        self.__source_directory = file_source
        self.__destination_directory = file_destination
        self.__last_file_name = file_name
        self.__removed_file_content = removed_file_content

    def undo_last_action(self):
        history_from_file = History()
        action_type, filename, source_folder, destination_folder = history_from_file.read_last_action()

        if self.history:

            if action_type == 'create_file':
                action.save_file_contents_to_list(self.__last_file_name)
                remove_file_command = RemoveFile(self.__last_file_name)
                remove_file_command.execute()
            elif action_type == 'remove_file':
                self.restore_file(filename)
            elif action_type == 'create_directory':
                os.rmdir(filename)
            elif action_type == 'copy_file':
                remove_file_command = RemoveFile(self.__last_file_name)
                remove_file_command.execute_to_destination(self.__destination_directory)

            elif action_type == 'move_file':
                self.move_file()

    def move_file(self):
        source = os.path.join(os.getcwd(), self.__destination_directory, self.__last_file_name)
        self.__source_directory = os.getcwd()
        shutil.move(source, self.__source_directory)
        print("File moved successfully.")

    def restore_file(self, file_name):

        file = open(file_name, 'w')
        for line in self.__removed_file_content:
            file.write(line + "\n")
        file.close()


class RemoveFile(Command):

    def __init__(self, file_name):
        super().__init__()
        self.file_name = file_name
        self.removed_file_content = []

    def execute(self):
        file_path = os.path.join(os.getcwd(), self.file_name)
        self.save_file_contents_to_list(self.file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print("File removed successfully.")
        else:
            print("File does not exist.")

    def save_file_contents_to_list(self, file_name):
        file_path = os.path.join(os.getcwd(), file_name)
        if os.path.exists(file_path):

            with open(file_name) as file:
                for line in file:
                    line = line.strip()  # or some other preprocessing

                    self.removed_file_content.append(line)

            print(f"File '{file_name}' contents have been saved to a list.")
        else:
            print(f"File '{file_name}' does not exist in the current directory.")
        return self.removed_file_content

    def execute_to_destination(self, destination):

        file_path = os.path.join(os.getcwd() + "\\" + destination, self.file_name)

        self.save_file_contents_to_list(self.file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print("File removed successfully.")
        else:
            print("File does not exist.")


class AddFile(Command):
    def __init__(self, file_name):
        super().__init__()
        self.file_name = file_name

    def execute(self):
        if not os.path.exists(self.file_name):
            with open(self.file_name, 'w'):
                pass

            print("File was created successfully")

        else:
            print("File already exists")


class CopyFile(Command):
    def __init__(self, file_name, source, destination):
        super().__init__()
        self.file_name = file_name
        self.source_directory = source
        self.destination_directory = destination

    def execute(self):
        if os.path.exists(self.file_name):
            shutil.copy(self.file_name, self.destination_directory)
            print(f"File {self.file_name} was transfered to {self.destination_directory}.")

        else:
            print(f"Error: File {self.file_name}does not exist.")


class MoveFile(Command):

    def __init__(self, file_name, source, destination):
        super().__init__()
        self.file_name = file_name
        self.source_directory = source
        self.destination_directory = destination

    def execute(self):
        shutil.move(self.file_name, self.destination_directory)

        print("File moved successfully.")


class CreateDirectory(Command):

    def __init__(self, directory_name):
        super().__init__()
        self.directory_name = os.path.join(os.getcwd(), directory_name)

    def execute(self):
        if os.path.exists(self.directory_name):
            print("Directory or a file by that name already exists")
            return
        os.makedirs(self.directory_name, exist_ok=True)

        print("Directory created successfully.")


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
            file_name = input("Enter the file name to add: ")
            action.execute_action(1, file_name)
        elif choice == '2':
            file_name = input("Enter the file name to remove: ")
            action.execute_action(2, file_name)
        elif choice == '3':
            action.show_files()
        elif choice == '4':
            file_name = input("Enter the file name: ")
            destination = input("Enter the destination file path: ")
            action.execute_action(4, file_name, destination)
        elif choice == '5':
            file_name = input("Enter the file name: ")
            destination = input("Enter the destination file path: ")
            action.execute_action(5, file_name, destination)
        elif choice == '6':
            dir_name = input("Enter the name of the directory to create: ")
            action.execute_action(6, dir_name)
        elif choice == '7':
            action.show_actions()
        elif choice == '8':
            restore = Restore(action.get_actions(), action.get_removed_file_name(), action.get_source_directory(),
                              action.get_destination_directory(), action.get_removed_file_content())
            restore.undo_last_action()
            print("Restored last action.")
        elif choice == '9':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 9.")


if __name__ == "__main__":
    main()

