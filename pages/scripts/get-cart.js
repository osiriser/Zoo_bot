window.onload = async function () {
    try {
        const userId = document.getElementById('user_id').value;

        if (!userId) {
            console.error("User ID is not set.");
            return;
        }

        // Отправляем запрос к API
        const response = await fetch(`/api/cart/${userId}`);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const cartItems = await response.json();
        const cartContainer = document.getElementById('cart-items');
        let totalAmount = 0;
        localStorage.setItem('cart', JSON.stringify(cartItems));
        // Очищаем контейнер перед добавлением данных
        cartContainer.innerHTML = '';
        const basePath = '../icons/';
        cartItems.forEach(item => {
            // Создаем отдельный элемент для каждого товара
            const productElement = document.createElement('div');
            productElement.classList.add('row-order');
            productElement.id = `product-${item.product_id}`;

            const productPath = basePath + item.product_image.split('/').pop();

            // Динамическая HTML-разметка
            productElement.innerHTML = `
                <button class="delete-btn" onclick="deleteProduct('${item.product_id}', '${userId}')">×</button>
                <img src="${productPath}" class="img-cont">
                <div class="inf-col-order">
                    <div class="name-text">${item.product_name}</div>
                    <div class="sum-row">
                        <span style="font-size: 20px;">Amount</span>
                        <span style="font-size: 20px;" id="amount-${item.product_id}">
                            ${(item.quantity * item.product_price).toFixed(2)}$
                        </span>
                    </div>
                    <div class="sum-row">
                        <span style="font-size: 20px;">Quantity</span>
                        <span style="font-size: 20px;" id="quantity-${item.product_id}">
                            ${item.quantity}
                        </span>
                        <button style="font-size: 20px;" onclick="decreaseFunc('${item.product_id}', '${userId}')">-</button>
                        <button style="font-size: 20px;" onclick="increaseFunc('${item.product_id}', '${userId}')">+</button>
                    </div>
                </div>
            `;
            cartContainer.appendChild(productElement); // Добавляем в DOM

            totalAmount += item.product_price * item.quantity; // Считаем итоговую сумму
        });

        // Рассчитываем суммы
        const commission = (totalAmount * 0.1).toFixed(2); // 10% комиссия
        const total = (totalAmount + parseFloat(commission)).toFixed(2);

        // Обновляем итоговые значения
        document.getElementById('amount').textContent = `${totalAmount.toFixed(2)}$`;
        document.getElementById('commission').textContent = `${commission}$`;
        document.getElementById('total').textContent = `${total}$`;

    } catch (error) {
        console.error('Ошибка загрузки корзины:', error);
    }
};



async function updateQuantityOnServer(productId, userId, action) {
    const formData = new FormData();
    formData.append("product_id", productId);
    formData.append("user_id", userId);
    formData.append("action", action);

    try {
        const response = await fetch("https://appminimall.xyz/api/update-cart", {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            throw new Error(`Ошибка на сервере: ${response.status}`);
        }

        const result = await response.json();
        if (result.success) {
            // Обновляем количество и сумму для конкретного продукта
            const quantityElement = document.getElementById(`quantity-${productId}`);
            const amountElement = document.getElementById(`amount-${productId}`);

            const newQuantity = result.new_quantity;
            const productPrice = result.product_price; // предполагается, что сервер возвращает цену товара

            quantityElement.textContent = newQuantity;
            amountElement.textContent = `${(newQuantity * productPrice).toFixed(2)}$`;

            // Перезагружаем корзину для обновления общих итогов
            window.onload();
        } else {
            alert("Ошибка при обновлении корзины: " + result.message);
        }
    } catch (error) {
        console.error("Ошибка при обновлении количества:", error);
        alert("Не удалось обновить количество товара.");
    }
}

function decreaseFunc(productId, userId) {
    updateQuantityOnServer(productId, userId, "decrease");
}

function increaseFunc(productId, userId) {
    updateQuantityOnServer(productId, userId, "increase");
}



async function deleteProduct(productId, userId) {
    try {
        const formData = new FormData();
        formData.append("product_id", productId);
        formData.append("user_id", userId);

        const response = await fetch("https://appminimall.xyz/api/delete-cart-item", {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            throw new Error(`Ошибка на сервере: ${response.status}`);
        }

        const result = await response.json();
        if (result.success) {
            // Удаляем HTML-элемент из DOM
            const productElement = document.getElementById(`product-${productId}`);
            if (productElement) {
                productElement.remove(); // Удаление из DOM
            }

            // Обновляем итоговые суммы
            updateTotalAmounts();
        } else {
            alert("Ошибка при удалении товара из корзины: " + result.message);
        }
    } catch (error) {
        console.error("Ошибка при удалении товара:", error);
        alert("Не удалось удалить товар из корзины.");
    }
}




function updateTotalAmounts() {
    const amountElements = document.querySelectorAll('[id^="amount-"]');
    let totalAmount = 0;

    amountElements.forEach((element) => {
        totalAmount += parseFloat(element.textContent.replace('$', ''));
    });

    const commission = (totalAmount * 0.1).toFixed(2); // 10% комиссия
    const total = (totalAmount + parseFloat(commission)).toFixed(2);

    document.getElementById('amount').textContent = `${totalAmount.toFixed(2)}$`;
    document.getElementById('commission').textContent = `${commission}$`;
    document.getElementById('total').textContent = `${total}$`;
}
