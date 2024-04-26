import unittest
import os
from main import History, Action, RemoveFile, AddFile, CopyFile, MoveFile, CreateDirectory


class TestHistory(unittest.TestCase):
    def setUp(self):
        self.history = History()

    def test_save_history_to_file(self):
        token = {'type': 'create_file', 'filename': 'test.txt', 'source': 'source', 'destination': 'destination'}
        self.history.save_history_to_file(token)
        with open("action_history.txt", 'r') as file:
            line = file.readline()
            for line in file:
                pass
            self.assertIn("Program initiated action:: create_file  :: File::  test.txt  "
                          "::Source folder:: source ::destination:: destination\n", line)


class TestAction(unittest.TestCase):
    def setUp(self):
        self.action = Action()

    def test_execute_action_invalid_case(self):
        with self.assertRaises(ValueError):
            self.action.execute_action(0, 'test.txt')


class TestRemoveFile(unittest.TestCase):
    def setUp(self):
        self.remove_file_command = RemoveFile("test.txt")

    def test_execute(self):
        with open("test.txt", "w") as file:
            file.write("Test content")
        self.remove_file_command.execute()
        self.assertFalse(os.path.exists("test.txt"))


class TestAddFile(unittest.TestCase):
    def setUp(self):
        self.add_file_command = AddFile("test.txt")

    def test_execute(self):
        self.add_file_command.execute()
        self.assertTrue(os.path.exists("test.txt"))


class TestCopyFile(unittest.TestCase):
    def setUp(self):
        with open("test.txt", "w") as file:
            file.write("Test content")
            if not os.path.isdir("destination"):
                os.mkdir("destination")
        self.copy_file_command = CopyFile("test.txt", ".", "destination")

    def test_execute(self):
        self.copy_file_command.execute()
        self.assertTrue(os.path.exists(os.path.join("destination", "test.txt")))
        os.remove(os.path.join("destination", "test.txt"))


class TestMoveFile(unittest.TestCase):
    def setUp(self):
        with open("test.txt", "w") as file:
            file.write("Test content")
        if not os.path.isdir("destination"):
            os.mkdir("destination")
        self.move_file_command = MoveFile("test.txt", ".", "destination")

    def test_execute(self):
        self.move_file_command.execute()
        destination = os.getcwd() + "\\destination"
        self.assertTrue(os.path.isfile(os.path.join(destination, "test.txt")))


class TestCreateDirectory(unittest.TestCase):
    def setUp(self):
        self.create_directory_command = CreateDirectory("test_dir")

    def test_execute(self):
        self.create_directory_command.execute()
        self.assertTrue(os.path.exists("test_dir"))


if __name__ == '__main__':
    unittest.main()
