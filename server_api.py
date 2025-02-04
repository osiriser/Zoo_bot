from flask import Flask, request, jsonify, render_template, session
from app import db_site
app = Flask(__name__)

import stripe

@app.route('/api/get-user-points', methods=['GET'])
def get_user_points():
    user_id = request.args.get('user_id')
    response = db_site.get_user_points(int(user_id))
    if response is None:
        return jsonify({'points': 0})
    else:
        return jsonify({'points': response})

# Сохранение очков пользователя при закрытии страницы
@app.route('/api/save-points', methods=['POST'])
def save_points():
    #data = request.json
    #user_id = data['user_id']
    #points = data['points']

    user_id = request.form.get('user_id')
    points = request.form.get('points')

    print(f"Received user_id: {user_id}, points: {points}")

    if not user_id or not points:
        return jsonify({'status': 'error', 'message': 'Missing data'}), 400
    response_update_points = db_site.update_user_points(int(user_id), int(points))
    
    return jsonify({'status': 'success'})

@app.route('/api/complete-task', methods=['POST'])
def complete_task():
    user_id = request.form.get('user_id')
    task_id = request.form.get('task_id')
    print(f"Received user_id: {user_id}, task_id: {task_id}")
    if not user_id or not task_id:
        return jsonify({'status': 'error', 'message': 'Missing data'}), 400

    # Обновление задачи в базе данных
    response_update_task = db_site.complete_task(int(user_id), task_id)

    return jsonify({'status': 'success'})

@app.route('/api/get-tasks-status', methods=['GET'])
def get_tasks_status():
    user_id = request.args.get('user_id')
    tasks_status = db_site.get_tasks_status(int(user_id))
    return jsonify(tasks_status)


@app.route('/api/categories')
def get_categories():
    categories = db_site.get_categories()
    print(categories) 
    return jsonify(categories)

# Маршрут для получения подкатегорий
@app.route('/api/subcategories')
def get_subcategories():
    category_id = request.args.get('category_id')
    subcategories = db_site.get_subcategories(int(category_id))
    return jsonify(subcategories)

# Маршрут для получения товаров
@app.route('/api/products')
def get_products():
    subcategory_id = request.args.get('subcategory_id')
    products = db_site.get_products(subcategory_id)
    return jsonify(products)

@app.route('/api/products/<int:product_id>', methods=['GET'])
def fetch_product(product_id):
    product = db_site.get_product(product_id)
    if product:
        return jsonify(product), 200
    return jsonify({"error": "Product not found"}), 404

@app.route('/api/add-to-cart', methods=['POST'])
def add_to_cart_func():
    try:
        # Извлекаем данные из формы
        user_id = request.form.get('user_id')
        product_id = request.form.get('product_id')
        product_name = request.form.get('product_name')
        product_image = request.form.get('product_image')
        product_price = request.form.get('product_price')
        quantity = request.form.get('quantity')

        # Проверка на заполненность полей
        if not all([user_id, product_id, product_name, product_image, product_price, quantity]):
            return jsonify({'success': False, 'message': 'Некоторые данные отсутствуют'}), 400

        # Добавляем в базу
        db_site.add_product_cart(
            int(user_id),
            product_id,
            product_name,
            product_image,
            float(product_price),  # Приводим цену к float
            int(quantity)          # Приводим количество к int
        )
        return jsonify({'success': True, 'message': 'Товар добавлен в корзину'}), 200

    except Exception as e:
        print("Ошибка базы данных:", e)  # Логгируем для отладки
        return jsonify({'success': False, 'message': f'Ошибка базы данных: {e}'}), 500
    print("Данные для добавления в корзину:", {
        "user_id": user_id,
        "product_id": product_id,
        "product_name": product_name,
        "product_image": product_image,
        "product_price": product_price,
        "quantity": quantity
    })

