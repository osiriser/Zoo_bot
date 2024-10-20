let points = 0;
let savedPoints = 0; // Очки, которые были подгружены из базы данных
let userId = document.getElementById('user_id').value; // Предположим, что user_id передан в HTML

// Функция для подгрузки очков из базы данных при загрузке страницы
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

// Обработчик кликов для увеличения очков
document.getElementById("bird").addEventListener("click", function() {
    points += 1;
    document.getElementById("points").innerText = points;
});

// Отправляем очки на сервер только при закрытии страницы
window.addEventListener("beforeunload", function() {
    if (points !== savedPoints) {
        const data = new URLSearchParams({
            user_id: userId,
            points: points
        });
        console.log('Sending points:', data.toString());
        navigator.sendBeacon("/api/save-points", data);
    }
});
