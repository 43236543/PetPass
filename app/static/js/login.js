const form = document.getElementById("login-form");
const message = document.getElementById("login-message");
const button = document.getElementById("login-button");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    message.textContent = "";
    message.className = "message";

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value;

    button.disabled = true;
    button.textContent = "Входим...";

    try {
        const response = await fetch("/api/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || "Не удалось войти.");
        }

        window.location.href = "/";

    } catch (error) {
        message.textContent = error.message;
        message.classList.add("error");
    } finally {
        button.disabled = false;
        button.textContent = "Войти";
    }
});
