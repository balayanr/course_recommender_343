from __future__ import print_function
from magic_numbers import *
import operator

class Course:
    def __init__(self, tuple):

        self.edition_id, _, self.grade, self.course_ranking, \
        self.instr_ranking, _, self.course_id, self.semester, self.year, \
        self.total_students, self.time_day, _, self.dept_code, \
        self.course_number, self.course_name = tuple

        # Used for sorting with __getitem__
        self.items = [self.edition_id, self.grade, self.course_ranking, \
        self.instr_ranking, self.course_id, self.semester, self.year, \
        self.total_students, self.time_day, self.dept_code, \
        self.course_number, self.course_name]

    def __getitem__(self, i):
        return self.items[i]

    ## Getters
    def get_eid(self):
        return self.edition_id
    def get_grade(self):
        return self.grade
    def get_course_ranking(self):
        return self.course_ranking
    def get_instr_ranking(self):
        return self.instr_ranking
    def get_cid(self):
        return self.course_id
    def get_sem(self):
        return self.semester
    def get_year(self):
        return self.year
    def get_numstd(self):
        return self.total_students
    def get_tod(self):
        return self.time_day
    def get_dept(self):
        return self.dept_code
    def get_cnum(self):
        return self.course_number
    def get_cname(self):
        return self.course_name
    def get_ccode(self):
        return self.dept_code + str(self.course_number)
    def get_old_course(self):
        return self.old
    def get_new_course(self):
        return self.new


    ## Setters
    def set_eid(self, input):
        if input == 'N/A': self.edition_id = None; return
        try:
            self.edition_id = int(input)
        except:
            raise Exception("Invalid input")

    def set_grade(self, input):
        if input == 'N/A': self.grade = None; return
        if input in GRADES:
            self.grade = input
        else:
            raise Exception("Invalid input")

    def set_course_ranking(self, input):
        if input == 'N/A': self.course_ranking = None; return
        if input in range(1,6):
            self.course_ranking = input
        else:
            raise Exception("Invalid input")

    def set_instr_ranking(self, input):
        if input == 'N/A': self.instr_ranking = None; return
        if input in range(1,6):
            self.instr_ranking = input
        else:
            raise Exception("Invalid input")

    def set_cid(self, input):
        if input == 'N/A': self.course_id = None; return
        try:
            self.course_id = int(input)
        except:
            raise Exception("Invalid input")

    def set_sem(self, input):
        if input == 'N/A': self.semester = None; return
        vals = {"Fall":"f", "Winter":"w", "Summer":"s"}
        if input in vals.keys():
            self.semester = vals[input]
        else:
            raise Exception("Invalid input")

    def set_year(self, input):
        if input == 'N/A': self.year = None; return
        try:
            self.year = int(input)
        except:
            raise Exception("Invalid input")

    def set_numstd(self, input):
        if input == 'N/A': self.total_students = None; return
        try:
            if imput > 0:
                self.total_students = int(input)
            else: raise
        except:
            raise Exception("Invalid input")

    def set_tod(self, input):
        vals = {"Morning":'m', "Afternoon":'a', "Evening":'e'}
        print("Input: %s" % input)
        if input == 'N/A': self.time_day = None
        elif input in vals.keys():
            self.time_day = vals[input]
        else:
            raise Exception("Invalid input")

    def set_dept(self, input):
        if input == 'N/A': self.dept_code = None; return
        if len(input) == 3:
            self.dept_code = input.upper()
        else:
            raise Exception("Invalid input")

    def set_cnum(self, input):
        if input == 'N/A': self.course_number = None; return
        if input >= 100 and input < 1000:
            try: self.course_number = int(input)
            except: raise Exception("Invalid input")
        else: raise Exception("Invalid input")

    def set_cname(self, input):
        if input == 'N/A': self.course_name = None; return
        # No checking I can really do. Either way, setting cname is blocked
        self.course_name = input


    ## Additional functs

    '''
    Prints out the data about the course.
    long - if True, prints out all available information about the course
    '''
    def print_data(self, long = False, rows = False):
        cr = "Course ranking: %s" % self.course_ranking if self.course_ranking else "Course ranking: N/A"
        gr = "Grade: %s" % self.grade if self.grade else "Grade: N/A"
        ir = "Instructor ranking: %s" % self.instr_ranking if self.instr_ranking else "Instructor ranking: N/A"

        if self.semester == 'f': sem = "Fall"
        elif self.semester == 'w': sem = "Winter"
        elif self.semester == 's': sem = "Summer"
        else: sem =  "Semester: N/A"

        yr = "%s" % self.year if self.year else "Year: N/A"

        stdnum = "Number of students: %s" % self.total_students if self.total_students else "Number of students: N/A"

        if self.time_day == 'm': tod = "Morning Section"
        elif self.time_day == 'a': tod = "Afternoon Section"
        elif self.time_day == 'e': tod = "Evening Section"
        else: tod = "Time of day: N/A"

        crnm = "Course Name: %s " % self.course_name if self.course_name else "Course Name: N/A"

        print("%s%s %-14s%-25s%s" % (self.dept_code,self.course_number, (sem + ' ' + yr),tod,gr))
        if long:
            if rows:
                print("   %-21s%-25s%s" % (cr, ir, stdnum))
                print("   %s" % crnm)
            else:
                print("%-21s%-23s%s" % (cr, ir, stdnum))
                print(crnm)

    def print_edition(self, rows = False):
        if self.semester == 'f': sem = "Fall"
        elif self.semester == 'w': sem = "Winter"
        elif self.semester == 's': sem = "Summer"
        else: sem =  "Semester: N/A"

        yr = "%s" % self.year if self.year else "Year: N/A"

        stdnum = "Number of students: %s" % self.total_students if self.total_students else "Number of students: N/A"

        if self.time_day == 'm': tod = "Morning Section"
        elif self.time_day == 'a': tod = "Afternoon Section"
        elif self.time_day == 'e': tod = "Evening Section"
        else: tod = "Time of day: N/A"

        crnm = "Course Name: %s " % self.course_name if self.course_name else "Course Name: N/A"

        print("%-8s %-14s%-20s%s" % (self.get_ccode(), (sem + ' ' + yr),tod,stdnum))
        if self.course_name:
            if rows:
                print("    %s" % crnm)
            else:
                print(crnm)
