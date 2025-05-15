document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("mood-form");
    const emotionButtons = document.querySelectorAll(".emotion-btn");
    const emotionInput = document.getElementById("emotion");


    // Обробка кнопки "Вихід"
    const logoutBtn = document.getElementById("logout-btn");
    logoutBtn.addEventListener("click", () => {
        // Видаляємо токени з localStorage
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");

        // Перенаправляємо на сторінку логіну
        window.location.href = "/login";
    });

    // Функція перевірки токена
    async function checkTokenValidity() {
        const token = localStorage.getItem("access_token");
        if (!token) {
            window.location.href = "http://127.0.0.1:8000/login";
            return false;
        }

        const res = await fetch("/api/user-info/", {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (res.ok) {
            const data = await res.json();
            document.getElementById("username-display").textContent = data.username;
            return true;
        } else {
            localStorage.removeItem("access_token");
            window.location.href = "http://127.0.0.1:8000/login";
            return false;
        }
    }

    // Виклик перевірки при завантаженні
    checkTokenValidity();

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

        const token = localStorage.getItem('access_token');
        if (!token) {
            window.location.href = "http://127.0.0.1:8000/login";
            return;
        }

        const emotion = emotionInput.value;
        const message = document.getElementById("message").value;
        const date = document.getElementById("date").value;

        if (!emotion) {
            alert("Оберіть емоцію!");
            return;
        }

        const response = await fetch("/api/mood/create/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({mood: emotion, note: message, date})
        });

        if (response.ok) {
            alert("Запис збережено!");
            form.reset();
            emotionButtons.forEach(btn => btn.classList.remove("btn-primary"));
        } else if (response.status === 401) {
            localStorage.removeItem("access_token");
            window.location.href = "http://127.0.0.1:8000/login";
        } else {
            alert("Помилка при збереженні запису.");
        }
    });
});
