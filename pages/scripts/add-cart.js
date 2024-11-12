document.querySelector('add-to-cart-button').addEventListener('click', () => {
    const productData = JSON.parse(localStorage.getItem('productData'));
    const productId = productData.id;
    const productImage = productData.image;
    const productName = document.getElementById('product-title').textContent;
    const userId = document.getElementById('user_id').textContent;
    const productPrice = productData.price;
      // Replace with the actual user ID from your session or state management
    const quantity = 1;  // Assuming a default quantity of 1 for now

    const data = {
        product_id: productId,
        product_name: productName,
        product_image: productImage,
        user_id: userId,
        product_price: productPrice,
        quantity: quantity
    };

    fetch(`/api/add-to-cart`)
    //     , {
    //     method: 'POST',
    //     body: JSON.stringify(data) // Преобразуем объект в JSON
    // })
    // })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Product added to cart!');
        } else {
            alert('Failed to add product to cart.');
        }
    })})