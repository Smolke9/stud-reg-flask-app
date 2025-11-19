from flask import Flask, render_template, request
import mysql.connector
import logging

app = Flask(__name__)

# Configure logging to file
logging.basicConfig(filename='flask.log', level=logging.INFO)

# Database config for local MySQL
db_config = {
    'host': 'localhost',
    'user': 'flaskuser',
    'password': 'Flaskpass123',  # 🔐 Replace if changed
    'database': 'studentdb'
}

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        course = request.form['course']
        address = request.form['address']
        contact = request.form['contact']

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = '''
        INSERT INTO students (name, email, phone, course, address, contact)
        VALUES (%s, %s, %s, %s, %s, %s)
        '''
        values = (name, email, phone, course, address, contact)

        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()

        logging.info(f"Student Registered: {name}")
        return 'Student Registered Successfully!'
    return render_template('register.html')

@app.route('/students')
def students():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("students.html", students=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
