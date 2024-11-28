from flask import Flask, request, render_template_string, jsonify, session
import sqlite3
import ssl
import time
import random
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey123'  # Intentionally weak

# Intentional vulnerabilities
TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Security Analysis Console v1.0</title>
    <style>
        body {
            background-color: #000;
            color: #00ff00;
            font-family: 'Courier New', monospace;
            margin: 0;
            padding: 20px;
            line-height: 1.6;
        }
        
        .terminal {
            background-color: rgba(0, 20, 0, 0.9);
            border: 1px solid #00ff00;
            border-radius: 5px;
            padding: 20px;
            margin: 20px auto;
            max-width: 800px;
            box-shadow: 0 0 20px rgba(0, 255, 0, 0.2);
            position: relative;
            overflow: hidden;
        }
        
        .terminal::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 25px;
            background: linear-gradient(to bottom, #001f00, transparent);
            pointer-events: none;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            text-shadow: 0 0 10px #00ff00;
        }
        
        .status-bar {
            border-top: 1px solid #00ff00;
            margin-top: 20px;
            padding-top: 10px;
            font-size: 0.9em;
            opacity: 0.8;
        }
        
        input {
            background-color: #001100;
            border: 1px solid #00ff00;
            color: #00ff00;
            padding: 8px 12px;
            margin: 5px 0;
            width: 100%;
            font-family: 'Courier New', monospace;
        }
        
        input[type="submit"] {
            background-color: #003300;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        input[type="submit"]:hover {
            background-color: #004400;
            box-shadow: 0 0 10px #00ff00;
        }
        
        .console-output {
            background-color: #001100;
            border: 1px solid #004400;
            padding: 10px;
            margin: 10px 0;
            min-height: 100px;
            position: relative;
        }
        
        @keyframes blink {
            0% { opacity: 1; }
            50% { opacity: 0; }
            100% { opacity: 1; }
        }
        
        .cursor {
            display: inline-block;
            width: 8px;
            height: 15px;
            background: #00ff00;
            margin-left: 5px;
            animation: blink 1s infinite;
        }
        
        .error {
            color: #ff0000;
            text-shadow: 0 0 5px #ff0000;
        }
        
        .success {
            color: #00ff00;
            text-shadow: 0 0 5px #00ff00;
        }
        
        #matrix-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
        }
        
        .vulnerable-search {
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid #004400;
        }
    </style>
</head>
<body>
    <canvas id="matrix-bg"></canvas>
    
    <div class="terminal">
        <div class="header">
            <h1>_SECURITY_ANALYSIS_CONSOLE_</h1>
            <p class="status">SYS.STATUS: {{ status if status else 'READY' }} <span class="cursor"></span></p>
        </div>

        <!-- Login Form - Vulnerable to SQL Injection -->
        <div class="section">
            <h3>> Authentication_Module:</h3>
            <form method="POST" action="/login" id="login-form">
                <input type="text" name="username" placeholder="ENTER_USERNAME" required>
                <input type="password" name="password" placeholder="ENTER_PASSWORD" required>
                <input type="submit" value="AUTHENTICATE">
            </form>
        </div>

        <!-- Search Form - Vulnerable to XSS -->
        <div class="vulnerable-search">
            <h3>> Search_Module:</h3>
            <form method="GET" action="/search">
                <input type="text" name="q" placeholder="ENTER_SEARCH_QUERY">
                <input type="submit" value="EXECUTE_SEARCH">
            </form>
        </div>

        <!-- Output Console -->
        <div class="console-output" id="output">
            {{ message | safe if message else 'Awaiting input...' }}
        </div>

        <div class="status-bar">
            <p>SYS.INFO: Running vulnerable test environment</p>
            <p>NODE: {{ request.remote_addr }} | TIME: {{ time }}</p>
        </div>
    </div>

    <script>
        // Matrix rain effect
        const canvas = document.getElementById('matrix-bg');
        const ctx = canvas.getContext('2d');

        canvas.height = window.innerHeight;
        canvas.width = window.innerWidth;

        const chars = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヰヱヲン0123456789";
        const matrix = chars.split('');
        const fontSize = 10;
        const columns = canvas.width/fontSize;
        const drops = [];

        for(let x = 0; x < columns; x++)
            drops[x] = 1;

        function draw() {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.04)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            ctx.fillStyle = '#0F0';
            ctx.font = fontSize + 'px monospace';

            for(let i = 0; i < drops.length; i++) {
                const text = matrix[Math.floor(Math.random()*matrix.length)];
                ctx.fillText(text, i*fontSize, drops[i]*fontSize);

                if(drops[i]*fontSize > canvas.height && Math.random() > 0.975)
                    drops[i] = 0;

                drops[i]++;
            }
        }

        setInterval(draw, 33);

        // Simulated typing effect
        function typeEffect(element, text, speed = 50) {
            let i = 0;
            element.innerHTML = '';
            const timer = setInterval(() => {
                if (i < text.length) {
                    element.innerHTML += text.charAt(i);
                    i++;
                } else {
                    clearInterval(timer);
                }
            }, speed);
        }

        // Form submission with fetch
        document.getElementById('login-form').onsubmit = function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            fetch('/login', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                const output = document.getElementById('output');
                typeEffect(output, data.message);
            });
        };
    </script>
</div>
</body>
</html>
"""

# Database initialization with vulnerable queries
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT, password TEXT, access_level TEXT)''')
    # Add some test users
    c.execute("INSERT OR IGNORE INTO users VALUES ('admin', 'secretpass123', 'admin')")
    c.execute("INSERT OR IGNORE INTO users VALUES ('user', 'password123', 'user')")
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template_string(TEMPLATE, time=time.strftime("%Y-%m-%d %H:%M:%S"))

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Vulnerable SQL query
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    try:
        c.execute(query)
        user = c.fetchone()
        if user:
            return jsonify({"status": "success", 
                          "message": f"ACCESS_GRANTED: Welcome {username}\nAccess Level: {user[2]}"})
        return jsonify({"status": "error", 
                       "message": "ACCESS_DENIED: Invalid credentials"})
    except sqlite3.Error as e:
        return jsonify({"status": "error", 
                       "message": f"DATABASE_ERROR: {str(e)}"})
    finally:
        conn.close()

@app.route('/search')
def search():
    query = request.args.get('q', '')
    # Vulnerable to XSS
    return render_template_string(TEMPLATE, 
                                message=f"SEARCH_RESULTS_FOR: {query}", 
                                time=time.strftime("%Y-%m-%d %H:%M:%S"))

@app.route('/api/data')
def get_data():
    # Vulnerable to information disclosure
    data = {
        "internal_ips": ["192.168.1.1", "10.0.0.1"],
        "api_keys": ["sk_test_12345", "pk_live_67890"],
        "debug_mode": True
    }
    return jsonify(data)

if __name__ == '__main__':
    init_db()
    context = ('certs/localhost.pem', 'certs/localhost-key.pem')
    
    # Intentionally weak SSL configuration
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    ssl_context.load_cert_chain(context[0], context[1])
    ssl_context.set_ciphers('ALL:@SECLEVEL=0')  # Weak ciphers
    
    app.run(port=8443, ssl_context=ssl_context, debug=True)