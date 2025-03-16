document.addEventListener("DOMContentLoaded", function () {
    let currentStep = 0;
    const steps = document.querySelectorAll(".step");
    const progress = document.getElementById("progress");
    const finalPage = document.querySelector(".final-page");

    function showStep(step) {
        steps.forEach((s, index) => {
            s.classList.toggle("active", index === step);
        });
        progress.style.width = `${(step / (steps.length - 1)) * 100}%`;
    }

    document.querySelectorAll(".next-btn").forEach((button) => {
        button.addEventListener("click", function () {
            if (currentStep < steps.length - 1) {
                currentStep++;
                showStep(currentStep);
            }
        });
    });

    document.querySelectorAll(".prev-btn").forEach((button) => {
        button.addEventListener("click", function () {
            if (currentStep > 0) {
                currentStep--;
                showStep(currentStep);
            }
        });
    });

    document.getElementById("survey-form").addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent page reload

        // Hide all form steps
        steps.forEach(step => step.style.display = "none");
    
        // Show the final page
        finalPage.style.display = "block";
    
        // Ensure countdown element exists
        const countdownElement = document.getElementById("countdown");
        if (!countdownElement) {
            console.error("Countdown element not found!");
            return;
        }

        // 폼 데이터 수집을 위한 객체 생성
        const data = {};

        // 모든 .step 요소 중 'Welcome' 문구가 포함된 시작 페이지를 제외하고 처리합니다.
        steps.forEach((step) => {
            const header = step.querySelector("h2");
            if (header && header.textContent.includes("Welcome")) {
                return;
            }

            // step 내부의 input, select, textarea 요소를 순회하여 값 수집
            const elements = step.querySelectorAll("input, select, textarea");
            elements.forEach((el) => {
                if (!el.name) return; // name 속성이 없으면 무시

                // radio는 선택된 값만 저장
                if (el.type === "radio") {
                    if (el.checked) {
                        data[el.name] = el.value;
                    }
                }
                // checkbox는 여러 선택이 가능하므로, 체크된 값들을 배열로 저장
                else if (el.type === "checkbox") {
                    if (el.checked) {
                        if (data.hasOwnProperty(el.name)) {
                            if (Array.isArray(data[el.name])) {
                                data[el.name].push(el.value);
                            } else {
                                data[el.name] = [data[el.name], el.value];
                            }
                        } else {
                            data[el.name] = el.value;
                        }
                    }
                }
                // 나머지 input, select, textarea는 값 저장
                else {
                    data[el.name] = el.value;
                }
            });
        });

        // 최종 payload를 { "result": data } 형식으로 감쌉니다.
        const payload = {
            result: JSON.stringify(data)
        };

        // JSON 문자열로 변환
        const jsonData = JSON.stringify(payload);
        console.log("Collected Survey Data:", jsonData);

        fetch("/api/endpoints/submit_survey.php", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: jsonData
        })
        .then((response) => response.json())
        .then((result) => {
            console.log("Server Response:", result);
            
            // user_id 저장 (sessionStorage를 사용하면 현재 탭에서만 유지됨)
            sessionStorage.setItem("user_id", result.user_id);
        
        })
        .catch((error) => {
            console.error("AJAX Error:", error);
        });        
    
        // Countdown logic
        let countdown = 5;
        countdownElement.textContent = countdown;
    
        const interval = setInterval(() => {
            countdown--;
            countdownElement.textContent = countdown;
    
            if (countdown === 0) {
                clearInterval(interval);
                console.log("Redirecting to chat.html...");
                window.location.href = "/chat"; // Redirect to chat page
            }
        }, 1000);
    });

    // Ensure the final page is hidden initially
    finalPage.style.display = "none";

    // Initialize the first step
    showStep(currentStep);
});
