document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("mood-form");
    const emotionButtons = document.querySelectorAll(".emotion-btn");
    const emotionInput = document.getElementById("emotion");

    // Вибір емоції
    emotionButtons.forEach(button => {
        button.addEventListener("click", () => {
            emotionButtons.forEach(btn => btn.classList.remove("btn-primary"));
            button.classList.add("btn-primary");
            emotionInput.value = button.getAttribute("data-emotion");
        });
    });

    // Відправка форми
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const emotion = emotionInput.value;
        const message = document.getElementById("message").value;
        const date = document.getElementById("date").value;

        if (!emotion) {
            alert("Оберіть емоцію!");
            return;
        }

        const token = localStorage.getItem("access_token");
        const response = await fetch("/api/mood/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ emotion, message, date })
        });

        if (response.ok) {
            alert("Запис збережено!");
            form.reset();
            emotionButtons.forEach(btn => btn.classList.remove("btn-primary"));
        } else {
            alert("Помилка при збереженні запису.");
        }
    });
});
