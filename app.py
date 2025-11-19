from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Database configuration
db_config = {
    'host': 'db',
    'user': 'flaskuser',
    'password': 'FlaskPass123"',
    'database': 'studentsdb'
}

# Home page: Registration form
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

        return 'Student Registered Successfully!'
    return render_template('register.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
