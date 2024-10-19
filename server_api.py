from flask import Flask, request, jsonify
import asyncpg
from app import db_commands
app = Flask(__name__)



@app.route('/get-user-points', methods=['GET'])
async def get_user_points():
    user_id = request.args.get('user_id')
    response = await db_commands.get_user_points(user_id)
    if response is None:
        return jsonify({'points': 0})
    else:
        return jsonify({'points': response})

# Сохранение очков пользователя при закрытии страницы
@app.route('/save-points', methods=['POST'])
async def save_points():
    data = request.json
    user_id = data['user_id']
    points = data['points']

    response_update_points = await db_commands.update_user_points_points(user_id, points)
    
    return jsonify({'status': 'success'})

if __name__ == "__main__":
    app.run(debug=True)