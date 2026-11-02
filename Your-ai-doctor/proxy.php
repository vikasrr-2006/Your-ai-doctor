<?php
/**
 * PHP Proxy Script for Flask Application
 * This script proxies requests from XAMPP Apache to the Flask application
 */

// Flask app configuration
$flask_host = '127.0.0.1';
$flask_port = 5000;

// Get the request URI and method
$request_uri = $_SERVER['REQUEST_URI'];
$request_method = $_SERVER['REQUEST_METHOD'];

// Remove the XAMPP path prefix (handle both encoded and decoded spaces)
$path_prefix_encoded = '/new%20help/Your%20AI%20Doctor';
$path_prefix_decoded = '/new help/Your AI Doctor';
$request_uri = str_replace($path_prefix_encoded, '', $request_uri);
$request_uri = str_replace($path_prefix_decoded, '', $request_uri);

// Remove proxy.php from the URI if present
$request_uri = str_replace('/proxy.php', '', $request_uri);

// Default to root if empty
if (empty($request_uri) || $request_uri === '/') {
    $request_uri = '/';
}

// Build the Flask URL
$flask_url = "http://{$flask_host}:{$flask_port}{$request_uri}";

// Initialize cURL session
$ch = curl_init();

// Set cURL options
curl_setopt($ch, CURLOPT_URL, $flask_url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $request_method);

// Handle POST data
if ($request_method === 'POST') {
    $post_data = file_get_contents('php://input');
    curl_setopt($ch, CURLOPT_POSTFIELDS, $post_data);
}

// Set headers - only forward Content-Type if present, don't force Accept header
$headers = array();

if (!empty($_SERVER['CONTENT_TYPE'])) {
    $headers[] = 'Content-Type: ' . $_SERVER['CONTENT_TYPE'];
}

// Forward additional headers
foreach ($_SERVER as $key => $value) {
    if (strpos($key, 'HTTP_') === 0) {
        $header_name = str_replace('_', '-', substr($key, 5));
        if ($header_name !== 'HOST' && $header_name !== 'ACCEPT') {
            $headers[] = "$header_name: $value";
        }
    }
}

if (!empty($headers)) {
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
}

// Execute the request
$response = curl_exec($ch);
$http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$content_type = curl_getinfo($ch, CURLINFO_CONTENT_TYPE);
$curl_error = curl_error($ch);

// Close cURL session
curl_close($ch);

// Handle cURL errors
if ($response === false || !empty($curl_error)) {
    http_response_code(502);
    header('Content-Type: text/html; charset=utf-8');
    echo '<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Proxy Error</title>
        <style>
            body { font-family: sans-serif; padding: 40px; background: #f8f9fa; }
            .error { background: #fff; padding: 30px; border-radius: 8px; max-width: 600px; margin: 0 auto; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #dc3545; }
            code { background: #e9ecef; padding: 2px 6px; border-radius: 4px; }
        </style>
    </head>
    <body>
        <div class="error">
            <h1>Backend Connection Error</h1>
            <p>The Flask backend is not responding.</p>
            <p>Error: <code>' . htmlspecialchars($curl_error) . '</code></p>
            <p>Please ensure the Flask app is running on port 5000.</p>
        </div>
    </body>
    </html>';
    exit;
}

// Set the response headers
if ($content_type) {
    header("Content-Type: $content_type");
}
http_response_code($http_code);

// Output the response
echo $response;
?>
