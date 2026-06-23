<?php
/**
 * Index file for Your AI Doctor Flask Application
 * This file serves as the entry point for accessing the Flask app through XAMPP
 */

// Check if the Flask app is running
$flask_host = '127.0.0.1';
$flask_port = 5000;
$flask_url = "http://{$flask_host}:{$flask_port}";

// Try to connect to Flask app
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $flask_url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_TIMEOUT, 5);
curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 5);
$response = curl_exec($ch);
$http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

// If Flask app is not running, show instructions
if ($http_code !== 200) {
    ?>
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Your AI Doctor - Setup Required</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }
            .container {
                background: white;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                max-width: 600px;
                width: 90%;
            }
            h1 {
                color: #333;
                margin-bottom: 10px;
            }
            .subtitle {
                color: #666;
                margin-bottom: 30px;
            }
            .alert {
                background: #fff3cd;
                border: 1px solid #ffc107;
                color: #856404;
                padding: 15px;
                border-radius: 5px;
                margin-bottom: 20px;
            }
            .steps {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 5px;
                margin-bottom: 20px;
            }
            .steps h3 {
                margin-top: 0;
                color: #333;
            }
            .steps ol {
                margin: 0;
                padding-left: 20px;
            }
            .steps li {
                margin-bottom: 10px;
                line-height: 1.6;
            }
            code {
                background: #e9ecef;
                padding: 2px 6px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
            }
            .btn {
                display: inline-block;
                background: #667eea;
                color: white;
                padding: 12px 24px;
                text-decoration: none;
                border-radius: 5px;
                margin-top: 10px;
                border: none;
                cursor: pointer;
                font-size: 16px;
            }
            .btn:hover {
                background: #5a6fd6;
            }
            .btn-success {
                background: #28a745;
            }
            .btn-success:hover {
                background: #218838;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Your AI Doctor</h1>
            <p class="subtitle">Medical Symptom Prediction System</p>
            
            <div class="alert">
                <strong>Flask Application Not Running</strong><br>
                The Flask backend is not currently running. Please start it first.
            </div>
            
            <div class="steps">
                <h3>Setup Instructions:</h3>
                <ol>
                    <li>Open a terminal/command prompt</li>
                    <li>Navigate to the Flask application directory:<br>
                        <code>cd "c:\xampp\htdocs\new help\Your AI Doctor"</code>
                    </li>
                    <li>Start the Flask application:<br>
                        <code>python app.py</code>
                    </li>
                    <li>Wait for the message: <code>Running on http://127.0.0.1:5000</code></li>
                    <li>Refresh this page or click the button below</li>
                </ol>
            </div>
            
            <a href="index.php" class="btn">Refresh Page</a>
            <button onclick="window.location.reload()" class="btn btn-success">Go to Flask App</button>
        </div>
    </body>
    </html>
    <?php
    exit;
}

// If Flask app is running, proxy the request directly
$request_uri = $_SERVER['REQUEST_URI'];
$path_prefix = '/new%20help/Your%20AI%20Doctor';
$request_uri = str_replace($path_prefix, '', $request_uri);
if (empty($request_uri) || $request_uri === '/') {
    $request_uri = '/';
}
$flask_url = "http://{$flask_host}:{$flask_port}{$request_uri}";

// Initialize cURL session
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $flask_url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $_SERVER['REQUEST_METHOD']);

// Handle POST data
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $post_data = file_get_contents('php://input');
    curl_setopt($ch, CURLOPT_POSTFIELDS, $post_data);
}

// Set headers
$headers = array();
$headers[] = 'Content-Type: ' . ($_SERVER['CONTENT_TYPE'] ?? 'application/json');
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

// Execute request
$response = curl_exec($ch);
$http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$content_type = curl_getinfo($ch, CURLINFO_CONTENT_TYPE);
curl_close($ch);

// Set response headers and output
if ($content_type) {
    header("Content-Type: $content_type");
}
http_response_code($http_code);
echo $response;
?>
