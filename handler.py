from __future__ import print_function
from builtins import input
from magic_numbers import *
from User import *
from Course import *
import numpy as np


def confirm_row(idx, row):
    while True:
        try:
            if idx == "cancel": return None
            elif (int(idx) > 0 and int(idx) - 1 <= row): return int(idx)
            else: raise
        except: idx = input("Please choose the course (1 to %d) or enter 'cancel' to stop: " % (row+1))


class Handler:
    def __init__(self, user, conn):
        self.conn = conn
        self.user = user
        # self.all_courses = []

    '''
    # This is me revieqing the code in 2017: these functions were untested back when I worked on the project, but I'll leave the code anyway
    def list_all_courses(self):
        if not self.all_courses:
            cursor = self.conn.cursor()
            query_out = cursor.execute('select * from course_editions CE, '+
                                'courses C where C.course_id = CE.course_id')
            course_tups = query_out.fetchall()
            for course_tup in course_tups:
                self.all_courses = sorted(self.all_courses + [Course(course_tup)], \
                            key=operator.itemgetter(DEPT_CIDX, CNUM_CIDX, YR_CIDX))
        for row, course in enumerate(self.all_courses):
            print('%-3s' % (str(row+1) + ':'), end = '')
            course.print_data(rows = True)
            if((row+1)%15 == 0 and (row+1) != len(self.all_courses):
                rem = len(self.all_courses) - row - 1
                cont = input("%d more courses. Show next %d?(y/n): " % (rem, min(rem, 15)) )
                if cont == "n": break
        return 1

    #list recorded courses
    def list_courses(self, long = False):
        for row, course in enumerate(self.user.get_courses()):
            print('%-3s' % (str(row+1) + ':'), end = '')
            course.print_data(long = long, rows = True)
            if((row+1)%15 == 0 and (row+1) != len(self.user.get_courses())):
                rem = len(self.user.get_courses()) - row - 1
                cont = input("%d more courses. Show next %d?(y/n): " % (rem, min(rem, 15)) )
                if cont == "n": break
        return 1
    '''
    # rate skill
    def rate_skills(self):
        while self.user.get_empty_skills():
        # 1) search skill or choose from a list
            while True:
                ans = input("Do you want to search for a skill or pick from a list?\n(search/pick/cancel): ")

                while ans not in ["search", "pick", "cancel"]: ans = input("Please enter 'search', 'pick' or 'cancel': ")

                if ans == "search": skill = self.search_skill();
                elif ans == "pick": skill = self.choose_skill();
                else: return

                if not skill:
                    ans = input("Do you want find the skill another way?(y/n): ")
                    while ans not in ['y', 'n']: ans = input("Please enter 'y' or 'n': ")
                    if ans == 'n': return
                    else: continue
                else: break
        # 2) rate
            before = input("Please enter your proficiency in %s before you took the course(1-5): " % skill.get_name())
            while True:
                try:
                    if int(before) in range(1,6): break
                    else: raise
                except: before = input("Invalid input! Please enter a number between 1 and 5: ")

            after = input("Please enter your proficiency in %s after you took the course(1-5): " % skill.get_name())
            while True:
                try:
                    if int(after) in range(1,6): break
                    else: raise
                except: after = input("Invalid input! Please enter a number between 1 and 5: ")

            try:
                cursor = self.conn.cursor()
                cursor.execute("insert into skill_rankings values (?,?,?,?,?,?)", (skill.get_cid(), skill.get_eid(), self.user.get_username(), skill.get_sid(), before, after))
                self.user.remove_empty_skill(skill)
                skill.set_rank_before(before)
                skill.set_rank_after(after)
                self.user.add_complete_skill(skill)
                self.conn.commit()
            except Exception as inst:
                print(type(inst))    # the exception instance
                print(inst.args)     # arguments stored in .args
                print(inst)

        # 3) repeat
            ans = input("Do you want to rate another skill?(y/n): ")
            while ans not in ["y", "n"]: ans = input("Please enter 'y' or 'n': ")
            if ans == "n": return
        print("You rated all available skills! Thank you!")

    def search_skill(self):
        # Select mode
        ans = input("Do you want to search by the course or by the name of the skill?(course/name): ")
        while ans not in ["course", "name"]: #check input
            ans = input("Please enter 'course' or 'name': ")

        if ans == "course":
            while True:
                crs = input("Enter the course code (i.e. CSC343): ")
                skills = self.user.find_skill(course = crs)
                if not skills: #nothing found
                    ans = input("No skills were found with that course. Search again?(y/n): ")
                    while ans not in ["y", "n"]:
                        ans = input("Please enter 'y' or 'n': ")
                    if ans == 'n': break
                else: #something found
                    break

        # ans == "name"
        else:
            while True:
                kwd = input("Enter the skill's name or a keyword: ")
                while not kwd:
                    kwd = input("Please enter a keyword: ")
                skills = self.user.find_skill(name = kwd)
                if not skills:
                    ans = input("No skills were found with that keyword. Search again?(y/n): ")
                    while ans not in ["y", "n"]:
                        ans = input("Please enter 'y' or 'n': ")
                    if ans == 'n': break
                else: # skills found
                    break

        if ans == 'n': return None
        else: # Successfully found courses
            print("%d skill(s) found!" % len(skills))
            if len(skills) == 1:
                ans = raw_data("Is %s the skill you were searching for?(y/n): " % skills[0].get_name())
                while ans not in ['y', 'n']: ans = raw_data("Please enter 'y' or 'n': ")
                if ans == 'y': return skills[0] #Only one skill found, return it
                else: return None

            for row, skill in enumerate(skills):
                print('%-3s' % (str(row+1) + ':'), end = '')
                skill.print_data(rows = True)
                if((row+1)%15 == 0 and len(skills) != row+1):
                    rem = len(skills) - row - 1
                    cont = input("%d more skills. Show next %d?(y/n): " % (rem, min(rem, 15)) )
                    while cont not in ['y', 'n']: cont = input("Please enter 'y' or 'n': ")
                    if cont == 'n': break

            while True:
                try:
                    idx = int(input("Please choose the skill (1 to %d) or enter 'cancel' to stop: " % (int(row)+1)))
                    if idx == "cancel": return None
                    elif (int(idx) > 0 and idx <= row): break
                    else: raise
                except: print("Invalid input! Please try again!")
            return skills[idx-1]

    def choose_skill(self):
        skills = []
        print("These are all skills you haven't reviewed:")
        for row, skill in enumerate(self.user.get_empty_skills()):
            print('%-3s' % (str(row+1) + ':'), end = '')
            skill.print_data(rows = True)
            skills = skills + [skill]
            if((row+1)%15 == 0 and len(self.user.get_empty_skills()) != row+1):
                rem = len(self.user.get_empty_skills()) - row - 1
                cont = input("%d more skills. Show next %d?(y/n): " % (rem, min(rem, 15)) )
                while cont not in ['y', 'n']: cont = input("Please enter 'y' or 'n': ")
                if cont == "n": break

        if len(skills) == 1: return skills[0] #Only one course found, return it
        while True:
            try:
                idx = input("Please choose the skill (1 to %d) or enter 'cancel' to stop: " % (row+1))
                if idx == "cancel": return None
                elif (int(idx) > 0 and int(idx) - 1 <= row): break
                else: raise
            except: print("Invalid input! Please try again!")
        return skills[int(idx)-1]


    # rate topic
    def rate_topics(self):
        while self.user.get_empty_topics():
        # 1) search topic or choose from a list
            while True:
                ans = input("Do you want to search for a topic or pick from a list?(search/pick/cancel): ")

                while ans not in ["search", "pick", "cancel"]: ans = input("Please enter 'search', 'pick' or 'cancel': ")

                if ans == "search": topic = self.search_topic();
                elif ans == "pick": topic = self.choose_topic();
                else: return

                if not topic:
                    ans = input("Do you want find the topic another way?(y/n): ")
                    while ans not in ['y', 'n']: ans = input("Please enter 'y' or 'n': ")
                    if ans == 'n': return
                    else: continue
                else: break
        # 2) rate
            before = input("Please enter your proficiency in %s before you took the course(1-5): " % topic.get_name())
            while True:
                try:
                    if int(before) in range(1,6): break
                    else: raise
                except: before = input("Invalid input! Please enter a number between 1 and 5: ")

            after = input("Please enter your proficiency in %s after you took the course(1-5): " % topic.get_name())
            while True:
                try:
                    if int(after) in range(1,6): break
                    else: raise
                except: after = input("Invalid input! Please enter a number between 1 and 5: ")

            try:
                cursor = self.conn.cursor()
                cursor.execute("insert into topic_interests values (?,?,?,?,?,?)", (topic.get_cid(), topic.get_eid(), self.user.get_username(), topic.get_tid(), before, after))
                self.user.remove_empty_topic(topic)
                topic.set_int_before(before)
                topic.set_int_after(after)
                self.user.add_complete_topic(topic)
                self.conn.commit()
            except Exception as inst:
                print(type(inst))    # the exception instance
                print(inst.args)     # arguments stored in .args
                print(inst)

        # 3) repeat
            ans = input("Do you want to rate another topic?(y/n): ")
            while ans not in ["y", "n"]: ans = input("Please enter 'y' or 'n': ")
            if ans == "n": return
        print("You rated all available topics! Thank you!")

    def search_topic(self):
        # Select mode
        ans = input("Do you want to search by the course or by the name of the topic?(course/name): ")
        while ans not in ["course", "name"]: #check input
            ans = input("Please enter 'course' or 'name': ")

        if ans == "course":
            while True:
                crs = input("Enter the course code (i.e. CSC343): ")
                topics = self.user.find_topic(course = crs)
                if not topics: #nothing found
                    ans = input("No topics were found with that course. Search again?(y/n): ")
                    while ans not in ["y", "n"]:
                        ans = input("Please enter 'y' or 'n': ")
                    if ans == 'n': break
                else: #something found
                    break

        # ans == "name"
        else:
            while True:
                kwd = input("Enter the topic's name or a keyword: ")
                while not kwd:
                    kwd = input("Please enter a keyword: ")
                topics = self.user.find_topic(name = kwd)
                if not topics:
                    ans = input("No topics were found with that keyword. Search again?(y/n): ")
                    while ans not in ["y", "n"]:
                        ans = input("Please enter 'y' or 'n': ")
                    if ans == 'n': break
                else: # topics found
                    break

        if ans == 'n': return None
        else: # Successfully found courses
            print("%d topic(s) found!" % len(topics))
            if len(topics) == 1:
                ans = raw_data("Is %s the topic you were searching for?(y/n): " % topics[0].get_name())
                while ans not in ['y', 'n']: ans = raw_data("Please enter 'y' or 'n': ")
                if ans == 'y': return topics[0] #Only one topic found, return it
                else: return None

            for row, topic in enumerate(topics):
                print('%-3s' % (str(row+1) + ':'), end = '')
                topic.print_data(rows = True)
                if((row+1)%15 == 0 and len(topics) != row+1):
                    rem = len(topics) - row - 1
                    cont = input("%d more topics. Show next %d?(y/n): " % (rem, min(rem, 15)) )
                    while cont not in ['y', 'n']: cont = input("Please enter 'y' or 'n': ")
                    if cont == 'n': break

            while True:
                try:
                    idx = int(input("Please choose the topic (1 to %d) or enter 'cancel' to stop: " % (int(row)+1)))
                    if idx == "cancel": return None
                    elif (int(idx) > 0 and idx <= row): break
                    else: raise
                except: print("Invalid input! Please try again!")
            return topics[idx-1]

    def choose_topic(self):
        topics = []
        print("These are all topics you haven't reviewed:")
        for row, topic in enumerate(self.user.get_empty_topics()):
            print('%-3s' % (str(row+1) + ':'), end = '')
            topic.print_data(rows = True)
            topics = topics + [topic]
            if((row+1)%15 == 0 and len(self.user.get_empty_topics()) != row+1):
                rem = len(self.user.get_empty_topics()) - row - 1
                cont = input("%d more topics. Show next %d?(y/n): " % (rem, min(rem, 15)) )
                while cont not in ['y', 'n']: cont = input("Please enter 'y' or 'n': ")
                if cont == "n": break

        if len(topics) == 1: return topics[0] #Only one course found, return it
        while True:
            try:
                idx = input("Please choose the topic (1 to %d) or enter 'cancel' to stop: " % (row+1))
                if idx == "cancel": return None
                elif (int(idx) > 0 and int(idx) - 1 <= row): break
                else: raise
            except: print("Invalid input! Please try again!")
        return topics[int(idx)-1]


    #Add course
    def add_courses(self):
        courses = self.get_unused_courses()
        while courses:
            # 1) pick a course:
            while True:
                mode = input("Do you want to search for a course by its code or select it from a list?\n(search/list/cancel): ")
                while mode not in ['search', 'list', 'cancel']: mode = input("Please enter 'search', 'list' or 'cancel': ")
                if mode == 'cancel': return
                elif mode == 'list': course = self.choose_from_list(courses)
                else: course = self.search_by_code(courses)

                if not course:
                    ans = input("Do you want to search another way?(y/n): ")
                    while ans not in ['y', 'n']: ans = input("Please enter 'y' or 'n': ")
                    if ans == 'n': return
                    else: continue
                else: break

            # 2) Pick an edition
            editions = self.get_course_editions(course)
            if not editions: # no editions
                print("Sorry, the chosen course has no editions in the database!")
                ans = input("Do you want to search for another course?(y/n): ")
                while ans not in ['y', 'n']: ans = input("Please enter 'y' or 'n': ")
                if ans == 'n': return
                else: continue
            else:
                print("You chose %s%d! Here are all editions of the course: " % (course[1], course[2]))
                for row, course in enumerate(editions): # print editions
                    print('%-3s' % (str(row+1) + ':'), end = '')
                    course.print_edition(rows = True)
                    if((row+1)%15 == 0 and (row+1) != len(editions)):
                        rem = len(self.user.get_courses()) - row - 1
                        cont = input("%d more courses. Show next %d?(y/n): " % (rem, min(rem, 15)) )
                        if cont == "n": break
                if len(editions) == 1:
                    ans = input("Is this the edition you were looking for?(y/n): ")
                    while ans not in ['y', 'n']: ans = input("Please enter 'y' or 'n': ")
                    if ans == 'y':
                        edition = editions[0]
                    else:
                        ans = input("Do you want to search another way?(y/n): ")
                        while ans not in ['y', 'n']: ans = input("Please enter 'y' or 'n': ")
                        if ans == 'n': return
                        else: continue
                else:
                    idx = input("Please enter the row of the edition you want to add or 'cancel': ")
                    idx = confirm_row(idx, row)
                    if not idx: continue
                    else: edition = editions[idx-1]

            # 3) complete
            print("These are the things you can complete about this course: \nCourse Ranking, Instructor Ranking, Course Grade.")
            crank = input("Please enter the course ranking(1-5) or 'skip': ")
            while True: # check input
                if crank == 'skip': break
                try:
                    if int(crank) not in range(1,6):
                        crank = input("Please enter a number between 1 and 5 or 'skip': ")
                    else:
                        edition.set_course_ranking(int(crank))
                        break
                except: pass

            irank = input("Please enter the instructor ranking(1-5) or 'skip': ")
            while True: # check input
                if irank == 'skip': break
                try:
                    if int(irank) not in range(1,6):
                        irank = input("Please enter a number between 1 and 5 or 'skip': ")
                    else:
                        edition.set_instr_ranking(int(irank))
                        break
                except: pass

            grade = input("Please enter the grade you received  or 'skip': ")
            while grade.upper() not in ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "F", 'skip']: grade = input("Please enter a letter grade (i.e. 'A+') or 'skip': ")
            if grade != 'skip': edition.set_grade(grade)

            cursor = self.conn.cursor()
            try:
                cursor.execute("insert into enrollments values(?,?,?,?,?)", \
                (edition.get_eid(), self.user.get_username(), edition.get_grade(),\
                edition.get_course_ranking(), edition.get_instr_ranking()))
            except:
                cursor.execute("update enrollments set letter_grade = ?, course_ranking = ?, instr_ranking = ? where edition_id = ? and username = ? ", \
                (edition.get_grade(), edition.get_course_ranking(), edition.get_instr_ranking(),
                edition.get_eid(), self.user.get_username()))
            self.conn.commit()
            self.user.add_course(edition)
            courses.remove((course.get_cid(), course.get_dept(), course.get_cnum(), course.get_cname()))

            #"Do you want to search for another course?"
            ans = input("Do you want to add another course??(y/n): ")
            while ans not in ["y", "n"]: ans = input("Please enter 'y' or 'n': ")
            if ans == "n": return
        print("You added all available courses! Thank you!")

    def get_unused_courses(self):
        cursor = self.conn.cursor()
        query = cursor.execute("select * from courses where course_id not in (select course_id from enrollments E, course_editions CE where E.username = ? and E.edition_id = CE.edition_id) order by dept_code", (self.user.get_username(),))
        return query.fetchall()

    def get_course_editions(self, course):
        editions = []
        cursor = self.conn.cursor()
        query = cursor.execute("select * from course_editions CE where CE.course_id = ?", (course[0],))
        for eid, cid, sem, year, studnum, tod in query.fetchall():
            editions = editions + [Course((eid, None, None, None, None, None, cid, sem, year, studnum, tod, None, course[1], course[2], course[3]))]
        return editions


    def choose_from_list(self, courses):
        for row, course in enumerate(courses):
            name = course[3] if course[3] else ''
            print("%-3s%s%d%s" % (str(row+1)+':', course[1], course[2], name))
            if((row+1)%15 == 0 and len(courses) != row+1):
                rem = len(courses) - row - 1
                cont = input("%d more courses. Show next %d?(y/n): " % (rem, min(rem, 15)) )
                while cont not in ['y', 'n']: cont = input("Please enter 'y' or 'n': ")
                if cont == "n": break
        idx = input("Please choose the edition (1 to %d) or enter 'cancel' to stop: " % (row+1))
        idx = confirm_row(idx, row)
        if not idx:
            return None
        else:
            return courses[int(idx)-1]


    def search_by_code(self, courses):
        while True:
            kwd = input("Please enter any part of the course code (i.e. 'CSC' or 'MAT235' or '343'): ")
            matched_courses = []
            for course in courses:
                if re.findall('.*'+kwd.lower()+'.*', (course[1] + str(course[2])).lower() ):
                    matched_courses = matched_courses + [course]
            if len(matched_courses) == 0:
                ans = input("No courses found. Search again?(y/n): ")
                while ans not in ['y', 'n']: ans = input("Please enter 'y' or 'n': ")
                if ans == 'n':
                    return None
                else:
                    continue
            else:
                print("%d course(s) cound!" % len(matched_courses))
                for row, course in enumerate(matched_courses):
                    print("%-3s%s%s" %(str(row+1)+':', course[1], course[2]))
                    if( (row+1)%15 == 0 and len(matched_courses) != row+1):
                        rem = len(matched_courses) - row - 1
                        cont = input("%d more courses. Show next %d?(y/n): " % (rem, min(rem, 15)) )
                        while cont not in ['y', 'n']: cont = input("Please enter 'y' or 'n': ")
                        if cont == "n": break
                if len(matched_courses) == 1:
                    ans = input("Is this the course you were looking for?(y/n): ")
                    while ans not in ['y', 'n']: ans = input("Please enter 'y' or 'n': ")
                    if ans == 'y':
                        return matched_courses[0]
                    else:
                        ans = input("Search again?(y/n): ")
                        while ans not in ['y', 'n']: ans = input("Please enter 'y' or 'n': ")
                        if ans == 'n':
                            return None
                        else:
                            continue


                idx = input("Please choose the course (1 to %d) or enter 'cancel' to stop: " % (row+1))
                idx = confirm_row(idx, row)
                if not idx:
                    return None
                else:
                    return matched_courses[int(idx)-1]





    # Create distance table:
    def create_table(self):
        cursor = self.conn.cursor()
        #get skill matches. edition_id to allow different reviews of the same skill with the same ranks
        users_with_skills = cursor.execute("select distinct username, skill_id, rank_before, rank_after, edition_id from skill_rankings where skill_id in (select skill_id from skill_rankings where username = ?) and username != ?", (self.user.get_username(),self.user.get_username(),)).fetchall()
        users_with_skills = np.asarray(users_with_skills)
        #get topic matches
        users_with_topics = cursor.execute("select distinct username, topic_id, interest_before, interest_after, edition_id from topic_interests where topic_id in (select topic_id from topic_interests where username = ?) and username != ?", (self.user.get_username(),self.user.get_username(),)).fetchall()
        users_with_topics = np.asarray(users_with_topics)

        # numbers for the table
        num_male = cursor.execute("select count(*) from students where gender = 'm'").fetchall()[0][0]
        num_female = cursor.execute("select count(*) from students where gender = 'f'").fetchall()[0][0]
        avg_age = cursor.execute("select avg(age) from students").fetchall()[0][0]

        #get user demographics
        usernames = list(set(np.append(users_with_skills[:,0], users_with_topics[:,0]))) #to get unique usernames
        users = []
        for username in usernames:
            tup = cursor.execute("select * from students where username = ?", (username,)).fetchall()[0]
            users = users + [User(tup, self.conn)]
        table = np.zeros((len(users), len(self.user.get_skills()) + len(self.user.get_skills()) + 9))
        for i, user in enumerate(users):
            table[i,0] = i #index in users, so that I can dig up the user later

            # age difference: distance = absolute age difference
            if self.user.get_age() and user.get_age():
                table[i,1] = abs(user.get_age() - self.user.get_age())
            elif self.user.get_age() and not user.get_age():
                table[i,1] = abs(avg_age - self.user.get_age())
            elif not self.user.get_age() and user.get_age():
                table[i,1] = abs(avg_age - user.get_age())
            #else 0 - default

            # gender match: distance = 0 if same gender
            if self.user.get_gender() and user.get_gender():
                table[i,2] = 0 if self.user.get_gender() == user.get_gender() else 1
            elif self.user.get_gender() and not user.get_gender():
                table[i,2] = num_male/(num_male+num_female) if self.user.get_gender() == 'm' else    num_female/(num_male+num_female)


            # country match: distance =  0 if same country
            if self.user.get_country() != user.get_country():
                table[i,3] = 1

            for j, skill in enumerate(self.user.get_skills()):
                users_review = cursor.execute("select avg(rank_before) from skill_rankings where username = ? and skill_id = ?", (user.get_username(), skill.get_sid())).fetchall()[0][0]
                main_review = cursor.execute("select avg(rank_before) from skill_rankings where username = ? and skill_id = ?", (self.user.get_username(), skill.get_sid())).fetchall()[0][0]

                table[i,j+4] = abs(users_review - main_review)  if users_review else 5


            for k, topic in enumerate(self.user.get_topics()):
                users_review = cursor.execute("select avg(interest_before) from topic_interests where username = ? and topic_id = ?", (user.get_username(), topic.get_tid())).fetchall()[0][0]
                main_review = cursor.execute("select avg(interest_before) from topic_interests where username = ? and topic_id = ?", (self.user.get_username(), topic.get_tid())).fetchall()[0][0]

                table[i,j+k+5] = abs(users_review - main_review)  if users_review else 5
            table[i,-1] = np.sum(table[i,1:])

        self.table = table[table[:,-1].argsort()][:NUM_NEIGHBOURS+1]
        self.nearest_users = users
        self.nearest_usernames = [str(usernames[int(i)]) for i in self.table[:,0]]


    # Get courses for each user
    def get_nearest_courses(self):
        cursor = self.conn.cursor()
        courses = []
        for username in self.nearest_usernames:
            users_course_ids = cursor.execute("select course_id from enrollments E, course_editions CE where  username = ? and E.edition_id = CE.edition_id except select course_id from enrollments E, course_editions CE where  username = ? and E.edition_id = CE.edition_id", (username, self.user.get_username())).fetchall()
            courses = courses + users_course_ids
        courses = list(set(courses))
        courses.sort()
        # rows: course_id, avg_grade, avg interest growth for all, avg interest grow for the student, avg_skill_growth, avg_course_eval
        table = np.zeros((len(courses), 7))
        for i, course in enumerate(courses):
            table[i, 0] = course[0]
            # avg grades
            table[i, 1] = cursor.execute("select avg(LG.max_grade) from enrollments E, course_editions CE, letter_grades LG where CE.course_id = ? and  E.edition_id = CE.edition_id and E.letter_grade = LG.letter_grade", course).fetchall()[0][0]
            # avg interest growth for all
            table[i, 2] = cursor.execute("select avg(TI.interest_after-TI.interest_before) from topic_interests TI where TI.course_id = ?", course).fetchall()[0][0]
            # avg interest growth for student
            growth = cursor.execute("select avg(TI.interest_after) from topic_interests TI where TI.course_id = ? and TI.topic_id in (select TI.topic_id from topic_interests TI where username = ?)", (course[0], self.user.get_username())).fetchall()[0][0]
            table[i, 3] = growth if growth else 0
            # avg skill growth for all
            table[i, 4] = cursor.execute("select avg(SR.rank_after-SR.rank_before) from skill_rankings SR where SR.course_id = ?", course).fetchall()[0][0]
            # avg skill growth for student
            growth = cursor.execute("select avg(SR.rank_after) from skill_rankings SR where SR.course_id = ? and SR.skill_id in (select SR.skill_id from skill_rankings SR where username = ?)", (course[0], self.user.get_username())).fetchall()[0][0]
            table[i, 5] = growth if growth else 0
            # avg course eval
            table[i, 6] = cursor.execute("select avg(E.course_ranking) from enrollments E, course_editions CE where CE.course_id = ? and  E.edition_id = CE.edition_id", course).fetchall()[0][0]
        self.nearest_courses = table


    def recommend_courses(self):
        cursor = self.conn.cursor()
        while True:
            #get preference
            pref = input("What would you like in the recommended courses?\n(best grade/interest growth/skill improvement/enjoyment/cancel): ")
            while pref.lower() not in ['best grade','interest growth','skill improvement','enjoyment', 'cancel']: pref = input("Please enter 'best grade', 'interest growth', 'skill improvement', 'enjoyment' or 'cancel': ")

            if pref.lower() == 'best grade':
                recommended = self.nearest_courses[self.nearest_courses[:,1].argsort()][:5]
            elif pref.lower() == 'interest growth':
                pref = input("Do you want to see your interest growth or average improvement?\n(my/average): ")
                while pref not in ['my', 'average']: pref = input("Please enter 'my' or 'average': ")
                if pref == 'my':
                    recommended = self.nearest_courses[self.nearest_courses[:,2].argsort()][:5]
                else:
                    recommended = self.nearest_courses[self.nearest_courses[:,3].argsort()][:5]
            elif pref.lower() == 'skill improvement':
                pref = input("Do you want to see your skill improvement or average improvement?\n(my/average): ")
                while pref not in ['my', 'average']: pref = input("Please enter 'my' or 'average': ")
                if pref == 'my':
                    recommended = self.nearest_courses[self.nearest_courses[:,4].argsort()][:5]
                else:
                    recommended = self.nearest_courses[self.nearest_courses[:,5].argsort()][:5]
            elif pref.lower() == 'enjoyment':
                recommended = self.nearest_courses[self.nearest_courses[:,6].argsort()][:5]
            else: return

            for i, course in enumerate(recommended):
                cid, dept, cnum, name = cursor.execute("select * from courses where course_id = ?", (course[0],)).fetchall()[0]
                name = "Course Name: %s"%name if name else ''
                print("%-3s%s%-5d %s" % (str(i+1)+":", dept, cnum, name))

            cont = input("Would you like us to recommend you courses another way?(y/n): ")
            while cont not in ['y', 'n']: cont = input("Please enter 'y' or 'n': ")
            if cont == 'n': return

"""
    #TODO: add all commands
    def handle_special_command(self, cmd):
        if cmd == "help":
            return self.help()
        elif cmd == "logout":
            return self.leave(LOGOUT)
        elif cmd == "exit" or cmd == "quit":
            return self.leave(EXIT)
        else:
            print("Command not recognized, type '.help' to see the list of commands")

    def handle_command(self, cmd):
        if cmd[0] == '.':
            self.handle_special_command(cmd[1:])
        elif cmd == "list courses":
            self.list_courses()
        elif cmd == "list courses full":
            self.list_courses(long = True)
"""
