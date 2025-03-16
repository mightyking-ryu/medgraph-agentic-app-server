<?php

// CORS 설정
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type, Authorization");

$request_method = $_SERVER["REQUEST_METHOD"];
$request_uri = parse_url($_SERVER["REQUEST_URI"], PHP_URL_PATH); // 요청 URI만 추출

// 요청 메서드가 OPTIONS일 경우, 빠르게 응답하여 CORS 처리
if ($request_method == 'OPTIONS') {
    header("HTTP/1.0 200 OK");
    exit();
}

// API 라우팅 처리
switch ($request_uri) {
    case '/api/submit_survey':
        if ($request_method == 'POST') {
            include(__DIR__ . '/endpoints/submit_survey.php');
        } else {
            header("HTTP/1.0 405 Method Not Allowed");
        }
        break;

    case '/api/ask_question':
        if ($request_method == 'POST') {
            include(__DIR__ . '/endpoints/ask_question.php');
        } else {
            header("HTTP/1.0 405 Method Not Allowed");
        }
        break;

    case '/api/fetch_response':
        if ($request_method == 'POST') {
            include(__DIR__ . '/endpoints/fetch_response.php');
        } else {
            header("HTTP/1.0 405 Method Not Allowed");
        }
        break;

    default:
        header("HTTP/1.0 404 Not Found");
        break;
}

?>
