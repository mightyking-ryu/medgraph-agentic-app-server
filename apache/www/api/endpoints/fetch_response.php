<?php

include(__DIR__ . '/../../config/database.php');

function fetch_response($conn) {

    $input = file_get_contents('php://input');
    $data = json_decode($input, true);

    if (!isset($data['user_id']) || !isset($data['question_id'])) {
        echo json_encode([
            "status" => "error",
            "message" => "Missing parameters"
        ]);
        return;
    }
    
    $user_id = $data['user_id'];
    $question_id = $data['question_id'];

    $query = "SELECT response FROM response_queue WHERE question_id = ? AND user_id = ? ORDER BY created_at ASC LIMIT 1";
    
    $stmt = $conn->prepare($query);
    if (!$stmt) {
        echo json_encode([
            "status" => "error",
            "message" => "SQL prepare error: " . $conn->error
        ]);
        return;
    }
    
    $stmt->bind_param("ss", $question_id, $user_id);
    
    $stmt->execute();
    $result = $stmt->get_result();

    if ($row = $result->fetch_assoc()) {
        $response = array(
            "status" => "success",
            "message" => "Response generated",
            "response" => $row['response']
        );
        echo json_encode($response);

        $delete_query = "DELETE FROM response_queue WHERE question_id = ? AND user_id = ? LIMIT 1";

        $delete_stmt = $conn->prepare($delete_query);
        if (!$delete_stmt) {
            error_log("SQL prepare error (DELETE): " . $conn->error);
            return;
        }

        $delete_stmt->bind_param("ss", $question_id, $user_id);

        if (!$delete_stmt->execute()) {
            error_log("Error deleting response: " . $delete_stmt->error);
        }

        return;
    }

    $query = "SELECT * FROM question_queue WHERE question_id = ? AND user_id = ? ORDER BY created_at ASC LIMIT 1";
    
    $stmt = $conn->prepare($query);
    if (!$stmt) {
        echo json_encode([
            "status" => "error",
            "message" => "SQL prepare error: " . $conn->error
        ]);
        return;
    }
    
    $stmt->bind_param("ss", $question_id, $user_id);
    
    $stmt->execute();
    $result = $stmt->get_result();

    if ($row = $result->fetch_assoc()) {
        $response = array(
            "status" => "processing",
            "message" => "Response in progress"
        );
        echo json_encode($response);
    } else {
        echo json_encode([
            "status" => "error",
            "message" => "No query found"
        ]);
    }
}

fetch_response($conn);
$conn->close();

?>
