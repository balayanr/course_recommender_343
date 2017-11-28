## CSC343 Assignment 3: Developing data products using data analytics and embedded SQL

The assignment was to design an application that would present a user with an
interface (CLI in this case), where the user can either "login" (without a password)
or set up a new user. Then the user can complete their profile by adding courses
and skills.

Once everything is set up, the user can select in which way to have the courses
recommended to them. The app queries the database for users with matching completed
courses and makes a recommendation. See "Assignment 3.pdf" for the assignment details on functionality and the database schema.

There was some experimental functionality planned with some functions implemented,
but in the end I decided to focus on fleshing out the core functinoality and abandonned
the extras. Some code is still present, but commented out.

Run main.py to use the app or use testing.py to have the app run with a pre-set user straight to recommendation.
