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

    fetch('https://appminimall.xyz/api/add-to-cart', { method: 'post', body: data }).then(fetcheddata => {
    fetcheddata.json().then(jsondata => {
        if(jsondata.success) console.log("товар успешно добавлен в корзину");
    }
    )})
})
