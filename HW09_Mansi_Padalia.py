"""
Author: Mansi Padalia
CWID: 10442254
Assignment: Homework 9
Date: 10/28/2019
"""

from collections import defaultdict
import os
from prettytable import PrettyTable


class Repository():
    """ stores students, instructors, grades and majors for a university """
    students = dict()
    instructors = dict()
    majors = dict()

    def __init__(self, directory):
        """ initializes the directory path for the university and reads the students, instructors, grades and majors files """
        self.directory = directory
        try:
            self.get_majors()
            self.get_students()
            self.get_instructors()
            self.get_grades()
        except Exception as err:
            raise err

    def get_students(self):
        """ reads the students file for the university and stored it in repository """
        student_records = read_file_generator(
            self.directory, 'students.txt', 3, ';', True)
        for cwid, name, major in student_records:
            if major in self.majors.keys():
                self.students[cwid] = Student(cwid, name, major)
            else:
                raise ValueError(
                    f"{major} is not a recognized major in 'major.txt' file.")

    def get_instructors(self):
        """ reads the instructors file for the university and stored it in repository """
        instructor_records = read_file_generator(
            self.directory, 'instructors.txt', 3, '|', True)
        for cwid, name, department in instructor_records:
            self.instructors[cwid] = Instructor(cwid, name, department)

    def get_grades(self):
        """ reads the grades file for the university and link it with students and instructors in repository """
        grade_records = read_file_generator(
            self.directory, 'grades.txt', 4, '|', True)
        for student_cwid, course, letter_grade, instructor_cwid in grade_records:
            if student_cwid in self.students.keys():
                self.students[student_cwid].student_courses = (
                    course, letter_grade)
                if instructor_cwid in self.instructors.keys():
                    self.instructors[instructor_cwid].instructor_courses = course
                else:
                    raise ValueError(
                        f"{instructor_cwid} is not a recognized instructor in 'instructor.txt' file.")
            else:
                raise ValueError(
                    f"{student_cwid} is not a recognized student in 'students.txt' file.")

    def get_majors(self):
        """ reads the majors file for the university and stored it in repository """
        major_records = read_file_generator(
            self.directory, 'majors.txt', 3, '\t', True)
        for major, reflag, course in major_records:
            if major not in self.majors:
                self.majors[major] = Major(major)
            if reflag in ('r', 'R'):
                self.majors[major].required_courses = course
            elif reflag in ('e', 'E'):
                self.majors[major].elective_courses = course

    def major_table(self):
        """ prints out the pretty table for majors """
        major_table = PrettyTable(
            field_names=['Dept', 'Required', 'Electives'])
        for dept, major in self.majors.items():
            major_table.add_row(
                [dept, sorted(list(major.required_courses)), sorted(list(major.elective_courses))])
        return major_table

    def student_table(self):
        """ prints out the pretty table for students """
        student_table = PrettyTable(
            field_names=['CWID', 'Name', 'Major', 'Completed Courses', 'Remaining Required', 'Remaining Electives'])
        for cwid, student in self.students.items():
            completed_courses, remaining_required, remaining_elective = self.majors[student.major].remaining_courses(
                student.student_courses)
            student_table.add_row(
                [cwid, student.name, student.major, sorted(completed_courses), remaining_required, remaining_elective])
        return student_table

    def instructor_table(self):
        """ prints out the pretty table for instructors """
        instructor_table = PrettyTable(
            field_names=['CWID', 'Name', 'Dept', 'Course', 'Students'])
        for cwid, instructor in self.instructors.items():
            for course in instructor.instructor_courses:
                instructor_table.add_row(
                    [cwid, instructor.name, instructor.department, course, instructor.instructor_courses[course]])
        return instructor_table


class Student:
    """ a class to store student information"""

    def __init__(self, cwid, name, major):
        """ stores student's basic information while creation of an object """
        self.cwid = cwid
        self.name = name
        self.major = major
        self._student_courses = defaultdict(str)

    @property
    def student_courses(self):
        """ experimenting with @property annotation to return all course names for a student """
        return self._student_courses

    @student_courses.setter
    def student_courses(self, course_grade):
        """ experimenting with @attribute.setter annotation to save course grades tuple(course, grade) for a student """
        try:
            course, grade = course_grade
        except ValueError:
            raise ValueError(
                "Pass an iterable with two items (course and grade) ")
        else:
            """ This will run only if no exception was raised """
            self._student_courses[course] = grade

    def __str__(self):
        """ returns student's cwid and name as a string """
        return "<student: {} {}>".format(self.cwid, self.name)


