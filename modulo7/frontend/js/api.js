document.getElementById('load-items').addEventListener('click', async () => {
    const response = await fetch('http://localhost:8000/api/v1/public/items');

    if (!response.ok) {
        console.error('Error:', response.status);
        return;
    }

    const items = await response.json();
    const container = document.getElementById('items-container');

    container.innerHTML = items.map(item => `
        <div>
            <h3>${item.name}</h3>
            <p>${item.description}</p>
        </div>
    `).join('');
});