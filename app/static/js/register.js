
const form = document.getElementById("register-form");
const message = document.getElementById("register-message");
const button = document.getElementById("register-button");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    message.textContent = "";
    message.className = "message";

    const fullName = document.getElementById("full-name").value.trim();
    const phone = document.getElementById("phone").value.trim();
    const email = document.getElementById("email").value.trim();
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value;
    const passwordConfirm = document.getElementById("password-confirm").value;
    const nameParts = fullName.split(/\s+/);

    if (nameParts.length < 2 || nameParts.length > 3) {
        message.textContent = "Введите фамилию, имя и при необходимости отчество.";
        message.classList.add("error");
        return;
    }

    if (password !== passwordConfirm) {
        message.textContent = "Пароли не совпадают.";
        message.classList.add("error");
        return;
    }

    const userData = {
        last_name: nameParts[0],
        first_name: nameParts[1],
        middle_name: nameParts[2] || null,
        phone: phone,
        email: email,
        username: username,
        password: password
    };

    button.disabled = true;
    button.textContent = "Регистрация...";

    try {
        const response = await fetch("/api/auth/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(userData)
        });

        const result = await response.json();

        if (!response.ok) {
            const errorText = Array.isArray(result.detail)
                ? result.detail.map(item => item.msg).join(" ")
                : result.detail;

            throw new Error(errorText || "Не удалось зарегистрироваться.");
        }

        message.textContent = "Регистрация прошла успешно!";
        message.classList.add("success");

        form.reset();

        setTimeout(() => {
            window.location.href = "/login.html";
        }, 1500);

    } catch (error) {
        message.textContent = error.message;
        message.classList.add("error");
    } finally {
        button.disabled = false;
        button.textContent = "Зарегистрироваться";
    }
});
