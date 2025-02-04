async function changeQuantity(productId, change) {
    const quantityElement = document.getElementById(`quantity-${productId}`);
    let currentQuantity = parseInt(quantityElement.textContent);

    // Изменяем количество
    currentQuantity += change;
    if (currentQuantity < 1) currentQuantity = 1; // Минимум 1

    // Обновляем количество на клиенте
    quantityElement.textContent = currentQuantity;

    // Отправляем обновленное количество на сервер
    const userId = document.getElementById('user_id').value;
    try {
        const response = await fetch(`/api/cart/${userId}/update`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                product_id: productId,
                quantity: currentQuantity
            })
        });

        if (!response.ok) {
            throw new Error(`Ошибка при обновлении количества: ${response.status}`);
        }

        // Перезагружаем корзину для обновления данных
        window.onload();
    } catch (error) {
        console.error('Ошибка при обновлении количества товара:', error);
    }
}