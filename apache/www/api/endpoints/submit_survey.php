<?php

include(__DIR__ . '/../../config/database.php');
include(__DIR__ . '/../utils/generate_uuid.php');

function submit_survey($conn) {

    $input = file_get_contents('php://input');
    $data = json_decode($input, true);

    if (!isset($data['result'])) {
        echo json_encode([
            "status" => "error",
            "message" => "Missing parameters"
        ]);
        return;
    }

    $user_id = generate_uuid();
    $result = $data['result'];

    $query = "INSERT INTO survey (user_id, result) VALUES (?,?)";
    $stmt = $conn->prepare($query);
    $stmt->bind_param("ss", $user_id, $result);
    
    if ($stmt->execute()) {
        $response = array(
            "status" => "success",
            "message" => "Survey submitted successfully",
            "user_id" => $user_id
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

submit_survey($conn);
$conn->close();

?>