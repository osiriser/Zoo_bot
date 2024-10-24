// Функция для выполнения задачи
function completeTask(taskId) {
    fetch(`/api/complete-task`, {
        method: 'POST',
        body: JSON.stringify({ user_id: userId, task_id: taskId }),
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Обновляем состояние кнопки и ссылки
            const taskButton = document.getElementById(taskId);
            taskButton.classList.add('completed');
            taskButton.querySelector('a').style.pointerEvents = 'none'; // Делаем ссылку неактивной
        }
    })
    .catch(error => console.error('Ошибка выполнения задачи:', error));
}
