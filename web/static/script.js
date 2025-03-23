fetch('/api/news')
    .then(response => response.json())
    .then(data => {
        const newsList = document.getElementById('news-list');
        data.forEach(news => {
            const div = document.createElement('div');
            div.className = 'news-item';
            div.innerHTML = `
                <h2>${news.title}</h2>
                <p><strong>Category:</strong> ${news.category}</p>
                <p>${news.summary}</p>
            `;
            newsList.appendChild(div);
        });
    });
