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
                // taskButton.querySelector('a').style.pointerEvents = 'none';
                taskButton.style.pointerEvents = 'none';
            }
        });
    })
    .catch(error => console.error('Ошибка загрузки состояния задач:', error));
};