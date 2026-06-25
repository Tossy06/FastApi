document.getElementById("item-form").addEventListener("submit", async (event) => {

    event.preventDefault();

    const name = document.getElementById("item-name").value;
    const description = document.getElementById("item-description").value;

    const item = {
        name: name,
        description: description
    };

    const response = await fetch("http://localhost:8000/api/v1/public/items", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(item)
    });

    const data = await response.json();

    const result = document.getElementById("create-result");

    if (response.ok) {
        result.textContent = `Item created: ${data.name}`;
    } else {
        result.textContent = `Error: ${data.detail}`;
    }

});