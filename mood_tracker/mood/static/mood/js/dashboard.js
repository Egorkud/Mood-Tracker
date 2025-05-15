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

    async function loadMoodChart() {
        const token = localStorage.getItem("access_token");
        const res = await fetch("/api/mood/week/", {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (!res.ok) {
            console.error("Не вдалося завантажити графік.");
            return;
        }

        const data = await res.json();

        // Сортуємо по даті
        data.sort((a, b) => new Date(a.date) - new Date(b.date));

        const labels = data.map(entry => entry.date);
        const moodLevels = data.map(entry => {
            switch (entry.mood) {
                case "excited":
                    return 5
                case "happy":
                    return 4;
                case "neutral":
                    return 3;
                case "anxious":
                    return 2;
                case "sad":
                    return 1
                case "angry":
                    return 0;
            }
        });

        const ctx = document.getElementById('moodChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Рівень настрою',
                    data: moodLevels,
                    fill: false,
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.3,
                    pointRadius: 6,
                    pointBackgroundColor: 'rgb(75, 192, 192)'
                }]
            },
            options: {
                scales: {
                    y: {
                        min: 0,
                        max: 5,
                        ticks: {
                            callback: function (value) {
                                if (value === 5) return 'Задоволений';
                                if (value === 4) return 'Щасливий';
                                if (value === 3) return 'Нейтральний';
                                if (value === 2) return 'Тривожний';
                                if (value === 1) return 'Сумний';
                                if (value === 0) return 'Злий';
                                return '';
                            },
                            stepSize: 1
                        }
                    }
                }
            }
        });
    }

    loadMoodChart();


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
