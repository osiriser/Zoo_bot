function handleItemClick(type, id) {
    if (type === "product") {
        // Загружаем данные товара
        fetch(<code>/api/products/${id}</code>)
            .then(response => response.json())
            .then(product => {
                if (!product.error) {
                    // Перенаправление на страницу товара с данными
                    localStorage.setItem('productData', JSON.stringify(product));  // Сохраняем данные о продукте
                    window.location.href = 'flow_card.html';
                } else {
                    alert(product.error);
                }
            })
            .catch(error => console.error('Error fetching product:', error));
    } else if (type === "subcategory") {
        fetch(<code>/api/products?subcategory_id=${id}</code>)
            .then(response => response.json())
            .then(products => {
                displayItems(products, "product");
            });
    }
}