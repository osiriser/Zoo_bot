// Функция для выполнения задачи
function completeTask(taskId, url) {
    
    const data = new URLSearchParams({
        user_id: userId,
        task_id: taskId
        });
    console.log('Sending task_id:', data.toString());
    navigator.sendBeacon("/api/complete-task", data);
    
    
    const taskButton = document.getElementById(taskId);
    taskButton.classList.add('completed');
    // taskButton.querySelector('a').style.pointerEvents = 'none';
    taskButton.style.pointerEvents = 'none';
    window.open(url, '_blank');
    }
    
