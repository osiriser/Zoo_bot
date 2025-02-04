import psycopg2
from psycopg2.extras import DictCursor

# Функция для подключения к базе данных
def connect():
    return psycopg2.connect(
        database="users",
        user="postgres",
        host="localhost",
        password="kuroishi31!",
        port=5432
    )



# Получение очков пользователя
def get_user_points(telegram_id):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT number_points FROM users WHERE tg_user_id = %s", (telegram_id,))
            return cur.fetchone()[0]

# Обновление очков пользователя
def update_user_points(telegram_id, points):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE users SET number_points = %s WHERE tg_user_id = %s", (points, telegram_id))
            conn.commit()

# Завершение задания
def complete_task(telegram_id, task_id):
    with connect() as conn:
        with conn.cursor() as cur:
            query = f"UPDATE users SET {task_id} = TRUE WHERE tg_user_id = %s"
            cur.execute(query, (telegram_id,))
            cur.execute("""
                UPDATE users
                SET number_points = number_points + 1000
                WHERE tg_user_id = %s
            """, (telegram_id,))
            conn.commit()

# Получение статуса задач
def get_tasks_status(telegram_id):
    with connect() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            query = """
            SELECT task1, task2, task3, task4
            FROM users
            WHERE tg_user_id = %s
            """
            cur.execute(query, (telegram_id,))
            row = cur.fetchone()

            return {
                "task1": row['task1'],
                "task2": row['task2'],
                "task3": row['task3'],
                "task4": row['task4']
            }

# Получение категорий
def get_categories():
    with connect() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT id, name, image_path FROM categories")
            rows = cur.fetchall()
            return [{"id": row["id"], "name": row["name"], "image_path": row["image_path"]} for row in rows]

# Получение подкатегорий
def get_subcategories(category_id):
    with connect() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT id, name, image_path FROM subcategories WHERE category_id = %s", (category_id,))
            rows = cur.fetchall()
            return [{"id": row["id"], "name": row["name"], "image_path": row["image_path"]} for row in rows]

# Получение продуктов
def get_products(subcategory_id):
    with connect() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT id, name, image_path FROM products WHERE subcategory_id = %s", (subcategory_id,))
            rows = cur.fetchall()
            return [{"id": row["id"], "name": row["name"], "image_path": row["image_path"]} for row in rows]

# Добавление категории
def add_category(name, image_path):
    with connect() as conn:
        with conn.cursor() as cur:
            query = "INSERT INTO categories (name, image_path) VALUES (%s, %s)"
            cur.execute(query, (name, image_path))
            conn.commit()

# Добавление подкатегории
def add_subcategory(name, image_path, category_id):
    with connect() as conn:
        with conn.cursor() as cur:
            query = "INSERT INTO subcategories (name, image_path, category_id) VALUES (%s, %s, %s)"
            cur.execute(query, (name, image_path, category_id))
            conn.commit()

# Добавление продукта
def add_product(category_id, subcategory_id, waiting_for_name, price, image_path, image_path2, image_path3, description):
    with connect() as conn:
        with conn.cursor() as cur:
            query = """
                INSERT INTO products (name, image_path, image_path2, image_path3, price, description, category_id, subcategory_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(query, (waiting_for_name, image_path, image_path2, image_path3, price, description, category_id, subcategory_id))
            conn.commit()

# Получение информации о продукте
def get_product(product_id):
    with connect() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT id, name, image_path, image_path2, image_path3, description, price FROM products WHERE id = %s", (product_id,))
            row = cur.fetchone()

            if row:
                return {
                    "id": row["id"],
                    "name": row["name"],
                    "image_path": row["image_path"],
                    "image_path2": row["image_path2"],
                    "image_path3": row["image_path3"],
                    "description": row["description"],
                    "price": row["price"]
                }
            return None

# Добавление товара в корзину
def add_product_cart(user_id, product_id, product_name, product_image, product_price, quantity):
    with connect() as conn:
        with conn.cursor() as cur:
            # Проверка, есть ли товар в корзине
            cur.execute("""
                SELECT quantity FROM cart WHERE user_id = %s AND product_id = %s
            """, (user_id, product_id))
            existing_item = cur.fetchone()

            if existing_item:
                # Если товар есть, обновляем количество
                cur.execute("""
                    UPDATE cart
                    SET quantity = quantity + 1
                    WHERE user_id = %s AND product_id = %s
                """, (user_id, product_id))
            else:
                # Если товара нет, добавляем новую запись
                cur.execute("""
                    INSERT INTO cart (user_id, product_id, product_name, product_image, product_price, quantity)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (user_id, product_id, product_name, product_image, product_price, quantity))
            
            conn.commit()
            return True


