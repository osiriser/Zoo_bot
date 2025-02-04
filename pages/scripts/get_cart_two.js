window.onload = async function () {
    try {
        const userIdElement = document.getElementById('user_id');
        if (!userIdElement || !userIdElement.value) {
            console.error("User ID is not set or element not found.");
            return;
        }

        const userId = userIdElement.value;

        // Отправляем запрос к API
        const response = await fetch(`/api/cart/${userId}`);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        // Получаем данные корзины
        const cartItems = await response.json();

        // Рассчитываем сумму заказа
        let totalAmount = 0;
        cartItems.forEach(item => {
            totalAmount += item.product_price * item.quantity;
        });

        // Рассчитываем комиссию (10%)
        const commission = (totalAmount * 0.1).toFixed(2);
        const total = (totalAmount + parseFloat(commission)).toFixed(2);

        // Обновляем элементы в DOM
        document.getElementById('amount').textContent = `${totalAmount.toFixed(2)}$`;
        document.getElementById('commission').textContent = `${commission}$`;
        document.getElementById('total-price').textContent = `${total}$`;
    } catch (error) {
        console.error('Ошибка загрузки корзины:', error);
    }
};

// Сохранение данных
async function SendOrder() {
    const saveButton = document.getElementById('save-button');
    if (!saveButton) return;

    const formData = new FormData();
    formData.append('user_id', document.getElementById('user_id')?.value || '');
    formData.append('contact_name', document.getElementById('contact-name')?.value || '');
    formData.append('mobile_number', document.getElementById('mobile-number')?.value || '');
    formData.append('street', document.getElementById('street')?.value || '');
    formData.append('country', document.getElementById('country')?.value || '');
    formData.append('region', document.getElementById('region')?.value || '');
    formData.append('zip_code', document.getElementById('zip-code')?.value || '');
    formData.append('extra_info', document.getElementById('extra-info')?.value || '');

    // Проверяем обязательные поля
    if (!formData.get('user_id') || !formData.get('mobile_number')) {
        console.error('Обязательные поля user_id или mobile_number отсутствуют');
        alert('Заполните все обязательные поля.');
        return;
    }
    console.log('Данные для отправки:', Object.fromEntries(formData.entries()));
    try {
        const response = await fetch('/api/place_order', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
        }

        const result = await response.json();

        if (result.success) {
            alert(`Заказ успешно создан! ID заказа: ${result.order_id}`);
        } else {
            console.error('Ошибка на сервере:', result.message);
            alert(`Ошибка: ${result.message}`);
        }
    } catch (error) {
        console.error('Ошибка при создании заказа:', error);
        alert('Не удалось создать заказ. Попробуйте ещё раз.');
    }
}


async function Checkout() {
    const response = await fetch('/api/create-checkout-session', {
        method: 'POST',
    });
    const session = await response.json();
    const stripe = Stripe('pk_test_51QZYAAP46aFviiNTQ3XEZn3zbOJ8bxofkBdACeSqGloVNMeBxBweI3teojajRcfAYpFdGoIoqjuokKLI4BOJ5wND002S8LTy1e');
    const { error } = await stripe.redirectToCheckout({
        sessionId: session.id,
    });
    if (error) {
        console.error('Ошибка перенаправления на Checkout:', error);
    }
};
