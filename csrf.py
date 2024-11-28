from flask import Flask, request, render_template_string, jsonify, session
from flask_wtf.csrf import CSRFProtect
import sqlite3
import ssl

app = Flask(__name__)
app.secret_key = 'supersecretkey123'  # Required for CSRF
csrf = CSRFProtect(app)  # Initialize CSRF protection

# Updated template with CSRF token
TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Security Analysis Console</title>
    <style>
        body {
            background-color: #000;
            color: #00ff00;
            font-family: 'Courier New', monospace;
            margin: 0;
            padding: 20px;
        }
        .console {
            background-color: rgba(0, 20, 0, 0.9);
            border: 1px solid #00ff00;
            padding: 20px;
            margin: 20px auto;
            max-width: 800px;
            box-shadow: 0 0 20px rgba(0, 255, 0, 0.2);
        }
        input {
            background-color: #001100;
            border: 1px solid #00ff00;
            color: #00ff00;
            padding: 8px;
            margin: 5px 0;
            width: 100%;
            font-family: 'Courier New', monospace;
        }
        input[type="submit"] {
            background-color: #003300;
            cursor: pointer;
        }
        .status {
            margin-top: 20px;
            padding: 10px;
            border: 1px solid #00ff00;
        }
    </style>
</head>
<body>
    <div class="console">
        <h1>_Security_Analysis_Console_</h1>
        
        <!-- Login Form without CSRF Protection -->
        <h3>> Vulnerable Login (No CSRF Protection):</h3>
        <form action="/login/vulnerable" method="POST">
            <input type="text" name="username" placeholder="USERNAME">
            <input type="password" name="password" placeholder="PASSWORD">
            <input type="submit" value="LOGIN (Vulnerable)">
        </form>

        <!-- Login Form with CSRF Protection -->
        <h3>> Protected Login (With CSRF):</h3>
        <form action="/login/protected" method="POST">
            <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
            <input type="text" name="username" placeholder="USERNAME">
            <input type="password" name="password" placeholder="PASSWORD">
            <input type="submit" value="LOGIN (Protected)">
        </form>

        <!-- Status Output -->
        <div class="status" id="status">
            {{ message if message else 'Ready for testing...' }}
        </div>
    </div>
</body>
</html>
"""

# Routes
@app.route('/')
def index():
    return render_template_string(TEMPLATE)

# Vulnerable route (no CSRF protection)
@app.route('/login/vulnerable', methods=['POST'])
@csrf.exempt  # Explicitly disable CSRF protection
def login_vulnerable():
    username = request.form.get('username')
    password = request.form.get('password')
    return jsonify({
        "status": "success",
        "message": f"Vulnerable login attempted with {username}",
        "csrf_status": "No Protection"
    })

# Protected route (with CSRF protection)
@app.route('/login/protected', methods=['POST'])
def login_protected():
    username = request.form.get('username')
    password = request.form.get('password')
    return jsonify({
        "status": "success",
        "message": f"Protected login attempted with {username}",
        "csrf_status": "Protected"
    })

if __name__ == '__main__':
    context = ('certs/localhost.pem', 'certs/localhost-key.pem')
    app.run(port=8443, ssl_context=context, debug=True)