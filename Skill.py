from __future__ import print_function

class Skill:
    def __init__(self, tuple):
        self.course_id, self.edition_id, _, self.skill_id,\
        self.rank_before, self.rank_after, _, self.skill, _, self.dept_code,\
        self.course_number, _ = tuple

        self.items = [self.course_id, self.edition_id, self.skill_id,\
        self.rank_before, self.rank_after, self.skill, self.dept_code,\
        self.course_number]

    def __getitem__(self, i):
        return self.items[i]

    ## Getters
    def get_cid(self):
        return self.course_id
    def get_eid(self):
        return self.edition_id
    def get_sid(self):
        return self.skill_id
    def get_rank_before(self):
        return self.rank_before
    def get_rank_after(self):
        return self.rank_after
    def get_name(self):
        return self.skill
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
    def set_skill_id(self, param):
        self.skill_id = param
    def set_rank_before(self, param):
        self.rank_before = param
    def set_rank_after(self, param):
        self.rank_after = param
    def set_skill(self, param):
        self.skill = param
    def set_dept(self, param):
        self.dept_code = param
    def set_cnum(self, param):
        self.course_number = param

    ## Misc
    def print_data(self, rows = False):
        print("Name: %s " % self.get_name())
        if rows:
            print("    ", end = '')
        print("Course: %-8s" % self.get_course(), end = '')
        if self.get_rank_before() and self.get_rank_after():
            print("Rank before: %-5d Rank after: %-5d" % \
                        (self.get_rank_before(), self.get_rank_after()))
        else: print('')
