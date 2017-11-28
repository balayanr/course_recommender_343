from __future__ import print_function
from builtins import input
from magic_numbers import *
from Course import *
from Topic import *
from Skill import *
import operator
import re

class User:
    def __init__(self, userdata, conn):
        self.username, _, self.age, self.gender, self.country = userdata
        self.conn = conn
        cursor = conn.cursor()
        self.courses = []
        self.skills = []
        self.empty_skills = []
        self.topics = []
        self.empty_topics = []


        # Get the user's courses
        query_out = cursor.execute('select * from enrollments E, ' +
            'course_editions CE, courses C where E.edition_id = CE.edition_id '+
            'and E.username = ? and C.course_id = CE.course_id',(self.username,))
        course_tups = query_out.fetchall()
        for course_tup in course_tups:
            self.add_course(Course(course_tup))

    ## Getters
    def get_username(self):
        return self.username
    def get_age(self):
        return self.age
    def get_gender(self):
        return self.gender
    def get_country(self):
        return self.country
    def get_courses(self):
        return self.courses
    def get_course(self, idx):
        return self.courses[idx]
    def get_empty_topics(self):
        return self.empty_topics
    def get_empty_topic(self, idx):
        return self.empty_topics[idx]
    def get_topics(self):
        return self.topics
    def get_topic(self, idx):
        return self.topics[idx]
    def get_empty_skills(self):
        return self.empty_skills
    def get_empty_skill(self, idx):
        return self.empty_skills[idx]
    def get_skills(self):
        return self.skills
    def get_skill(self, idx):
        return self.skills[idx]
    def get_userdata(self):
        return (self.username, self.age, self.gender, self.country, \
                    self.courses, self.skills, self.topics, self.empty_skills,\
                    self.empty_topics)


    ## Setters (probably won't need them)
    def set_age(self, age):
        if int(age) in range(15,101): #if age not int, throws an exception
            self.age = int(age)

    def set_gender(self, gender):
        if gender ==  "Male": self.gender = 'm'
        elif gender == "Female": self.gender = 'f'
        elif gender == "N/A": self.gender = None
        else: raise Exception("Invalid input")

    def set_country(self, country):
        self.country = country

    def add_course(self, course):
        self.courses = sorted(self.courses + [course], \
                        key=operator.itemgetter(DEPT_UIDX, CNUM_UIDX, YR_UIDX))

    def add_complete_skill(self, skill):
        self.skills = sorted(self.skills + [skill], \
                        key=operator.itemgetter(DEPT_SIDX, CNUM_SIDX))

    def add_complete_topic(self, topic):
        self.topics = sorted(self.topics + [topic], \
                        key=operator.itemgetter(DEPT_TIDX, CNUM_TIDX))

    def add_empty_skill(self, skill):
        self.empty_skills = sorted(self.empty_skills + [skill], \
                        key=operator.itemgetter(DEPT_SIDX, CNUM_SIDX))

    def add_empty_topic(self, topic):
        self.empty_topics = sorted(self.empty_topics + [topic], \
                        key=operator.itemgetter(DEPT_TIDX, CNUM_TIDX))

    ## Additional functs
    def print_all(self):
        if self.get_gender() == "f": gen = "Female"
        elif self.get_gender() == "m": gen = "Male"
        else: gen = None
        print("Username: %s \nAge: %s \nGender: %s \nNative country: %s" % \
        (self.get_username(), self.get_age(), gen, self.get_country()))

    def print_topics(self):
        for topic in self.get_topics():
            topic.print_data()

    def print_skills(self):
        for skill in self.get_skills():
            skill.print_data()

    def find_skill(self, name = None, course = None):
        skills = []
        if name: #User chose to seatch by name
            for skill in self.get_empty_skills():
                if re.search(".*"+name.lower()+".*", skill.get_name().lower()):
                    skills = skills + [skill]
        elif course: #User chose to search by the course
            for skill in self.get_empty_skills():
                if skill.get_course() == course:
                    skills = skills + [skill]
        return skills

    def find_topic(self, name = None, course = None):
        topics = []
        if name: #User chose to seatch by name
            for topic in self.get_empty_topics():
                if re.search(".*"+name.lower()+".*", topic.get_name().lower()):
                    topics = topics + [topic]
        elif course: #User chose to search by the course
            for topic in self.get_empty_topics():
                if topic.get_course() == course:
                    topics = topics + [topic]
        return topics

    def remove_empty_topic(self, topic):
        try: self.empty_topics.remove(topic)
        except: pass

    def remove_empty_skill(self, skill):
        try: self.empty_skills.remove(skill)
        except: pass

    # Lets the user update their profile
    def update_profile(self):
        ans = input("Do you want to complete or update your profile?(y/n): ")
        while ans not in ['y', 'n']:
            ans = input("Please enter 'y' or 'n': ")
        if ans == 'y':
            # Update age:
            if not self.age: # no age
                print("Curnetly there is no age on your profile!")
                ans = input("Do you want to enter your age?(y/n): ")
            else: # age
                print("Curnetly your age is %d" % self.age)
                ans = input("Do you want to update your age?(y/n): ")
            while ans not in ['y', 'n']:
                ans = input("Please enter 'y' or 'n': ")
            if ans == 'y':
                age = input("Please enter your age: ")
                while True: # Check
                    try:
                        self.set_age(age)
                        break
                    except:
                        age = input("Please enter a value between 15 and 100: ")

            # Update gender
            if not self.gender:
                print("Curnetly there is no gender on your profile!")
                ans = input("Do you want to enter your gender?(y/n): ")
            else:
                gen = "Male" if self.gender == 'm' else "Female"
                print("Curretly your gender is %s" % gen)
                ans = input("Do you want to update your gender?(y/n): ")
            while ans not in ['y', 'n']:
                ans = input("Please enter 'y' or 'n': ")
            if ans == 'y':
                gender = input("Please enter your gender: ")
                while True:
                    try:
                        self.set_gender(gender)
                        break
                    except:
                        gender = \
                            input("Please enter 'Male', 'Female' or 'N/A': ")

            # Update country
            if not self.country:
                print("Curnetly there is no native country on your profile!")
                ans = input("Do you want to enter your native country?(y/n): ")
            else:
                print("Currently your native country is %s" % self.country)
                ans = input("Do you want to update it?(y/n): ")
            while ans not in ['y', 'n']:
                ans = input("Please enter 'y' or 'n': ")
            if ans == 'y':
                country = input("Please enter your native country: ")
                self.set_country(country)

            cursor = self.conn.cursor()
            try:
                qry =  "update students set age = ?, gender = ?, \
                                native_country = ? where username = ?"
                params = (self.age, self.gender, self.country, self.username)
                cursor.execute(qry, params)
            except:
                qry = "insert into students values (?,?,?,?,?)"
                params = (self.username, 0, self.age, self.gender, self.country)
                cursor.execute(qry, params)
            self.conn.commit()

    # Fetch items from the DB
    def setup_skills_and_interests(self):
        self.skills = []
        self.empty_skills = []
        self.topics = []
        self.empty_topics = []
        cursor = self.conn.cursor()
        # Get the user's interests
        qry = "select * from topic_interests TI, topics T, courses C where \
                            TI.username = ? and TI.topic_id = T.topic_id and \
                            C.course_id = TI.course_id"
        query_out = cursor.execute(qry, (self.username,))
        topic_tups = query_out.fetchall()
        for topic_tup in topic_tups:
            self.add_complete_topic(Topic(topic_tup))

        # Get the user's skills
        qry = "select * from skill_rankings SR, skills S, courses C where \
                            SR.username = ? and SR.skill_id = S.skill_id and \
                            C.course_id = SR.course_id"
        query_out = cursor.execute(qry,(self.username,))
        skill_tups = query_out.fetchall()
        for skill_tup in skill_tups:
            self.add_complete_skill(Skill(skill_tup))

        # Get unranked skills
        # Get all skills the user could have and subtract the ones they don't
        select = "select distinct CS.skill_id, CS.course_id, E.edition_id, \
                                        C.dept_code, C.course_number, S.skill"
        tables = "from course_skills CS, enrollments E, course_editions CE, \
                                        courses C , skills S"

        inner_qry = "(select distinct SR.skill_id from \
                                skill_rankings SR where SR.username = ?)"
        where = "where E.username = ? and E.edition_id = CE.edition_id and \
            CE.course_id = CS.course_id and C.course_id = CS.course_id and \
            S.skill_id = CS.skill_id and CS.skill_id not in " + inner_qry
        grouping = "group by CS.skill_id"
        qry = " ".join([select, tables, where, grouping])
        query_out = cursor.execute(qry,(self.username, self.username,))
        skill_tups = query_out.fetchall()
        for sid, cid, eid, dept, cnum, sname in skill_tups:
            self.add_empty_skill(Skill((cid, eid, None, sid, None, None, None, \
                                                sname, None, dept, cnum, None)))


        # Get unranked interests:
        select = "select distinct CT.topic_id, CT.course_id, E.edition_id, \
                                    C.dept_code, C.course_number, T.topic"
        tables = "from course_topics CT, enrollments E, course_editions CE, \
                                                    courses C , topics T"
        inner_qry = "(select distinct TI.topic_id from topic_interests TI \
                                                    where TI.username = ?)"
        where = "where E.username = ? and E.edition_id = CE.edition_id and \
                CE.course_id = CT.course_id and C.course_id = CT.course_id and \
                T.topic_id = CT.topic_id and CT.topic_id not in " + inner_qry
        grouping = "group by CT.topic_id"
        qry = " ".join([select, tables, where, grouping])
        query_out = cursor.execute(qry,(self.username, self.username))
        topic_tups = query_out.fetchall()
        for tid, cid, eid, dept, cnum, tname in topic_tups:
            self.add_empty_topic(Topic((cid, eid, None, tid, None, None, None, \
                            tname, None, dept, cnum, None)))
