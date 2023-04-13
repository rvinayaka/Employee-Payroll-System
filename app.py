from flask import request, Flask, jsonify
from conn import connection
from settings import logger, handle_exceptions
import psycopg2

app = Flask(__name__)

# Employee payroll system - Design a class to manage employee payroll,
# including calculating salaries, taxes, and benefits.

# Table
#  sno | emp_name  | salary | taxes  |    role    |          benefits          | benefits_amt | overtime_hrs | attendance_record
# -----+-----------+--------+--------+------------+----------------------------+--------------+--------------+-------------------
#    6 | Hinata    |  20000 | 3600.0 | Frontend   | Coupon voucher             |          500 |          100 |               100
#    5 | NARUTO    |  14000 | 2520.0 | Backend    | Gift cards                 |          500 |           98 |                98
#    4 | FERNANDES |  12000 | 2160.0 | Junior     | Insurance                  |          500 |           78 |                78
#    2 | XYZ       |   8000 | 1440.0 | Marketing  | PF, Insurance              |         1000 |           85 |                85
#    1 | ABCD      |   4000 |  720.0 | Senior Emp | PF, Insurance, Paid leaves |         1500 |           80 |                80




@app.route("/employee", methods=["GET", "POST"])             # CREATE an item
@handle_exceptions
def add_employee():
    # Starting the database connection
    cur, conn = connection()
    logger(__name__).warning("Starting the db connection to add new employees in table")

    # Taking values from the user
    emp_name = request.json["empName"]
    salary = request.json["salary"]
    taxes = salary * 0.18

    print(emp_name, salary, taxes)

    # format = {
    #     "empName": "Hinata",
    #     "salary": 20000
    # }

    # Insert query
    add_query = """INSERT INTO payroll(emp_name, salary, 
                        taxes) VALUES (%s, %s, %s)"""

    values = (emp_name, salary, taxes)

    # Executing the query
    cur.execute(add_query, values)

    # Committing the changes to the table
    conn.commit()
    logger(__name__).info(f"{emp_name} added in the list")
    return jsonify({"message": f"{emp_name} added in the list"}), 200


@app.route("/", methods=["GET"], endpoint='show_emp_list')            # READ the cart lists
@handle_exceptions
def show_emp_list():
    # Starting the database connection
    cur, conn = connection()
    logger(__name__).warning("Starting the db connection to display members in the list")

    # Taking values from the user
    show_query = "SELECT * FROM payroll;"
    cur.execute(show_query)
    data = cur.fetchall()
    print("LIST", data)

    # Log the details into logger file
    logger(__name__).info("Displayed list of all employees in the list")
    return jsonify({"message": data}), 200


@app.route("/employee/<int:sno>", methods=["PUT"], endpoint='update_emp_details')
@handle_exceptions
def update_emp_details(sno):
    # Starting the database connection
    cur, conn = connection()
    logger(__name__).warning("Starting the db connection to update the details ")

    cur.execute("SELECT emp_name from payroll where sno = %s", (sno,))
    get_character = cur.fetchone()

    if not get_character:
        return jsonify({"message": "Character not found"}), 200

    # Taking values from the user
    data = request.get_json()
    emp_name = data.get('emp_name')
    salary = data.get('salary')
    taxes = data.get('interact')
    benefits = data.get('benefits')
    benefits_amt = data.get('benefits_amt')
    overtime_hrs = data.get('overtime')
    attendance = data.get('attendance')

    if emp_name:
        cur.execute("UPDATE payroll SET emp_name = %s WHERE sno = %s", (emp_name, sno))
    elif salary:
        cur.execute("UPDATE payroll SET salary = %s WHERE sno = %s", (salary, sno))
    elif taxes:
        cur.execute("UPDATE payroll SET taxes = %s WHERE sno = %s", (taxes, sno))
    elif benefits:
        cur.execute("UPDATE payroll SET benefits = %s WHERE sno = %s", (benefits, sno))
    elif benefits_amt:
        cur.execute("UPDATE payroll SET benefits_amt = %s WHERE sno = %s", (benefits_amt, sno))
    elif overtime_hrs:
        cur.execute("UPDATE payroll SET overtime_hrs = %s WHERE sno = %s", (overtime_hrs, sno))
    elif attendance:
        cur.execute("UPDATE payroll SET attendance_record = %s WHERE sno = %s", (attendance, sno))

    # Committing the changes to the table
    conn.commit()
    # Log the details into logger file
    logger(__name__).info(f"Member details updated: {data}")
    return jsonify({"message": "Member details updated", "Details": data}), 200



@app.route("/role/<int:sno>", methods=["PUT"], endpoint='define_role')
@handle_exceptions
def define_role(sno):
    # Starting the database connection
    cur, conn = connection()
    logger(__name__).warning("Starting the db connection to update the details ")

    cur.execute("SELECT emp_name from payroll where sno = %s", (sno,))
    get_emp = cur.fetchone()

    if not get_emp:
        return jsonify({"message": "Employee not found"}), 200

    # Taking values from the user
    data = request.get_json()
    role = data.get('role')

    # Executing the query
    cur.execute("UPDATE payroll SET role = %s WHERE sno = %s", (role, sno))

    # Committing the changes to the table
    conn.commit()
    # Log the details into logger file
    logger(__name__).info(f"Member details updated: {data}")
    return jsonify({"message": "Member role added", "Details": data}), 200



