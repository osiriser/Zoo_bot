let userId = document.getElementById('user_id').value;

window.onload = function() {
    fetch(`/api/get-tasks-status?user_id=${userId}`)
    .then(response => response.json())
    .then(data => {
        // Проходим по всем задачам и обновляем кнопки
        Object.keys(data).forEach(taskId => {
            if (data[taskId] === true) {
                const taskButton = document.getElementById(taskId);
                taskButton.classList.add('completed');
                taskButton.querySelector('a').style.pointerEvents = 'none';
                taskButton.disabled = true;
            }
        });
    })
    .catch(error => console.error('Ошибка загрузки состояния задач:', error));
};



let points = 0;
let savedPoints = 0; // Очки, которые были подгружены из базы данных


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