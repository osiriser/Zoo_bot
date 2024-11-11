document.addEventListener("DOMContentLoaded", () => {
    // Retrieve the product data from localStorage
    const productData = JSON.parse(localStorage.getItem('productData'));

    if (productData) {
        const productId = productData.id;  // Assuming the product ID is stored in `productData.id`
        console.log("Product ID:", productId);

        // Set up the "Add to Cart" button
        const addToCartButton = document.querySelector('.add-to-cart-button');
        addToCartButton.addEventListener('click', () => {
            addToCart(productId, productData.name, productData.image, 1);
        });

        // Display the product details on the page
        document.getElementById('product-title').textContent = productData.name;
        document.getElementById('product-price').textContent = productData.price;
        document.getElementById('product-description').textContent = productData.description;
    } else {
        alert("Product data not found!");
    }
});


function addToCart(productId, productName, productImage, quantity) {
    fetch('/api/add-to-cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            user_id: 1, // Replace with the actual user ID in your app
            product_id: productId,
            product_name: productName,
            product_image: productImage,
            quantity: quantity
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Product added to cart successfully!");
        } else {
            alert("Error adding product to cart: " + data.error);
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred while adding the product to the cart.");
    });
}










document.querySelector('.add-to-cart-button').addEventListener('click', () => {
    const productData = JSON.parse(localStorage.getItem('productData'));
    const productId = productData.id;
    const productImage = productData.image;
    const productName = document.getElementById('product-title').textContent;
    const userId = document.getElementById('user_id').textContent;
    const productPrice = productData.price;
      // Replace with the actual user ID from your session or state management
    const quantity = 1;  // Assuming a default quantity of 1 for now

    fetch('/api/add-to-cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            product_id: productId,
            product_name: productName,
            product_image: productImage,
            user_id: userId,
            product_price: productPrice,
            quantity: quantity
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Product added to cart!');
        } else {
            alert('Failed to add product to cart.');
        }
    })
    .catch(error => console.error('Error:', error));
});