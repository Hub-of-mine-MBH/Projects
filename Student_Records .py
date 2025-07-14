import sqlite3
import json
import xml.etree.ElementTree as ET
from tabulate import tabulate

try:
    conn = sqlite3.connect("HyperionDev.db")
except sqlite3.Error:
    print("Please store your database as HyperionDev.db")
    quit()

cur = conn.cursor()

def usage_is_incorrect(args, num_args):
    if len(args) != num_args + 1:
        print(f"The {args[0]} command requires {num_args} arguments.")
        return True
    return False


def store_data_as_json(data, filename):
    """Store the first element of each row in data as a JSON array."""
    obj_list = [row for row in data]

    with open(filename, "w") as file:
        json.dump(obj_list, file, indent=4)
    print("JSON file created!")


def store_data_as_xml(data, filename):
    """Store the first element of each row in data as XML under a user-defined root."""
    root_name = input("Please enter root element: ")
    root = ET.Element(root_name)

    for row in data:
        course = ET.SubElement(root, root_name)
        for j, value in enumerate(row):
            col = ET.SubElement(course, f"Column{j + 1}")
            col.text = str(value)

    tree = ET.ElementTree(root)
    tree.write(filename, encoding="utf-8")
    print("XML file created!")


def offer_to_store(data):
    while True:
        print("Would you like to store this result?")
        choice = input("Y/[N]? : ").strip().lower()

        if choice == "y":
            filename = input("Specify filename. Must end in .xml or .json: ")
            ext = filename.split(".")[-1].lower()
            if ext == "xml":
                store_data_as_xml(data, filename)
            elif ext == "json":
                store_data_as_json(data, filename)
            else:
                print("Invalid file extension. Please use .xml or .json.")
        elif choice == "n":
            break
        else:
            print("Invalid choice.")


usage = '''
What would you like to do?

d - demo
vs <student_id>            - view subjects taken by a student
la <firstname> <surname>   - lookup address for a given firstname and surname
lr <student_id>            - list reviews for a given student_id
lc <teacher_id>            - list all courses taken by teacher_id
lnc                        - list all students who haven't completed their course
lf                         - list all students who have completed their course and achieved 30 or below
e                          - exit this program

Type your option here: '''

print("Welcome to the data querying app!")

while True:
    print()
    # Get input from user
    user_input = input(usage).split(" ")
    print()

    # Parse user input into command and args
    command = user_input[0]
    args = user_input[1:] if len(user_input) > 1 else []

    if command == 'd':  # Demo - print all student names and surnames
        data = cur.execute("SELECT * FROM Student")
        for _, firstname, surname, _, _ in data:
            print(f"{firstname} {surname}")

    elif command == 'vs':  # View subjects by student_id
        if usage_is_incorrect(user_input, 1):
            continue

        student_id = args[0]
        data = cur.execute(
            '''
            SELECT Course.course_name
            FROM Course
            INNER JOIN StudentCourse
            ON Course.course_code = StudentCourse.course_code
            WHERE student_id = ?
            ''',
            (student_id,)
        ).fetchall()

        print(f"Courses taken by {student_id}:")
        for count, course in enumerate(data):
            print(f"{count + 1}. {course[0]}")
        print()

        offer_to_store(data)

    elif command == 'la':  # List address by name and surname
        if usage_is_incorrect(user_input, 2):
            continue

        firstname, surname = args[0], args[1]
        data = cur.execute(
            '''
            SELECT street, city
            FROM Address
            INNER JOIN Student
            ON Address.address_id = Student.address_id
            WHERE first_name = ? AND last_name = ?
            ''',
            (firstname, surname)
        ).fetchall()

        for address in data:
            print(f"{address[0]} {address[1]}")
        print("\n")

        offer_to_store(data)

    elif command == 'lr':  # List reviews by student_id
        if usage_is_incorrect(user_input, 1):
            continue

        student_id = args[0]
        data = cur.execute(
            '''
            SELECT completeness,
                   efficiency,
                   style,
                   documentation,
                   review_text
            FROM Review
            WHERE student_id = ?
            ''',
            (student_id,)
        ).fetchall()


        for review in data:
            print(f'Completeness: {review[0]}')
            print(f'Efficiency: {review[1]}')
            print(f'Style: {review[2]}')
            print(f'Documentation: {review[3]}')
            print(f'Review:\n{review[4]}')
            print()

        offer_to_store(data)

    elif command == 'lc':  # List all courses taken by teacher_id
        if usage_is_incorrect(user_input, 1):
            continue

        teacher_id = args[0]
        data = cur.execute(
            '''
            SELECT course_name
            FROM Course
            WHERE teacher_id = ?
            ''',
            (teacher_id,)
        ).fetchall()

        print("Courses:\n")
        for course in data:
            print(course[0])
        print()

        offer_to_store(data)

    elif command == 'lnc':  # List all students who haven't completed their course
        data = cur.execute(
            '''
            SELECT Student.student_id,
                   first_name,
                   last_name,
                   email,
                   course_name
            FROM StudentCourse
            INNER JOIN Student
            ON Student.student_id = StudentCourse.student_id
            INNER JOIN Course
            ON StudentCourse.course_code = Course.course_code
            WHERE is_complete = 0
            '''
        ).fetchall()

        print("Students who have not completed their course:\n")
        
        # Creating table
        headers = [desc[0] for desc in cur.description]
        print(tabulate(data, headers=headers, tablefmt="fancy_grid"))

        print()

        offer_to_store(data)

    elif command == 'lf':  # List all students who completed their course and got a mark <= 30
        data = cur.execute(
            '''
            SELECT Student.student_id,
                   first_name,
                   last_name,
                   email,
                   course_name,
                   mark
            FROM StudentCourse
            INNER JOIN Student
            ON Student.student_id = StudentCourse.student_id
            INNER JOIN Course
            ON StudentCourse.course_code = Course.course_code
            WHERE is_complete = 1 AND mark <= 30
            '''
        ).fetchall()

        # Creating a table
        headers = [desc[0] for desc in cur.description]
        print(tabulate(data, headers=headers, tablefmt="fancy_grid"))

        offer_to_store(data)

    elif command == 'e':
        print("Programme exited successfully!")
        break

    else:
        print(f"Incorrect command: '{command}'")
        