@app.route('/api/cart/<int:user_id>', methods=['GET'])
def get_user_cart(user_id):
    try:
        # Получаем данные корзины из базы
        cart_items = db_site.get_user_cart(user_id)
        if not cart_items:
            return jsonify({"error": "Cart is empty"}), 404

        # Формируем JSON ответ
        response = [
            {
                "product_id": item[0],
                "product_name": item[1],
                "product_image": item[2],
                "product_price": item[3],
                "quantity": item[4],
            }
            for item in cart_items
        ]
        return jsonify(response), 200

    except Exception as e:
        print(f"Error fetching cart for user {user_id}: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/update-cart', methods=['POST'])
def update_cart():
    product_id = request.form.get('product_id')
    user_id = request.form.get('user_id')
    action = request.form.get('action')  # "increase" или "decrease"

    if not product_id or not user_id or not action:
        return jsonify({'success': False, 'message': 'Missing parameters'}), 400

    try:
        if action == "increase":
            db_site.increase_quantity(user_id, product_id)
        elif action == "decrease":
            db_site.decrease_quantity(user_id, product_id)
        else:
            return jsonify({'success': False, 'message': 'Invalid action'}), 400

        # Получаем новое количество для ответа
        new_quantity = db_site.get_quantity(user_id, product_id)
        return jsonify({'success': True, 'new_quantity': new_quantity}), 200
    except Exception as e:
        print("Error updating cart:", e)
        return jsonify({'success': False, 'message': 'Database error occurred'}), 500


@app.route('/api/delete-cart-item', methods=['POST'])
def delete_cart_item():
    product_id = request.form.get('product_id')
    user_id = request.form.get('user_id')

    if not product_id or not user_id:
        return jsonify({"success": False, "message": "Product ID or User ID is missing."}), 400

    try:
        db_site.delete_item_cart(user_id, product_id)
        return jsonify({"success": True, "message": "Product removed from cart."})
    except Exception as e:
        print(f"Ошибка удаления товара: {e}")
        return jsonify({"success": False, "message": "Failed to remove product."}), 500






@app.route('/api/place_order', methods=['POST'])
def place_order():
    try:
        # Извлекаем данные из формы
        print("Полученные данные:", request.form)
        user_id = request.form.get('user_id')
        contact_name = request.form.get('contact_name')
        mobile_number = request.form.get('mobile_number')
        street = request.form.get('street')
        country = request.form.get('country')
        region = request.form.get('region')
        zip_code = request.form.get('zip_code')
        extra_info = request.form.get('extra_info', "")

        # Проверяем обязательные поля
        if not user_id or not mobile_number:
            return jsonify({"success": False, "message": "Обязательные поля отсутствуют"}), 401

        # Получаем данные корзины
        cart_items = db_site.get_user_cart(user_id)
        print(cart_items)
        if not cart_items:
            return jsonify({"success": False, "message": "Корзина пуста"}), 402

        # Рассчитываем сумму и комиссию
        total_amount = sum(item['product_price'] * item['quantity'] for item in cart_items)
        commission = round(total_amount * 0.1, 2)
        total = total_amount + commission

        # Сохраняем информацию о пользователе
        save_user_info(user_id, mobile_number, street, country, region, zip_code, extra_info)

        # Создаем заказ
        order_id = create_order(
            user_id=int(user_id),
            contact_name=contact_name,
            mobile_number=mobile_number,
            street=street,
            country=country,
            region=region,
            zip_code=zip_code,
            extra_info=extra_info,
            total=total
        )

        # Добавляем товары в заказ
        add_order_items(order_id, cart_items)

        return jsonify({"success": True, "order_id": order_id})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500



stripe.api_key = 'sk_test_51QZYAAP46aFviiNTmo0MpIzjs6BlyAC040PuIqgHokMxUQ4XYHIMuzeQPdrwO3xJTB3pAKXGGFDeBQUlAvCcteUK00b2A8VkdC'

@app.route('/api/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Название товара',
                    },
                    'unit_amount': 2000,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://appminimall.xyz/pages/success.html',
            cancel_url='https://appminimall.xyz/pages/cancel.html',
        )
        return jsonify(id=session.id)
    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == "__main__":
    app.run(debug=True)