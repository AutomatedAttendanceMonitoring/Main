import psycopg2
import datetime


class Cursor:
    def __init__(self):
        self.conn = psycopg2.connect(dbname='fse_db', 
                                user='fseteam', 
                                password='1q2w3e4r', 
                                host='127.0.0.1'
                                )
        self.cursor = self.conn.cursor()
    
    def add_student_in_db(self, email, fname, lname, year):
        """Add new student in db

        Args:
            email (str): e-mail of new student 
            fname (str): first name of new student
            lname (str): last name of new student
            year (str): year of education of new student
        """
        self.cursor.execute("INSERT INTO students VALUES ('{}', '{}', '{}', '{}');". \
                            format(
                                email, 
                                fname, 
                                lname, 
                                year
                                )
                            )
    
    def get_list_of_student_names(self):
        """Function to get all students information for each student

        Returns:
            cursor: iterative list of corteges with student information
        """
        self.cursor.execute('SELECT {}, {}, {}, {} FROM students'. \
                            format('student.email', 
                                   'students.FName', 
                                   'students.LName', 
                                   'students.year_of_education')
                            )
        return self.cursor
    
    def get_lesson(self, instructor_name):
        """Function to get list of lessons of instructor by his name
        
        Args:
            instructor_name (str): name of instructor
            
        Returns:
            cursor: iterative list of corteges with lesson id information
        """
        self.cursor.execute("""SELECT lessons.id FROM lessons
                            INNER JOIN subjects
                            ON lessons.subject=subjects.id
                            INNER JOIN is_taught_by
                            ON subjects.id=is_taught_by.subject
                            INNER JOIN instructors
                            ON instructors.id=is_taught_by.instructor
                            WHERE instructors.name='{}';""".format(instructor_name))
        return self.cursor
        
    def mark_student_attendance(self, lesson_id, student_id):
        """Function to mark student attendance.
            the automated attendance and manually attendance is execute by this function
            
        Args:
            lesson_id (uuid): id of lesson in which student is present
            student_id (str): e-mail of student that should be marked as present
            
        Returns:
        """
        self.cursor.execute('INSERT INTO is_present VALUES ({}, {})'.format(lesson_id, student_id))
        
    def clear_lessons(self):
        """Function to clear lesson table after export data in moodle
        """
        self.cursor.execute('DELETE FROM lessons;')
        self.cursor.execute('DELETE FROM is_present;')

    def add_lesson(self, start_time, end_time, kind, subject):
        """Function to add new lesson

        Args:
            start_date (str): [description]
            end_time (str): [description]
            kind (str): [description]
            subject (uuid): id of subject
        """
        start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f') 
        end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S.%f') 
        self.cursor.execute('INSERT INTO lessons VALUES (uuid_generate_v4(), {}, {}, {}, {})'. \
                            format(
                                start_time,
                                end_time, 
                                kind,
                                subject
                                )
                            )
        
    def add_instructor(self, name):
        """Function to add new instuctor

        Args:
            name (str): name of instructor
        """
        self.cursor.execute('INSERT INTO instructors VALUES (uuid_generate_v4(), {})'.format(name))
    
    def add_subject(self, name, year):
        """Function to add new subject

        Args:
            name (str): name of new subject
            year (str): year of student for new subject
        """
        self.cursor.execute('INSERT INTO subjects VALUES (uuid_generate_v4(), {}, {})'.
                            format(
                                name,
                                year
                            )
                            )