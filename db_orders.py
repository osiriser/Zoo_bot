import asyncpg

async def create_table():
    conn = await asyncpg.connect(database="users",
                                 user="postgres",
                                 host="localhost",
                                 password="kuroishi31!",
                                 port=5432)


    await conn.execute("""
    DROP TABLE IF EXISTS orders;
    CREATE TABLE orders (
        order_id SERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL,
        total NUMERIC(10, 2) NOT NULL,
        payment_method VARCHAR(50) NOT NULL,
        status VARCHAR(20) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        contact_name VARCHAR(100) NOT NULL,
        mobile_number VARCHAR(15) NOT NULL,
        street_house VARCHAR(255) NOT NULL,
        country VARCHAR(100) NOT NULL,
        region VARCHAR(100) NOT NULL,
        zip_code VARCHAR(20) NOT NULL,
        extra_info TEXT
    );
""")

    await conn.execute("""
                       DROP TABLE IF EXISTS order_items;
                       CREATE TABLE order_items (
                        item_id SERIAL PRIMARY KEY,
                        order_id INT NOT NULL REFERENCES orders(order_id),
                        product_id INT NOT NULL,
                        quantity INT NOT NULL,
                        price NUMERIC(10, 2) NOT NULL
                        );             
                    """)

    await conn.close()

import asyncio
asyncio.run(create_table())