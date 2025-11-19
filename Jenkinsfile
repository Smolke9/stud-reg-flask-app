pipeline {
    agent any

    environment {
        FLASK_LOG = 'flask.log'
        SOCAT_LOG = 'socat.log'
        // Optional: If your Flask app uses environment variables for DB connection, define them here
        // MYSQL_HOST = 'localhost'
        // MYSQL_USER = 'flask_user'
        // MYSQL_PASSWORD = 'your_secure_password'
        // MYSQL_DB = 'student_registration'
    }

    stages {
        stage('Clone GitHub Repo') {
            steps {
                echo "Cloning repository: https://github.com/Smolke9/stud-reg-flask-app.git"
                git branch: 'master', url: 'https://github.com/Smolke9/stud-reg-flask-app.git'
            }
        }

        stage('Create Virtual Environment') {
            steps {
                echo "Creating Python virtual environment..."
                sh 'python3 -m venv venv'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo "Upgrading pip..."
                sh './venv/bin/pip install --upgrade pip'
                echo "Installing Flask and MySQL connector from requirements.txt..."
                sh './venv/bin/pip install -r requirements.txt'
            }
        }

        stage('Run Flask App') {
            steps {
                echo "Attempting to kill any old Flask app processes to ensure clean start..."
                sh 'pkill -f app.py || true' // Kill old Flask app if running

                echo "Starting Flask app in background on port 5000..."
                // Start Flask app in the background and capture its PID
                // Ensure your app.py is configured to run on host='0.0.0.0' and port=5000
                sh 'nohup ./venv/bin/python3 app.py > $FLASK_LOG 2>&1 & echo $! > flask_app_pid.txt'
                sh 'sleep 15' // Give it ample time to start and bind, especially if DB connection is slow

                echo "Verifying Flask app process is running..."
                // Check if Flask is running using its PID
                sh 'FLASK_PID=$(cat flask_app_pid.txt); if ps -p $FLASK_PID > /dev/null; then echo "Flask app with PID $FLASK_PID is running."; else echo "Flask app failed to start or crashed! Check $FLASK_LOG for details."; exit 1; fi'

                echo "--- Flask app logs from startup (check for DB connection errors) ---"
                sh 'cat $FLASK_LOG' // Display Flask app logs for debugging
                sh 'echo "-------------------------------------------------------------------"'

                echo "Verifying Flask app is listening on port 5000 using 'ss'..."
                // Use 'ss' to check if Flask is listening on port 5000
                // 'ss -tulnp' might require sudo depending on permissions and environment.
                // If it fails with "sudo: a terminal is required", you need to add 'jenkins ALL=(ALL) NOPASSWD: /usr/bin/ss' to sudoers.
                sh 'sudo ss -tulnp | grep 5000 || (echo "Flask app not listening on port 5000! Check $FLASK_LOG for errors." && exit 1)'
                sh 'echo "Flask app confirmed listening on port 5000."'
            }
        }

        stage('Expose Port to Windows (via socat)') {
            steps {
                echo "Attempting to kill any old socat processes..."
                sh 'pkill socat || true' // Kill old socat if any

                echo "Starting socat for port forwarding (5050 -> 5000)..."
                // Use port 5050 on WSL2, forward to Flask app on localhost:5000
                sh 'nohup socat TCP-LISTEN:5050,fork TCP:localhost:5000 > $SOCAT_LOG 2>&1 & echo $! > socat_pid.txt'
                sh 'sleep 240' // Give it enough time to start

                echo "Verifying socat process is running..."
                // Check if socat is running using its PID
                sh 'SOCAT_PID=$(cat socat_pid.txt); if ps -p $SOCAT_PID > /dev/null; then echo "Socat with PID $SOCAT_PID is running."; else echo "Socat failed to start or crashed! Check $SOCAT_LOG for details."; exit 1; fi'

                echo "--- Socat logs from startup ---"
                sh 'cat $SOCAT_LOG' // Display socat logs
                sh 'echo "-------------------------------"'

                echo "Verifying socat is listening on port 5050 using 'ss'..."
                // Use 'ss' to check if socat is listening on port 5050
                sh 'sudo ss -tulnp | grep 5050 || (echo "Socat not listening on port 5050! Check $SOCAT_LOG for errors." && exit 1)'
                sh 'echo "Socat confirmed listening on port 5050."'
            }
        }

        stage('Verify Application Access (from within Jenkins Agent)') {
            steps {
                echo "Attempting to curl Flask app via socat from within the Jenkins agent..."
                // This verifies the full chain from socat to Flask from the agent's perspective
                sh 'curl -v http://13.232.184.169:5050 || (echo "Curl to Flask app via socat failed! Check logs and process status." && exit 1)'
                echo "Application accessible via socat from within Jenkins agent. This confirms internal connectivity."
            }
        }
    }
}
