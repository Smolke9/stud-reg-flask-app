from flask import Flask, render_template, request
import mysql.connector
import logging

app = Flask(__name__)

logging.basicConfig(
    filename='flask.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Surajmolke123',
    'database': 'studentdb'
}

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            course = request.form['course']
            address = request.form['address']
            contact = request.form['contact']

            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            query = """
                INSERT INTO students (name, email, phone, course, address, contact)
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            cursor.execute(query, (name, email, phone, course, address, contact))
            conn.commit()

            cursor.close()
            conn.close()

            return "Student Registered Successfully!"

        except Exception as e:
            logging.error(f"ERROR: {e}")
            return f"Internal Server Error: {e}", 500

    return render_template('register.html')


@app.route('/students')
def students():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template("students.html", students=data)

    except Exception as e:
        logging.error(f"ERROR: {e}")
        return f"Internal Server Error: {e}", 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
