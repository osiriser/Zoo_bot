
window.onload = function() {
    fetch(`/api/get-user-points?user_id=${userId}`)
        .then(response => response.json())
        .then(data => {
            points = data.points; // Инициализируем очки из базы данных
            savedPoints = points;
            document.getElementById("points").innerText = points;
        })
        .catch(error => console.error('Ошибка загрузки данных:', error));
};