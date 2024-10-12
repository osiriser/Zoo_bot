window.Telegram.WebApp.ready();
document.getElementById('continue-button').addEventListener('click', async (e) => {
    e.preventDefault();
    console.log(window.Telegram.WebApp.initDataUnsafe.user.id);
            // Получаем данные из полей формы
    const userId = window.Telegram.WebApp.initDataUnsafe.user.id;
    const contactName = document.querySelector('input[placeholder="Contact Name*"]').value;
    const mobileNumber = document.querySelector('input[placeholder="Mobile number*"]').value;
    const streetHouse = document.querySelector('input[placeholder="Street, house/apartment/unit*"]').value;
    const country = document.querySelector('input[placeholder="Country*"]').value;
    const region = document.querySelector('input[placeholder="Region*"]').value;
    const zipCode = document.querySelector('input[placeholder="Zip code*"]').value;
    const extraInfo = document.querySelector('input[placeholder="Add free text if needed, eg: dont ring the doorbell, leave by the door, etc."]').value;
    
            // Собираем все данные в объект
    const userData = {
        userId: userId,
        contactName: contactName,
        mobileNumber: mobileNumber,
        streetHouse: streetHouse,
        country: country,
        region: region,
        zipCode: zipCode,
        extraInfo: extraInfo
    };
    console.log(userData);
        try {
                // Отправляем данные через fetch POST запрос
            const response = await fetch('http://100.42.176.212:8340/update_user_info', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });
    
        const result = await response.json();
        if (result.success) {
            alert('Данные успешно обновлены');
        } else {
            alert('Ошибка при обновлении данных');
        }
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка');
    }
});