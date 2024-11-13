document.querySelector('.add-to-cart-button').addEventListener('click', () => {
    const productData = JSON.parse(localStorage.getItem('productData'));
    const productId = productData.id;
    const productImage = productData.image;
    const productName = document.getElementById('product-title').textContent;
    const userId = document.getElementById('user_id').textContent;
    const productPrice = productData.price;
    const quantity = 1;  // Предполагается, что количество по умолчанию равно 1

    const data = {
        product_id: productId,
        product_name: productName,
        product_image: productImage,
        user_id: userId,
        product_price: productPrice,
        quantity: quantity
    };

    fetch('https://appminimall.xyz/api/add-to-cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        // Преобразуйте объект в строку JSON
        body: JSON.stringify(data)
    }).then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    }).then(jsondata => {
        if (jsondata.success) {
            console.log("товар успешно добавлен в корзину");
        } else {
            console.log("Не удалось добавить товар в корзину:", jsondata);
        }
    }).catch(error => {
        console.error('Ошибка:', error);
    });
});