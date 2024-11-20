document.getElementById("add-to-cart").addEventListener("click", function() {
    const productData = JSON.parse(localStorage.getItem('productData'));
    console.log("Product Data from localStorage:", productData);
    
    const productId = productData?.id;
    const productImage = productData?.image_path;
    const productName = document.getElementById('product-title')?.textContent;
    const userId = document.getElementById('user_id')?.value;
    const productPrice = productData?.price;
    const quantity = 1;

    // Log values for debugging
    console.log("Product ID:", productId);
    console.log("Product Image:", productImage);
    console.log("Product Name:", productName);
    console.log("User ID:", userId);
    console.log("Product Price:", productPrice);

    // const data = new URLSearchParams({
    //     product_id: productId,
    //     product_name: productName,
    //     product_image: productImage,
    //     user_id: userId,
    //     product_price: productPrice,
    //     quantity: quantity
    //     });
    const data = {
        product_id: productId,
        product_name: productName,
        product_image: productImage,
        user_id: userId,
        product_price: productPrice,
        quantity: quantity
    };

    fetch(`https://appminimall.xyz/api/add-to-cart`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data) // Преобразуйте объект `data` в JSON
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json(); // Попробуйте разобрать JSON только после проверки статуса
    })
    .then(jsondata => {
        if (jsondata.success) {
            console.log("Товар успешно добавлен в корзину");
        } else {
            console.log("Не удалось добавить товар в корзину:", jsondata);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
    
})
