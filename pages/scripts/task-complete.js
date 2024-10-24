// Функция для выполнения задачи
function completeTask(taskId) {
    if (points !== savedPoints) {
        const data = new URLSearchParams({
            user_id: userId,
            task_id: taskId
        });
        console.log('Sending task_id:', data.toString());
        navigator.sendBeacon("/api/complete-task", data);
    
    
    if (data.status === 'success') {
            // Обновляем состояние кнопки и ссылки
        const taskButton = document.getElementById(taskId);
        taskButton.classList.add('completed');
        taskButton.querySelector('a').style.pointerEvents = 'none'; // Делаем ссылку неактивной
        }
    }
    
}
