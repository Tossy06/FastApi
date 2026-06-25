document.getElementById("login-form").addEventListener("submit", async (event) =>{
    event.preventDefault()


    const username = document.getElementById("login-email").value;
    const password = document.getElementById("login-password").value;

    const item = new URLSearchParams();
    item.append("username", username);
    item.append("password", password);

    const response = await fetch("http://localhost:8000/api/v1/auth/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: item

    });

    const data = await response.json();
    const loginAlert = document.getElementById("login-alert");

    if (response.ok) {
        window.location.href = "gallery.html";
        return;
    }

    loginAlert.textContent = data.detail;
    loginAlert.classList.remove("d-none");
})

document.getElementById("register-form").addEventListener("submit", async (event) => {
    event.preventDefault()

    const email = document.getElementById("register-email").value;
    const password = document.getElementById("register-password").value;
    const passwordConfirm = document.getElementById("register-password-confirm").value;
    const registerAlert = document.getElementById("register-alert");

    if (password !== passwordConfirm) {
        registerAlert.textContent = "Las contraseñas no coinciden";
        registerAlert.classList.remove("d-none");
        return;
    }

    const item = {
        email: email,
        password: password
    };

    const response = await fetch("http://localhost:8000/api/v1/auth/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(item)
    });

    const data = await response.json();

    if (!response.ok) {
        registerAlert.textContent = data.detail;
        registerAlert.classList.remove("d-none");
    }
})