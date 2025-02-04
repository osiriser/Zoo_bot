async function addProductCart() {
    const productData = JSON.parse(localStorage.getItem('productData'));
    
    // Проверяем, что данные есть
    if (!productData) {
        alert("Данные о продукте не найдены в localStorage.");
        return;
    }

    const productId = productData?.id;
    const productImage = productData?.image_path;
    const productName = document.getElementById('product-title')?.textContent;
    const userId = document.getElementById('user_id')?.value;
    const productPrice = productData?.price;
    const quantity = 1;

    // Логгируем для отладки
    console.log("Отправляемые данные:", {
        productId, productName, productImage, userId, productPrice, quantity
    });

    const formData = new FormData();
    formData.append("product_id", productId);
    formData.append("product_name", productName);
    formData.append("product_image", productImage);
    formData.append("user_id", userId);
    formData.append("product_price", productPrice);
    formData.append("quantity", quantity);

    try {
        const response = await fetch("https://appminimall.xyz/api/add-to-cart", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Ошибка сервера: ${response.status}`);
        }

        const result = await response.json();
        if (result.success) {
            alert("Товар успешно добавлен в корзину!");
        } else {
            alert("Ошибка при добавлении товара: " + result.message);
        }
    } catch (error) {
        console.error("Ошибка при отправке данных:", error);
        alert("Не удалось отправить данные на сервер.");
    }
}
