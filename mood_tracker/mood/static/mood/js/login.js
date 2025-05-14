    async function requestCode() {
        const email = document.getElementById('email').value;
        const res = await fetch('/api/auth/request-code/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email })
        });

        if (res.ok) {
            document.getElementById('step-email').style.display = 'none';
            document.getElementById('step-code').style.display = 'block';
            document.getElementById('message').textContent = "Код надіслано на пошту!";
        } else {
            document.getElementById('message').textContent = "Помилка. Спробуйте ще раз.";
        }
    }

    async function verifyCode() {
        const email = document.getElementById('email').value;
        const code = document.getElementById('code').value;
        const res = await fetch('/api/auth/verify-code/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, code })
        });

        if (res.ok) {
            const data = await res.json();
            localStorage.setItem('access_token', data.access); // JWT
            window.location.href = "/dashboard/";
        } else {
            document.getElementById('message').textContent = "Неправильний код, спробуйте знову.";
        }
    }