from fastapi import FastAPI, Request
import asyncpg
from aiogram import Bot

app = FastAPI()

async def connect():
    return await asyncpg.connect(database="users",
                                 user="postgres",
                                 host="localhost",
                                 password="kuroishi31!",
                                 port=5432)

@app.post("/update_user_info")
async def update_user_info(request: Request):
    print(f"Received data: {data}")
    data = await request.json()
    user_id = data.get("userId")
    contact_name = data.get("contactName")
    mobile_number = data.get("mobileNumber")
    street_house = data.get("streetHouse")
    country = data.get("country")
    region = data.get("region")
    zip_code = data.get("zipCode")
    extra_info = data.get("extraInfo")


    conn = await connect()
    try:
        # Обновляем данные пользователя в базе данных
        await conn.execute("""
            UPDATE users
            SET contact_name = $1, mobile_number = $2, street_house = $3, 
                country = $4, region = $5, zip_code = $6, extra_info = $7
            WHERE tg_user_id = $8;
        """, contact_name, mobile_number, street_house, country, region, zip_code, extra_info, user_id)

        return {"success": True}
    except Exception as e:
        print(f"Ошибка: {e}")
        return {"success": False, "error": str(e)}
    finally:
        await conn.close()

# Запуск Uvicorn сервера
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8340)
