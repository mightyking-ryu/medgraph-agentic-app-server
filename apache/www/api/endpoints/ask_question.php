<?php

include(__DIR__ . '/../../config/database.php');
include(__DIR__ . '/../utils/generate_uuid.php');

function ask_question($conn) {

    $input = file_get_contents('php://input');
    $data = json_decode($input, true);

    if (!isset($data['user_id']) || !isset($data['question'])) {
        echo json_encode([
            "status" => "error",
            "message" => "Missing parameters"
        ]);
        return;
    }

    $user_id = $data['user_id'];
    $question_id = generate_uuid();
    $question = $data['question'];

    $query = "INSERT INTO question_queue (user_id, question_id, question) VALUES (?,?,?)";
    $stmt = $conn->prepare($query);
    $stmt->bind_param("sss", $user_id, $question_id, $question);
    
    if ($stmt->execute()) {
        $response = array(
            "status" => "success",
            "message" => "Your question has been received",
            "question_id" => $question_id
        );
        echo json_encode($response);
    } else {
        $response = array(
            "status" => "error",
            "message" => $stmt->error
        );
        echo json_encode($response);
    }
}

ask_question($conn);
$conn->close();

?>