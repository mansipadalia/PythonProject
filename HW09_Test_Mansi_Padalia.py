"""
Author: Mansi Padalia
CWID: 10442254
Assignment: Homework 9 - Test
Date: 10/23/2019
"""

import unittest
from prettytable import PrettyTable
from HW09_Mansi_Padalia import Repository, Student, Instructor, Major, read_file_generator


class TestRepository(unittest.TestCase):
    """ Test class to perform test over university repository """

    def test_read_file_generator(self):
        """ verify the generator function to read field-separated text files and yield a tuple with all of the values from a single line in the file """
        directory = '/Volumes/Macintosh HD/Users/pratik/Courses/SSW810A/PythonProject'
        filename = 'HW09_ReadFile.txt'
        gen = read_file_generator(directory, filename, 3, sep='|', header=True)
        expected_result = [('123', 'Jin He', 'Computer Science'), ('234', 'Nanda Koka',
                                                                   'Software Engineering'), ('345', 'Benji Cai', 'Software Engineering')]
        for t in expected_result:
            self.assertEqual(t, next(gen))

        filename = 'HW09_ReadFile_NoHeader.txt'
        gen = read_file_generator(
            directory, filename, 3, sep='|', header=False)
        expected_result = [('123', 'Jin He', 'Computer Science'), ('234', 'Nanda Koka',
                                                                   'Software Engineering'), ('345', 'Benji Cai', 'Software Engineering')]
        for t in expected_result:
            self.assertEqual(t, next(gen))
        filename = 'HW09_ReadFile_Bad.txt'
        gen = read_file_generator(directory, filename, 3, sep='|', header=True)
        with self.assertRaises(ValueError):
            next(gen)
        gen = read_file_generator(
            directory, "abcdefg.txt", 3, sep='|', header=True)
        with self.assertRaises(FileNotFoundError):
            next(gen)

    def test_create_repository(self):
        """ verify that given a directory, it creates repository instance with all majors, students and instructor information """
        test_directory = '/Volumes/Macintosh HD/Users/pratik/Courses/SSW810A/PythonProject/Test'
        test_repository = Repository(test_directory)

        expected_majors_table = PrettyTable(
            field_names=['Dept', 'Required', 'Electives'])
        expected_majors_table.add_row(
            ['CS', sorted(['CS 510', 'CS 520']), sorted(['SSW 500', 'SSW 510', 'SSW 520', 'SSW 530', 'SSW 540'])])
        expected_majors_table.add_row(
            ['SSW', sorted(['SSW 500', 'SSW 510', 'SSW 520', 'SSW 530', 'SSW 540']), sorted(['CS 510', 'CS 520'])])
        self.assertEqual(expected_majors_table.get_string(),
                         test_repository.major_table().get_string())

        expected_student_table = PrettyTable(
            field_names=['CWID', 'Name', 'Major', 'Completed Courses', 'Remaining Required', 'Remaining Electives'])
        expected_student_table.add_row(
            [1, 'Baldwin, C', 'CS', sorted(['CS 520', 'SSW 500', 'SSW 510']), {'CS 510'}, None])
        expected_student_table.add_row(
            [2, 'Wyatt, X', 'SSW', sorted(['CS 510', 'SSW 500']), {'SSW 510', 'SSW 520', 'SSW 530', 'SSW 540'}, None])
        expected_student_table.add_row([3, 'Forbes, I', 'CS', sorted(
            ['CS 510', 'SSW 500', 'SSW 510', 'SSW 520', 'SSW 530']), {'CS 520'}, None])
        expected_student_table.add_row(
            [4, 'Erickson, D', 'SSW', sorted(['SSW 520', 'SSW 540']), {'SSW 500', 'SSW 510', 'SSW 530'}, {'CS 510', 'CS 520'}])
        expected_student_table.add_row([5, 'Chapman, O', 'CS', sorted(
            []), {'CS 510', 'CS 520'}, {'SSW 500', 'SSW 510', 'SSW 520', 'SSW 530', 'SSW 540'}])

        for expected_row, test_repository_row in zip(expected_student_table, test_repository.student_table()):
            expected_row.border = False
            expected_row.header = False
            test_repository_row.border = False
            test_repository_row.header = False
            self.assertEqual(expected_row.get_string(fields=["CWID"]).strip(),
                             test_repository_row.get_string(fields=["CWID"]).strip())
            self.assertEqual(expected_row.get_string(fields=["Name"]).strip(),
                             test_repository_row.get_string(fields=["Name"]).strip())
            self.assertEqual(expected_row.get_string(fields=["Major"]).strip(),
                             test_repository_row.get_string(fields=["Major"]).strip())
            self.assertEqual(expected_row.get_string(fields=["Completed Courses"]).strip(),
                             test_repository_row.get_string(fields=["Completed Courses"]).strip())
            self.assertEqual(set(expected_row.get_string(fields=["Remaining Required"]).strip()),
                             set(test_repository_row.get_string(fields=["Remaining Required"]).strip()))
            self.assertEqual(set(expected_row.get_string(fields=["Remaining Electives"]).strip()),
                             set(test_repository_row.get_string(fields=["Remaining Electives"]).strip()))

        expected_instructor_table = PrettyTable(
            field_names=['CWID', 'Name', 'Dept', 'Course', 'Students'])
        expected_instructor_table.add_row(
            [1, 'Einstein, A', 'CS', 'CS 510', 1])
        expected_instructor_table.add_row(
            [1, 'Einstein, A', 'CS', 'SSW 500', 3])
        expected_instructor_table.add_row(
            [1, 'Einstein, A', 'CS', 'SSW 510', 2])
        expected_instructor_table.add_row(
            [2, 'Feynman, R', 'SSW', 'CS 510', 1])
        expected_instructor_table.add_row(
            [2, 'Feynman, R', 'SSW', 'CS 520', 1])
        expected_instructor_table.add_row(
            [2, 'Feynman, R', 'SSW', 'SSW 520', 1])
        expected_instructor_table.add_row(
            [2, 'Feynman, R', 'SSW', 'SSW 530', 1])
        expected_instructor_table.add_row(
            [3, 'Newton, I', 'SSW', 'SSW 520', 1])
        expected_instructor_table.add_row(
            [4, 'Hawking, S', 'CS', 'SSW 520', 1])
        expected_instructor_table.add_row(
            [4, 'Hawking, S', 'CS', 'SSW 540', 1])
        self.assertEqual(expected_instructor_table.get_string(),
                         test_repository.instructor_table().get_string())


class TestRepositoryDB(unittest.TestCase):
    """ Test class to perform test over stevens repository with database """

    def test_create_repository_with_db(self):
        """ verify that the data retrieved from the database matches the expected rows """
        stevens_directory = '/Volumes/Macintosh HD/Users/pratik/Courses/SSW810A/PythonProject/Stevens'
        DB_FILE = '/Volumes/Macintosh HD/Users/pratik/ssw810a.db'
        stevens_repository = Repository(stevens_directory)
        self.assertEqual(stevens_repository.instructor_table().get_string(
        ), stevens_repository.instructor_table_db(DB_FILE).get_string())


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
