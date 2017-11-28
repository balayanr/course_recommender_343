from __future__ import print_function
from builtins import input
from db_core import *
from handler import *
from magic_numbers import *

def verify_yn(ans):
    while True:
        if ans == "y" or ans == "n":
            return ans
        else: ans = input("Unrecognised input, please enter 'y' or 'n': ")



# Establish connection
conn = db_init();
cursor = conn.cursor()
newuser = True

while True:
    if newuser:
        # Initial welcome screen
        print("Welcome to my Course Recommender App! \n\
            Fun times await, but only if you enter your credentials!")
        username = input("Username: ")
        user = login(conn, username)
        handler = Handler(user, conn)

        ## Update profile
        user.update_profile()

   ## Collecting user courses
    if not len(user.get_courses()):
        print("\nThere are 0 courses on your profile!")
        print("Please add some courses to get good recommendations!")
    else:
        print("\nThere are %d courses recorded on your profile." %
                len(user.get_courses()))
        quest ="Do you want to see them?(y/n): "
        if verify_yn(input(quest)) == "y":
            quest = "Do you want to see full course descriptions?(y/n): "
            long = True if verify_yn(input(quest)) == "y" else False
            handler.list_courses(long = long)


    ## Add courses - "complete" profile
    quest = "\nDo you want to add more courses to complete the profile?(y/n): "
    if verify_yn(input(quest)) == "y":
        handler.add_courses()

    ## Set up skills
    user.setup_skills_and_interests()

    if len(user.get_courses()): #skip if there are no courses
    ## Collecting user interests
        if user.get_empty_topics():
            print("\nYou have filled out %d topic reviews out of %d available."
                        % (len(user.get_topics()),
                        len(user.get_topics()) + len(user.get_empty_topics())))
            quest ="Do you want to fill out any topic reviews available?(y/n): "
            if verify_yn(input(quest)) == 'y':
                handler.rate_topics()
        else:
            print("You have reviewed all available topics, thank you! \n")
            quest = "Do you want to see them?(y/n): "
            if verify_yn(input(quest)) == "y":
                user.print_topics()


    ## Collecting user skills
        if user.get_empty_skills():
            print("\nYou have filled out %d skill reviews out of %d available."
                    % (len(user.get_skills()),
                    len(user.get_skills()) + len(user.get_empty_skills())))
            quest = "Do you want to fill out any skill reviews available?(y/n): "
            if verify_yn(input(quest)) == 'y':
                handler.rate_skills()
        else:
            print("\nYou have reviewed all available skills, thank you!")
            quest = "Do you want to see them?(y/n): "
            if verify_yn(input(quest)) == "y":
                user.print_skills()


    ## Compute potential recommendations
    try:
        handler.create_table() # sets up the table with recommendations
        handler.get_nearest_courses() # get the list of nearest courses
    except:
        print("Sorry, there is too little information about you in the system.")
        print("Please add at lease one course to your profile and \
                                                review a topic and a skill!")

        quest = "Do you want to continue?(y/n): "
        if verify_yn(input(quest)) == 'y':
            newuser = False
            continue
        else: break


    ## Presenting recommendations based on the user-specified criteria
    handler.recommend_courses()

    ## Ask to quit or logout
    logout = input("\nWould you like to log out, exit or continue using the \
                                    recommender?\n(logout/exit/continue): ")
    while logout not in ['logout', 'exit', 'continue']:
        logout = input("Please enter 'logout', 'exit' or 'continue': ")
    if logout == 'exit': break
    elif logout == 'logout': continue
    else:
        print("Sorry, this feature is still under construction.")
        print("Uncomment the code at your own risk!")
        continue
        ## Loop over functions in case user wants to play around
        # updated = False
        # while True:
       ##       action = input("What would you like to do?:\n(update profile/add courses/rate topics/rate skills/get recommendations/exit): ")
        #     while action not in ['update profile','add courses','rate topics','rate skills','get recommendations','exit']:
                # action = input()

       ##       if action == 'update profile': user.update_profile()
        #     elif action == 'add courses':
        #         handler.add_courses()
        #         user.setup_skills_and_interests()
        #         updated = True
        #     elif action == 'rate topics':
        #         handler.rate_topics()
        #         updated = True
        #     elif action == 'rate skills':
        #         rate_skills()
        #         updated = True
        #     elif action == 'get recommendations':
        #         if updated:
        #             handler.create_table() # sets up the table with recommendations
        #             handler.get_nearest_courses() # get the list of nearest courses
        #             updated = False
        #         handler.recommend_courses()
        #     elif action == 'exit': exit()
