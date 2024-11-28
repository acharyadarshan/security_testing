from flask import Flask, request, render_template_string, make_response
import ssl

app = Flask(__name__)

# Template with test elements
TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Security Headers Test</title>
    <style>
        body {
            background-color: #000;
            color: #00ff00;
            font-family: 'Courier New', monospace;
            padding: 20px;
        }
        .console {
            border: 1px solid #00ff00;
            padding: 20px;
            margin: 20px;
            background-color: rgba(0, 20, 0, 0.9);
        }
        iframe {
            border: 1px solid #00ff00;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="console">
        <h1>_Security_Headers_Test_Console_</h1>
        
        <!-- Test elements for security headers -->
        <div id="tests">
            <h3>Testing Elements:</h3>
            <iframe src="about:blank" width="300" height="100"></iframe>
            <img src="http://example.com/image.jpg" alt="Mixed content test">
            <script>
                console.log("Inline script execution test");
            </script>
        </div>

        <div id="output" class="console">
            {{ message if message else 'Ready for header testing...' }}
        </div>
    </div>
</body>
</html>
"""

def security_headers(response):
    """Add security headers to response"""
    
    # HTTP Strict Transport Security
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    
    # Content Security Policy
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; "
        "frame-ancestors 'none'; "
        "form-action 'self'"
    )
    
    # X-Frame-Options (Clickjacking Protection)
    response.headers['X-Frame-Options'] = 'DENY'
    
    # X-Content-Type-Options (MIME-type sniffing protection)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    
    # X-XSS-Protection
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    # Referrer Policy
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    # Permissions Policy
    response.headers['Permissions-Policy'] = (
        'camera=(), '
        'microphone=(), '
        'geolocation=()'
    )
    
    return response

@app.route('/')
def index():
    response = make_response(render_template_string(TEMPLATE))
    return security_headers(response)

@app.route('/test-headers')
def test_headers():
    response = make_response('Header Test Endpoint')
    return security_headers(response)

if __name__ == '__main__':
    context = ('certs/localhost.pem', 'certs/localhost-key.pem')
    app.run(port=8443, ssl_context=context, debug=True)