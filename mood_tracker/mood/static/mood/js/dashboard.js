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

        async function getUsername() {
            const token = localStorage.getItem("access_token");
            const res = await fetch("/api/user-info/", {
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            });
                if (res.ok) {
                    const data = await res.json();
                    document.getElementById("username-display").textContent = data.username;
                }
        }
        getUsername();

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

        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        const token = localStorage.getItem('access_token');
        const response = await fetch("/api/mood/create/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ mood: emotion, note: message, date })
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
