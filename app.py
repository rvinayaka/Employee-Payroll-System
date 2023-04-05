from flask import request, Flask, jsonify
from conn import connection
from settings import logger
import psycopg2

app = Flask(__name__)

# Employee payroll system - Design a class to manage employee payroll,
# including calculating salaries, taxes, and benefits.

# Table
#  sno | emp_name  | salary | taxes  | benefits |    role
# -----+-----------+--------+--------+----------+------------
#    1 | ABCD      |   4000 |  720.0 |   2000.0 | Senior Emp
#    2 | XYZ       |   8000 | 1440.0 |   4000.0 | Marketing
#    4 | FERNANDES |  12000 | 2160.0 |   6000.0 | Junior
#    5 | NARUTO    |  14000 | 2520.0 |   7000.0 | Backend
#    6 | Hinata    |  20000 | 3600.0 |  10000.0 | Frontend


def handle_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except psycopg2.Error as error:
            conn = kwargs.get('conn')
            if conn:
                conn.rollback()
            logger(__name__).error(f"Error occurred: {error}")
            return jsonify({"message": f"Error occurred: {error}"})
        except Exception as error:
            logger(__name__).error(f"Error occurred: {error}")
            return jsonify({"message": f"Error occurred: {error}"})
        finally:
            conn = kwargs.get("conn")
            cur = kwargs.get("cur")
            # close the database connection
            if conn:
                conn.close()
            if cur:
                cur.close()
            logger(__name__).warning("Closing the connection")
    return wrapper



@app.route("/employee", methods=["GET", "POST"])             # CREATE an item
@handle_exceptions
def add_employee():
    cur, conn = connection()
    logger(__name__).warning("Starting the db connection to add new employees in table")

    emp_name = request.json["empName"]
    salary = request.json["salary"]
    taxes = salary * 0.18
    benefits = salary * 0.5
    print(emp_name, salary, taxes, benefits)

    # format = {
    #     "empName": "Hinata",
    #     "salary": 20000
    # }

    add_query = """INSERT INTO payroll(emp_name, salary, 
                        taxes, benefits) VALUES (%s, %s, %s, %s)"""
    # entry = "{
    #     "empName": "ABCD",
    #     "salary": 4000
    #   }"
    values = (emp_name, salary, taxes, benefits)
    cur.execute(add_query, values)

    conn.commit()
    logger(__name__).info(f"{emp_name} added in the list")
    return jsonify({"message": f"{emp_name} added in the list"}), 200


@app.route("/", methods=["GET"], endpoint='show_emp_list')            # READ the cart lists
@handle_exceptions
def show_emp_list():
    cur, conn = connection()
    logger(__name__).warning("Starting the db connection to display members in the list")

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
    cur, conn = connection()
    logger(__name__).warning("Starting the db connection to update the details ")

    cur.execute("SELECT emp_name from payroll where sno = %s", (sno,))
    get_character = cur.fetchone()

    if not get_character:
        return jsonify({"message": "Character not found"}), 200
    data = request.get_json()
    emp_name = data.get('emp_name')
    salary = data.get('salary')
    taxes = data.get('interact')
    benefits = data.get('benefits')

    if emp_name:
        cur.execute("UPDATE payroll SET emp_name = %s WHERE sno = %s", (emp_name, sno))
    elif salary:
        cur.execute("UPDATE payroll SET salary = %s WHERE sno = %s", (salary, sno))
    elif taxes:
        cur.execute("UPDATE payroll SET taxes = %s WHERE sno = %s", (taxes, sno))
    elif benefits:
        cur.execute("UPDATE payroll SET benefits = %s WHERE sno = %s", (benefits, sno))

    conn.commit()
    # Log the details into logger file
    logger(__name__).info(f"Member details updated: {data}")
    return jsonify({"message": "Member details updated", "Details": data}), 200



@app.route("/role/<int:sno>", methods=["PUT"], endpoint='define_role')
@handle_exceptions
def define_role(sno):
    cur, conn = connection()
    logger(__name__).warning("Starting the db connection to update the details ")

    cur.execute("SELECT emp_name from payroll where sno = %s", (sno,))
    get_emp = cur.fetchone()

    if not get_emp:
        return jsonify({"message": "Employee not found"}), 200

    data = request.get_json()
    role = data.get('role')

    cur.execute("UPDATE payroll SET role = %s WHERE sno = %s", (role, sno))

    conn.commit()
    # Log the details into logger file
    logger(__name__).info(f"Member details updated: {data}")
    return jsonify({"message": "Member role added", "Details": data}), 200



@app.route("/report/<int:sno>", methods=["GET"], endpoint='generate_report')
@handle_exceptions
def generate_report(sno):
    cur, conn = connection()
    logger(__name__).warning("Starting the db connection to update the details ")

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

    conn.commit()
    # Log the details into logger file
    logger(__name__).info(f"Account no {sno} deleted from the table")
    return jsonify({"message": "Deleted Successfully", "item_no": sno}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
