"""
Author: Mansi Padalia
CWID: 10442254
Assignment: Homework 9 - Test
Date: 10/23/2019
"""

import unittest
from prettytable import PrettyTable
from HW09_Mansi_Padalia import Repository, Student, Instructor, read_file_generator


class TestRpository(unittest.TestCase):
    """ Test class to perform test over university repository """

    def test_read_file_generator(self):
        """ verify the generator function to read field-separated text files and yield a tuple with all of the values from a single line in the file """
        directory = '/Volumes/Macintosh HD/Users/pratik/Courses/SSW810A/Week9'
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
        """ verify that given a directory, it creates repository instance with all students and instructor information """
        test_directory = '/Volumes/Macintosh HD/Users/pratik/Courses/SSW810A/Week9/Test'
        test_repository = Repository(test_directory)

        expected_student_table = PrettyTable(
            field_names=['CWID', 'Name', 'Completed Courses'])
        expected_student_table.add_row(
            [1, 'Baldwin, C', sorted(['SSW 500', 'SSW 510', 'CS 520'])])
        expected_student_table.add_row(
            [2, 'Wyatt, X', sorted(['SSW 500', 'CS 510', 'SSW 520'])])
        expected_student_table.add_row([3, 'Forbes, I', sorted(
            ['SSW 500', 'SSW 510', 'CS 510', 'SSW 520', 'SSW 530'])])
        expected_student_table.add_row(
            [4, 'Erickson, D', sorted(['SSW 520', 'SSW 540'])])
        expected_student_table.add_row([5, 'Chapman, O', sorted([])])
        self.assertEqual(expected_student_table.get_string(),
                         test_repository.student_table().get_string())

        expected_instructor_table = PrettyTable(
            field_names=['CWID', 'Name', 'Dept', 'Course', 'Students'])
        expected_instructor_table.add_row(
            [1, 'Einstein, A', 'CS', 'SSW 500', 3])
        expected_instructor_table.add_row(
            [1, 'Einstein, A', 'CS', 'SSW 510', 2])
        expected_instructor_table.add_row(
            [1, 'Einstein, A', 'CS', 'CS 510', 1])
        expected_instructor_table.add_row(
            [2, 'Feynman, R', 'SSW', 'CS 520', 1])
        expected_instructor_table.add_row(
            [2, 'Feynman, R', 'SSW', 'CS 510', 1])
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


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
