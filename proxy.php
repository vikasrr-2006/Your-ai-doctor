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

// Remove the XAMPP path prefix
$path_prefix = '/new%20help/Your%20AI%20Doctor';
$request_uri = str_replace($path_prefix, '', $request_uri);

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

// Set proper headers
$headers = array();
$headers[] = 'Content-Type: ' . ($_SERVER['CONTENT_TYPE'] ?? 'application/json');
$headers[] = 'Accept: application/json';

// Forward additional headers
foreach ($_SERVER as $key => $value) {
    if (strpos($key, 'HTTP_') === 0) {
        $header_name = str_replace('_', '-', substr($key, 5));
        if ($header_name !== 'HOST') {
            $headers[] = "$header_name: $value";
        }
    }
}
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

// Execute the request
$response = curl_exec($ch);
$http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$content_type = curl_getinfo($ch, CURLINFO_CONTENT_TYPE);

// Close cURL session
curl_close($ch);

// Set the response headers
if ($content_type) {
    header("Content-Type: $content_type");
}
http_response_code($http_code);

// Output the response
echo $response;
?>
