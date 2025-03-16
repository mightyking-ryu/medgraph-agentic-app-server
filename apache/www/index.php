<?php

$request_uri = $_SERVER['REQUEST_URI'];

// API 요청 처리
if (strpos($request_uri, '/api/') === 0) {
    // API 라우팅 처리
    include_once('api/router.php'); // API 요청을 처리하는 별도의 파일로 라우팅
} else {
    // 일반 페이지 요청 처리
    switch ($request_uri) {
        case '/':
            include 'pages/home.html';  // home.html 페이지를 보여줌
            break;
        case '/chat':
            include 'pages/chat.html'; // about.html 페이지를 보여줌
            break;
        default:
            include 'pages/404.html'; // 그 외의 경우 404 페이지 제공
            break;
    }
}

?>