def get_user_cart(user_id):
    with connect() as conn:
        with conn.cursor() as cur:
            query = """
            SELECT product_id, product_name, product_image, product_price, quantity 
            FROM cart 
            WHERE user_id = %s;
        """
            cur.execute(query, (user_id,))
            items = cur.fetchall()
            conn.commit()
            return items

def increase_quantity(user_id, product_id):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE cart
                SET quantity = quantity + 1
                WHERE user_id = %s AND product_id = %s
            """, (int(user_id), int(product_id)))
            conn.commit()

def decrease_quantity(user_id, product_id):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE cart
                SET quantity = GREATEST(quantity - 1, 0)  -- Уменьшаем до 0
                WHERE user_id = %s AND product_id = %s
            """, (int(user_id), int(product_id)))
            conn.commit()

def get_quantity(user_id, product_id):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT quantity FROM cart
                WHERE user_id = %s AND product_id = %s
            """, (int(user_id), int(product_id)))
            result = cur.fetchone()
            return result[0] if result else 0



def delete_item_cart(user_id, product_id):
    with connect() as conn:
        with conn.cursor() as cur:
            query = "DELETE FROM cart WHERE product_id = %s AND user_id = %s"
            cur.execute(query, (product_id, user_id))
        conn.commit()  # Ensure this line is indented correctly.


def submit_order_cart(contact_name, mobile_number, street_house, country, region, zip_code, extra_info):
    with connect() as conn: 
        with conn.cursor() as cur:
            cur = conn.cursor()

        # Вставка данных в таблицу
            query = """
            INSERT INTO orders (contact_name, mobile_number, street_house, country, region, zip_code, extra_info)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(query, (contact_name, mobile_number, street_house, country, region, zip_code, extra_info))
        conn.commit()



def add_order_items(order_id, cart_data):
    query = """
        INSERT INTO order_items (order_id, product_id, quantity, price)
        VALUES %s;
    """
    values = [(order_id, item['product_id'], item['quantity'], item['product_price']) for item in cart_data]
    with connect() as conn:
        with conn.cursor() as cur:
            execute_values(cur, query, values)
            conn.commit()

def create_order(user_id, total, payment_method, contact_info):
    query = """
        INSERT INTO orders (user_id, total, payment_method, status, created_at, contact_name, mobile_number, street_house, country, region, zip_code, extra_info)
        VALUES (%s, %s, %s, 'pending', %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING order_id;
    """
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (
                user_id, total, payment_method, datetime.now(),
                contact_info['contact_name'], contact_info['mobile_number'], contact_info['street_house'],
                contact_info['country'], contact_info['region'], contact_info['zip_code'], contact_info['extra_info']
            ))
            order_id = cur.fetchone()[0]
            conn.commit()
    return order_id


def save_user_info(user_id, mobile_number, street, country, region, zip_code, extra_info):
    """Сохранить или обновить информацию о пользователе."""
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (tg_user_id, mobile_number, street_house, country, region, zip_code, extra_info)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (tg_user_id) DO UPDATE 
            SET mobile_number = EXCLUDED.mobile_number,
                street_house = EXCLUDED.street_house,
                country = EXCLUDED.country,
                region = EXCLUDED.region,
                zip_code = EXCLUDED.zip_code,
                extra_info = EXCLUDED.extra_info;
        """, (user_id, mobile_number, street, country, region, zip_code, extra_info))
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def create_order(user_id, contact_name, mobile_number, street, country, region, zip_code, extra_info, payment_method, total):
    """Создать заказ и вернуть его ID."""
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO orders (user_id, total, payment_method, status, contact_name, mobile_number, street_house, country, region, zip_code, extra_info)
            VALUES (%s, %s, %s, 'Pending', %s, %s, %s, %s, %s, %s, %s)
            RETURNING order_id;
        """, (user_id, total, payment_method, contact_name, mobile_number, street, country, region, zip_code, extra_info))
        order_id = cursor.fetchone()[0]
        conn.commit()
        return order_id
    finally:
        cursor.close()
        conn.close()


def add_order_items(order_id, cart_items):
    """Добавить товары в заказ."""
    conn = connect()
    cursor = conn.cursor()
    try:
        for item in cart_items:
            cursor.execute("""
                INSERT INTO order_items (order_id, product_id, quantity, price)
                VALUES (%s, %s, %s, %s);
            """, (order_id, item['product_id'], item['quantity'], item['product_price']))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

