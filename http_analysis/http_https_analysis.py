from flask import Flask, render_template_string, request
import json

app = Flask(__name__)

# HTML template for the console
TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Security Analysis Console</title>
    <style>
        body {
            background-color: #0a0a0a;
            color: #00ff00;
            font-family: 'Courier New', monospace;
            margin: 0;
            padding: 20px;
        }
        .console {
            background-color: rgba(0, 0, 0, 0.8);
            border: 1px solid #00ff00;
            border-radius: 5px;
            padding: 20px;
            max-width: 800px;
            margin: 20px auto;
            box-shadow: 0 0 10px #00ff00;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .header h1 {
            color: #00ff00;
            text-shadow: 0 0 5px #00ff00;
        }
        .form-group {
            margin-bottom: 15px;
        }
        input[type="text"], input[type="password"] {
            background-color: #000;
            border: 1px solid #00ff00;
            color: #00ff00;
            padding: 8px;
            width: 100%;
            margin-top: 5px;
            font-family: 'Courier New', monospace;
        }
        input[type="submit"] {
            background-color: #000;
            color: #00ff00;
            border: 1px solid #00ff00;
            padding: 10px 20px;
            cursor: pointer;
            font-family: 'Courier New', monospace;
            transition: all 0.3s;
        }
        input[type="submit"]:hover {
            background-color: #00ff00;
            color: #000;
        }
        .status {
            margin-top: 20px;
            padding: 10px;
            border: 1px solid #00ff00;
        }
        .matrix-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
            opacity: 0.1;
        }
        @keyframes blink {
            0% { opacity: 1; }
            50% { opacity: 0; }
            100% { opacity: 1; }
        }
        .blink {
            animation: blink 1s infinite;
        }
    </style>
</head>
<body>
    <canvas id="matrix" class="matrix-bg"></canvas>
    <div class="console">
        <div class="header">
            <h1>_Security Analysis Console_</h1>
            <p class="blink">>_ Ready for transmission...</p>
        </div>
        
        <form action="/api/test" method="POST" id="securityForm">
            <div class="form-group">
                <label for="username">>_ Username:</label><br>
                <input type="text" id="username" name="username" placeholder="Enter username">
            </div>
            <div class="form-group">
                <label for="password">>_ Password:</label><br>
                <input type="password" id="password" name="password" placeholder="Enter password">
            </div>
            <div class="form-group">
                <input type="submit" value="TRANSMIT">
            </div>
        </form>
        
        <div class="status" id="status"></div>
    </div>

    <script>
        // Matrix rain effect
        const canvas = document.getElementById('matrix');
        const ctx = canvas.getContext('2d');

        canvas.height = window.innerHeight;
        canvas.width = window.innerWidth;

        const chars = "アイウエオカキクケコサシスセソタチツテトナニヌネハヒフヘホマミムメモヤユヨラリルレワヲン0123456789";
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

        // Form submission handling
        document.getElementById('securityForm').onsubmit = function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            fetch('/api/test', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('status').innerHTML = 
                    `>_ Transmission complete...<br>>_ Payload: ${JSON.stringify(data, null, 2)}`;
            });
        };
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(TEMPLATE)

@app.route('/api/test', methods=['POST'])
def test_endpoint():
    sensitive_data = {
        "username": request.form.get('username', ''),
        "password": request.form.get('password', ''),
        "timestamp": "INTERCEPTED",
        "status": "TRANSMISSION_COMPLETE"
    }
    return json.dumps(sensitive_data)

if __name__ == '__main__':
    # For HTTP testing
    #app.run(port=5000, debug=True)
    
    # For HTTPS testing (uncomment below)
    context = ('certs/localhost.pem', 'certs/localhost-key.pem')
    app.run(port=8443, ssl_context=context, debug=True)