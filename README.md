# 🚀 Flask Student Registration App — Stepwise README

> A step-by-step guide to set up, run and deploy the Flask-based Student Registration application (from the provided Project 3 PDF).
> Source PDF: /mnt/data/Project 3.pdf

---

## Prerequisites
1. Ubuntu (or similar Linux) or Windows with WSL / macOS  
2. Python 3.8+ installed (`python3 --version`)  
3. MySQL server installed and running  
4. Git installed (`git --version`)  
5. Jenkins server (for CI/CD) — optional for local testing  
6. `socat` installed on the Jenkins agent (for port forwarding)

---

## 1. Clone the repository
```bash
git clone https://github.com/Smolke9/stud-reg-flask-app.git
cd stud-reg-flask-app
```

> If you forked from `https://github.com/swati-zampal/stud-reg-flask-app.git`, use your fork URL instead.

---

## 2. Create Python virtual environment & install dependencies
```bash
python3 -m venv venv
source venv/bin/activate      # macOS / Linux
# or on Windows PowerShell:
# venv\Scripts\Activate.ps1

pip install --upgrade pip
pip install -r requirements.txt
# If requirements.txt not present, install:
pip install Flask==2.3.2 mysql-connector-python
```

---

## 3. Create MySQL database & table
Login to MySQL and run SQL commands:
```sql
CREATE DATABASE studentdb;

USE studentdb;

CREATE TABLE students (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(100),
  phone VARCHAR(20),
  course VARCHAR(50),
  address VARCHAR(255),
  contact VARCHAR(20),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

Update DB credentials in `app.py` (see next section).

---

## 4. Configure the Flask app (app.py)
Open `app.py` and update `db_config` with your MySQL credentials:
```python
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_mysql_password',
    'database': 'studentdb'
}
```

Main parts of `app.py` (for reference):
```python
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__, template_folder='templates')

db_config = { ... }   # update as above

@app.route('/')
def register():
    return render_template('register.html')

@app.route('/students', methods=['POST'])
def students():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    course = request.form['course']
    address = request.form['address']
    contact = request.form['contact']

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO students (name,email,phone,course,address,contact) VALUES (%s,%s,%s,%s,%s,%s)",
        (name,email,phone,course,address,contact)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('register'))  # or a success page
```

---

## 5. HTML templates
Create `templates/register.html` (example):
```html
<!doctype html>
<html>
  <head><title>Register Student</title></head>
  <body>
    <h1>Student Registration</h1>
    <form action="/students" method="POST">
      <input type="text" name="name" placeholder="Name" required><br>
      <input type="email" name="email" placeholder="Email" required><br>
      <input type="text" name="phone" placeholder="Phone" required><br>
      <input type="text" name="course" placeholder="Course" required><br>
      <input type="text" name="address" placeholder="Address" required><br>
      <input type="text" name="contact" placeholder="Contact No" required><br>
      <button type="submit">Register</button>
    </form>
  </body>
</html>
```

Optional `templates/students.html` to list students:
```html
<!-- iterate and show rows fetched from DB -->
```

---

## 6. Run locally (development)
```bash
export FLASK_APP=app.py
# Optional: export FLASK_ENV=development
python3 app.py
# App will run on 0.0.0.0:5000 by default if app.py uses app.run(host='0.0.0.0', port=5000)
# Open: http://localhost:5000
```

---

## 7. Jenkins CI/CD pipeline (Jenkinsfile)
Add the following `Jenkinsfile` to repo root:
```groovy
pipeline {
  agent any
  stages {
    stage('Clone Repo') {
      steps { git 'https://github.com/Smolke9/stud-reg-flask-app.git' }
    }
    stage('Create VENV') {
      steps { sh 'python3 -m venv venv' }
    }
    stage('Install Dependencies') {
      steps { sh 'venv/bin/pip install -r requirements.txt' }
    }
    stage('Run Flask App') {
      steps { sh 'nohup venv/bin/python3 app.py & sleep 2' }
    }
    stage('Expose Port') {
      steps { sh 'nohup socat TCP-LISTEN:5050,fork TCP:localhost:5000 & sleep 1' }
    }
    stage('Health Check') {
      steps { sh 'curl -v http://localhost:5050 || true' }
    }
  }
}
```

**Notes for Jenkins:**
- Install required plugins: Git, Pipeline, SSH Agent, Python (optional).
- Ensure the Jenkins agent has `python3`, `pip`, and `socat` installed.
- Use credentials store for any secrets rather than storing passwords in code.

---

## 8. Install `socat` (on Jenkins agent)
```bash
sudo apt-get update
sudo apt-get install -y socat
```
This command forwards external port 5050 to the Flask app running on 5000:
```bash
socat TCP-LISTEN:5050,fork TCP:localhost:5000
```

---

## 9. Healthcheck and troubleshooting
- Health check (from Jenkins or host):
```bash
curl -v http://localhost:5050
```
- If curl fails:
  - Check Flask logs (console or nohup.out)
  - Ensure MySQL is reachable and credentials correct
  - Ensure `socat` is running and port 5050 not blocked by firewall

---

## 10. Production considerations
- Use a production WSGI server (Gunicorn / uWSGI) instead of Flask dev server:
```bash
venv/bin/pip install gunicorn
venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app
```
- Use environment variables (or secrets manager) for DB credentials.
- Add HTTPS (reverse proxy like Nginx + TLS).
- Apply input validation and CSRF protection (Flask-WTF) before production use.

---

## 11. Useful commands
```bash
# Stop socat (find PID then kill)
ps aux | grep socat
kill <pid>

# Show MySQL connection test
mysql -u root -p -e "USE studentdb; SHOW TABLES;"
```

---

## 12. Helpful links & original PDF
- Project PDF (uploaded): `/mnt/data/Project 3.pdf`
- Original forked repo: https://github.com/swati-zampal/stud-reg-flask-app.git
- Your repo: https://github.com/Smolke9/stud-reg-flask-app.git

---

## Author
**Suraj Molke** — see full project PDF: `/mnt/data/Project 3.pdf`

---

*If you want, I can save this as a file and provide a download link.*