class Instructor:
    """ a class to store instructor information"""

    def __init__(self, cwid, name, department):
        """ stores instructor's basic information while creation of an object """
        self.cwid = cwid
        self.name = name
        self.department = department
        self._instructor_courses = defaultdict(int)

    @property
    def instructor_courses(self):
        """ experimenting with @property annotation to return dictionary of course names and no. of students for an instructor """
        return self._instructor_courses

    @instructor_courses.setter
    def instructor_courses(self, course):
        """ experimenting with @attribute.setter annotation to save no. of students for a course for an instructor """
        self._instructor_courses[course] += 1

    def __str__(self):
        """ returns instructor's cwid and name as a string """
        return "<instructor: {} {}>".format(self.cwid, self.name)


class Major:
    """ a class to store majors related information"""

    def __init__(self, major):
        """ stores instructor's basic information while creation of an object """
        self.major = major
        self._required_courses = set()
        self._elective_courses = set()

    @property
    def required_courses(self):
        """ experimenting with @property annotation to return set of required courses for a major """
        return self._required_courses

    @required_courses.setter
    def required_courses(self, course):
        """ experimenting with @attribute.setter annotation to add course to required courses for a major """
        self._required_courses.add(course)

    @property
    def elective_courses(self):
        """ experimenting with @property annotation to return set of elective courses for a major """
        return self._elective_courses

    @elective_courses.setter
    def elective_courses(self, course):
        """ experimenting with @attribute.setter annotation to add course to elective courses for a major """
        self._elective_courses.add(course)

    def remaining_courses(self, student_courses):
        """ return a tuple of completed courses, remaining required courses and remaining elective courses for a student with a given major"""
        student_required = self.required_courses.copy()
        student_elective = self.elective_courses.copy()
        student_completed = list(student_courses.keys()).copy()
        passing_grades = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']
        for course, grade in student_courses.items():
            if grade in passing_grades:
                if course in student_required:
                    student_required.remove(course)
                elif course in student_elective:
                    student_elective = set()
            else:
                student_completed.remove(course)
        return student_completed, student_required if student_required else None, student_elective if student_elective else None

    def __str__(self):
        """ returns major with its required and elective courses as a string """
        return "<major: {}, required courses: {}, elective courses: {}>".format(self.major, ", ".join(list(self.required_courses)), ", ".join(list(self.elective_courses)))


def read_file_generator(directory, filename, fields, sep='\t', header=False):
    """ a generator function to read field-separated text files and yield a tuple with all of the values from a single line in the file """
    path = os.path.join(directory, filename)
    try:
        fp = open(path, 'r')  # try to open the file in read mode
    except FileNotFoundError:
        # raise an exception if file cannot be opened in read mode
        raise FileNotFoundError(f"Can't open {path}")
    else:
        with fp:
            line_number = 0  # initilaze counter for counting lines to 0
            for line in fp:
                line_number += 1  # keep incremeting the line number with each line
                # replace the newline character and split by separator
                words_list = line.strip().split(sep)
                # if number of fields expected is not equal to the one generated by spliting separator then raise error
                if len(words_list) != fields:
                    raise ValueError(
                        f"{path} has {len(words_list)} fields on line {line_number} but expected {fields}")
                # if there is a header line then skip it and don't yield
                if(header and line_number == 1):
                    continue
                yield(tuple(words_list))


def main():
    """ framework for the project to summarize student and instructor data """
    stevens_directory = '/Volumes/Macintosh HD/Users/pratik/Courses/SSW810A/PythonProject/Stevens'
    try:
        stevens_repository = Repository(stevens_directory)
        print("Majors Summary")
        print(stevens_repository.major_table())
        print("Student Summary")
        print(stevens_repository.student_table())
        print("Instructor Summary")
        print(stevens_repository.instructor_table())
    except Exception as err:
        print(f"{err.__class__.__name__}: {err}")


if __name__ == "__main__":
    main()
