from flask import Flask, request, jsonify, render_template, session
from app import db_commands
app = Flask(__name__)



@app.route('/api/get-user-points', methods=['GET'])
async def get_user_points():
    user_id = request.args.get('user_id')
    response = await db_commands.get_user_points(int(user_id))
    if response is None:
        return jsonify({'points': 0})
    else:
        return jsonify({'points': response})

# Сохранение очков пользователя при закрытии страницы
@app.route('/api/save-points', methods=['POST'])
async def save_points():
    #data = request.json
    #user_id = data['user_id']
    #points = data['points']

    user_id = request.form.get('user_id')
    points = request.form.get('points')

    print(f"Received user_id: {user_id}, points: {points}")

    if not user_id or not points:
        return jsonify({'status': 'error', 'message': 'Missing data'}), 400
    response_update_points = await db_commands.update_user_points(int(user_id), int(points))
    
    return jsonify({'status': 'success'})

@app.route('/api/complete-task', methods=['POST'])
async def complete_task():
    user_id = request.form.get('user_id')
    task_id = request.form.get('task_id')
    print(f"Received user_id: {user_id}, task_id: {task_id}")
    if not user_id or not task_id:
        return jsonify({'status': 'error', 'message': 'Missing data'}), 400

    # Обновление задачи в базе данных
    response_update_task = await db_commands.complete_task(int(user_id), task_id)

    return jsonify({'status': 'success'})

@app.route('/api/get-tasks-status', methods=['GET'])
async def get_tasks_status():
    user_id = request.args.get('user_id')
    tasks_status = await db_commands.get_tasks_status(int(user_id))
    return jsonify(tasks_status)


@app.route('/api/categories')
async def get_categories():
    categories = await db_commands.get_categories()
    print(categories) 
    return jsonify(categories)

# Маршрут для получения подкатегорий
@app.route('/api/subcategories')
async def get_subcategories():
    category_id = request.args.get('category_id')
    subcategories = await db_commands.get_subcategories(int(category_id))
    return jsonify(subcategories)

# Маршрут для получения товаров
@app.route('/api/products')
async def get_products():
    subcategory_id = request.args.get('subcategory_id')
    products = await db_commands.get_products(subcategory_id)
    return jsonify(products)

@app.route('/api/products/<int:product_id>', methods=['GET'])
async def fetch_product(product_id):
    product = await db_commands.get_product(product_id)
    if product:
        return jsonify(product), 200
    return jsonify({"error": "Product not found"}), 404

@app.route('/api/add-to-cart', methods=['POST'])
async def add_to_cart_func():
    data = request.json  # Используем JSON вместо form data
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    product_name = data.get('product_name')
    product_image = data.get('product_image')
    product_price = data.get('product_price')
    quantity = data.get('quantity', 1)  # Читаем quantity
    
    user_id = request.form.get('user_id')
    points = request.form.get('points')
    # Теперь вызываем вашу функцию для добавления товара в корзину
    try:
        await db_commands.add_product_cart(
            user_id, product_id, product_name, product_image, product_price, quantity
        )
        return jsonify({'success': True, 'message': 'Product added to cart'}), 200
    except Exception as e:
        print("Database Error:", e)  # Debugging
        return jsonify({'success': False, 'message': 'Database error occurred'}), 500

    

if __name__ == "__main__":
    app.run(debug=True)