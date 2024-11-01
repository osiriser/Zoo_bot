// Загружаем начальные категории при загрузке страницы
window.onload = function() {
    loadCategories();
};

// Функция для загрузки категорий
function loadCategories() {
    fetch("/api/categories")
        .then(response => response.json())
        .then(categories => {
            displayItems(categories, "category");
        });
}

// Функция для обработки кликов на категорию или подкатегорию
function handleItemClick(type, id) {
    if (type === "category") {
        fetch(`/api/subcategories?category_id=${id}`)
            .then(response => response.json())
            .then(subcategories => {
                displayItems(subcategories, "subcategory");
            });
    } else if (type === "subcategory") {
        fetch(`/api/products?subcategory_id=${id}`)
            .then(response => response.json())
            .then(products => {
                displayItems(products, "product");
            });
    }
}

// Отображение элементов (категорий, подкатегорий или товаров)
function displayItems(items, type) {
    const container = document.getElementById("category-container");
    container.innerHTML = ""; // Очистка контейнера

    items.forEach(item => {
        const itemDiv = document.createElement("div");
        itemDiv.className = "grid-item";
        itemDiv.onclick = () => handleItemClick(type, item.id);

        const img = document.createElement("img");
        img.src = item.image_path;
        img.alt = item.name;

        const title = document.createElement("p");
        title.textContent = item.name;

        itemDiv.appendChild(img);
        itemDiv.appendChild(title);
        container.appendChild(itemDiv);
    });
}
