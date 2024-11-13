document.querySelector('.add-to-cart-button').addEventListener('click', () => {
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

    fetch('https://appminimall.xyz/api/add-to-cart', { method: 'post', body: data }).then(fetcheddata => {
    fetcheddata.json().then(jsondata => {
        if(jsondata.success) console.log("товар успешно добавлен в корзину");
    }
    )})
})