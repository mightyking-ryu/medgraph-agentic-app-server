document.addEventListener("DOMContentLoaded", function () {
    const chatBox = document.getElementById("chat-box");
    const input = document.getElementById("user-input");
    const sendButton = document.querySelector("button");
    const userId = sessionStorage.getItem("user_id");

    if (!userId) {
        displayAIMessage("Please complete the survey first.");
        return;
    }

    function sendMessage() {
        const message = input.value.trim();
        if (message === "") return;

        sendButton.disabled = true; // 버튼 비활성화
    
        if (!chatBox.getAttribute("data-has-content")) {
            chatBox.setAttribute("data-has-content", "true");
            document.getElementById("placeholder").style.display = "none";
        }
    
        const userMessage = document.createElement("div");
        userMessage.classList.add("user-message");
        userMessage.textContent = message;
        chatBox.appendChild(userMessage);
        input.value = "";
        chatBox.scrollTop = chatBox.scrollHeight;
    
        const typingGif = document.createElement("img");
        typingGif.src = "/assets/images/question_loading.gif";
        typingGif.classList.add("typing-gif");
        chatBox.appendChild(typingGif);
        chatBox.scrollTop = chatBox.scrollHeight;
    
        fetch("/api/endpoints/ask_question.php", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id: userId, question: message })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                checkForResponse(data.question_id, typingGif);
            } else {
                chatBox.removeChild(typingGif);
                displayAIMessage("Error: " + data.message);
                sendButton.disabled = false; // 버튼 활성화
            }
        })
        .catch(error => {
            chatBox.removeChild(typingGif);
            displayAIMessage("Error: Failed to send message");
            sendButton.disabled = false; // 버튼 활성화
        });
    }

    function checkForResponse(questionId, typingGif) {
        let elapsedTime = 0;
        const maxWaitTime = 30000; // 30초
        const interval = setInterval(() => {
            if (elapsedTime >= maxWaitTime) {
                clearInterval(interval);
                chatBox.removeChild(typingGif);
                displayAIMessage("Error: Server timeout. Please try again later.");
                sendButton.disabled = false; // 버튼 활성화
                return;
            }
        
            fetch("/api/endpoints/fetch_response.php", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ user_id: userId, question_id: questionId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    clearInterval(interval);
                    chatBox.removeChild(typingGif);
                    displayAIMessage(data.response);
                    sendButton.disabled = false; // 버튼 활성화
                } else if (data.status === "error") {
                    clearInterval(interval);
                    chatBox.removeChild(typingGif);
                    displayAIMessage("Error: " + data.message);
                    sendButton.disabled = false; // 버튼 활성화
                }
                // "processing" 상태일 경우 아무 동작하지 않음 (계속 폴링)
            })
            .catch(error => {
                clearInterval(interval);
                chatBox.removeChild(typingGif);
                displayAIMessage("Error: Failed to fetch response");
                sendButton.disabled = false; // 버튼 활성화
            });
            elapsedTime += 2000;
        }, 2000); // 2초마다 확인
    }

    function displayAIMessage(text) {
        const aiMessage = document.createElement("div");
        aiMessage.classList.add("ai-message");
        aiMessage.textContent = text;
        chatBox.appendChild(aiMessage);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    sendButton.addEventListener("click", sendMessage);
});