@app.route("/report/<int:sno>", methods=["GET"], endpoint='generate_report')
@handle_exceptions
def generate_report(sno):
    # Starting the database connection
    cur, conn = connection()
    logger(__name__).warning("Starting the db connection to update the details ")

    # Executing the query
    cur.execute("SELECT * from payroll where sno = %s", (sno,))
    report = cur.fetchone()

    if not report:
        return jsonify({"message": "Employee not found"}), 200

    # Log the details into logger file
    logger(__name__).info(f"Member details updated: {report}")
    return jsonify({"message": "Member report generate", "Details": report}), 200



@app.route("/delete/<int:sno>", methods=["GET", "DELETE"], endpoint='delete_emp')
@handle_exceptions
def delete_emp(sno):
    # start the database connection
    cur, conn = connection()
    logger(__name__).warning("Starting the db connection to delete employee from the list")

    query = "DELETE FROM payroll WHERE sno = %s"
    cur.execute(query, (sno,))

    # Committing the changes to the table
    conn.commit()
    # Log the details into logger file
    logger(__name__).info(f"Account no {sno} deleted from the table")
    return jsonify({"message": "Deleted Successfully", "item_no": sno}), 200



@app.route("/benefits/<int:sno>", methods=["PUT"], endpoint='show_benefits_list')
@handle_exceptions
def enter_benefits_list(sno):
    # start the database connection
    cur, conn = connection()
    logger(__name__).warning("Starting the db connection to enter benefits")

    get_query = "SELECT * from payroll WHERE sno =  %s"
    cur.execute(get_query, (sno, ))

    get_emp = cur.fetchone()

    if not get_emp:
        return jsonify({"message": "Employee not found"}), 200

    # get all the benefits from the user
    data = request.get_json()
    benefits = data.get("benefits")

    query = "UPDATE payroll SET benefits = %s WHERE sno = %s"
    values = (benefits, sno)

    # execute the query with the values
    cur.execute(query, values)

    # commit the change to the table
    conn.commit()

    # Log the details into logger file
    logger(__name__).info(f"{benefits} added to the employee with id: {sno}")
    return jsonify({"message": f"{benefits} added to the employee with id: {sno}",
                    "item_no": sno}), 200


# Calculate the benefits amount
@app.route("/benefits_amt/<int:sno>", methods=["PUT"], endpoint="calc_benefits_amount")
@handle_exceptions
def calc_benefits_amount(sno):
    # start the database connection
    cur, conn = connection()
    logger(__name__).warning("Starting the db connection to enter benefit's amount")

    get_query = "SELECT benefits from payroll WHERE sno =  %s"
    cur.execute(get_query, (sno, ))

    get_benefits_tuple = cur.fetchone()

    if not get_benefits_tuple:
        return jsonify({"message": "Employee not found"}), 200

    get_benefits_list = get_benefits_tuple[0].split(",")

    salary = len(get_benefits_list)
    print("tuple", get_benefits_tuple)
    print("list", get_benefits_list)
    print(salary)



    # get all the benefits from the user
    benefits_amt = salary * 500
    print("amt", benefits_amt)

    query = "UPDATE payroll SET benefits_amt = %s WHERE sno = %s"
    values = (benefits_amt, sno)

    # execute the query with the values
    cur.execute(query, values)

    # commit the change to the table
    conn.commit()

    # Log the details into logger file
    logger(__name__).info(f"Employee with id: {sno} has got total benefits of {benefits_amt}")
    return jsonify({"message": f"Employee with id: {sno} has got total benefits of {benefits_amt}",
                    "employee number": sno}), 200


@app.route("/overtime/<int:sno>", methods=["PUT"], endpoint='enter_overtime_hours')
@handle_exceptions
def enter_overtime_hours(sno):
    # start the database connection
    cur, conn = connection()
    logger(__name__).warning("Starting the db connection to enter overtime hours")

    get_query = "SELECT salary from payroll WHERE sno =  %s"
    cur.execute(get_query, (sno, ))

    get_emp = cur.fetchone()

    if not get_emp:
        return jsonify({"message": "Employee not found"}), 200


    # Taking values from the user
    data = request.get_json()
    overtime_hrs = data.get("overtime")

    query = "UPDATE payroll SET overtime_hrs = %s WHERE sno = %s"
    values = (overtime_hrs, sno)

    # execute the query with the values
    cur.execute(query, values)

    # commit the change to the table
    conn.commit()

    # Log the details into logger file
    logger(__name__).info(f"Overtime of {overtime_hrs} hours added to the employee with id: {sno}")
    return jsonify({"message": f"Overtime of {overtime_hrs} hours added to the employee with id: {sno}",
                    "item_no": sno}), 200


@app.route("/attendance/<int:sno>", methods=["PUT"], endpoint='enter_attendance')
@handle_exceptions
def enter_attendance(sno):
    # start the database connection
    cur, conn = connection()
    logger(__name__).warning("Starting the db connection to enter overtime hours")

    get_query = "SELECT salary from payroll WHERE sno =  %s"
    cur.execute(get_query, (sno, ))

    get_emp = cur.fetchone()

    if not get_emp:
        return jsonify({"message": "Employee not found"}), 200

    # Taking values from the user
    data = request.get_json()
    attendance = data.get("attendance")
    print(attendance)

    query = "UPDATE payroll SET attendance_record = %s WHERE sno = %s"
    values = (attendance, sno)

    # execute the query with the values
    cur.execute(query, values)

    # commit the change to the table
    conn.commit()

    # Log the details into logger file
    logger(__name__).info(f"Employee with id: {sno} has overall attendance of {attendance}")
    return jsonify({"message": f"Employee with id: {sno} has overall attendance of {attendance}",
                    "item_no": sno}), 200



if __name__ == "__main__":
    app.run(debug=True, port=5000)
