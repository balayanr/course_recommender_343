from __future__ import print_function

class Topic:
    def __init__(self, tuple):
        self.course_id, self.edition_id, _, self.topic_id,\
        self.interest_before, self.interest_after, _, self.topic, _, \
        self.dept_code, self.course_number, _= tuple

        self.items = [self.course_id, self.edition_id, self.topic_id,\
        self.interest_before, self.interest_after, self.topic, self.dept_code,\
        self.course_number]

    def __getitem__(self, i):
        return self.items[i]

    ## Getters
    def get_cid(self):
        return self.course_id
    def get_eid(self):
        return self.edition_id
    def get_tid(self):
        return self.topic_id
    def get_int_before(self):
        return self.interest_before
    def get_int_after(self):
        return self.interest_after
    def get_name(self):
        return self.topic
    def get_dept(self):
        return self.dept_code
    def get_cnum(self):
        return self.course_number
    def get_course(self):
        return self.dept_code + str(self.course_number)

    ## Setters
    def set_cid(self, param):
        self.course_id = param
    def set_eid(self, param):
        self.edition_id = param
    def set_topic_id(self, param):
        self.topic_id = param
    def set_topic(self, param):
        self.topic = param
    def set_dept(self, input):
        self.dept_code = input.upper()
    def set_cnum(self, input):
        self.course_number = int(input)
    def set_int_before(self, param):
        self.interest_before = param
    def set_int_after(self, param):
        self.interest_after = param

    ## Misc
    def print_data(self, rows = False):
        print("Name: %s " % self.get_name())
        if rows:
            print("    ", end = '')
        print("Course: %-8s" % self.get_course(), end = '')
        if self.get_int_before() and self.get_int_after():
            print("Interest before: %-5d Interest after: %-5d" % (self.get_int_before(), self.get_int_after()))
        else: print('')
