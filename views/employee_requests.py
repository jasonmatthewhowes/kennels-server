import sqlite3
import json
from models import Employee, Location

def create_employee(employee):
    # Get the id value of the last item in the list
    max_id = EMPLOYEES[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the dictionary
    employee["id"] = new_id

    # Add the  dictionary to the list
    EMPLOYEES.append(employee)

    # Return the dictionary with `id` property added
    return employee

    
def delete_employee(id):
    # Initial -1 value for employee index, in case one isn't found
    employee_index = -1

    # Iterate the list, but use enumerate() so that you
    # can access the index value of each item
    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
            # Found the employe. Store the current index.
            employee_index = index

    # If the employee was found, use pop(int) to remove it from list
    if employee_index >= 0:
        EMPLOYEES.pop(employee_index)

def update_employee(id, new_employee):
    # Iterate the list, but use enumerate() so that
    # you can access the index value of each item.
    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
            # Found the dictionary. Update the value.
            EMPLOYEES[index] = new_employee
            break


#New actual SQL database function
def get_all_employees():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.location_id,
            l.name location_name,
            l.address location_address
        FROM employee a
        JOIN Location l
            ON l.id = a.location_id
        """)

        # Initialize an empty list to hold all animal representations
        employees = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Animal class above.
            employee = Employee(row['id'], row['name'], row['location_id'])
            location = Location(row['id'], row['location_name'], row['location_address'])
            employee.location = location.__dict__

            employees.append(employee.__dict__)

    return employees

#New actual SQL database function
def get_single_employee(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.location_id
        FROM employee a
        WHERE a.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        employee = Employee(data['id'], data['name'], data['location_id'])

        return employee.__dict__



def get_employees_by_location(location_id):

    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            c.id,
            c.name,
            c.location_id
        FROM employee c
        WHERE c.location_id = ?
        """, ( location_id, ))

        employees = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            employee = Employee(row['id'], row['name'],row['location_id'])
            employees.append(employee.__dict__)

    return employees