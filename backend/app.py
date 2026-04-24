from flask import Flask, request, jsonify
import pymysql
import os

app = Flask(__name__)

# DB connection
def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

# Health check (VERY IMPORTANT for debugging)
@app.route('/health')
def health():
    return jsonify({"status": "ok"})

# GET all items
@app.route('/api/items', methods=['GET'])
def get_items():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM item")
        data = cursor.fetchall()
        conn.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# CREATE item
@app.route('/api/items', methods=['POST'])
def create_item():
    try:
        data = request.json
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO item (name) VALUES (%s)", (data['name'],))
        conn.close()
        return jsonify({"message": "created"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# DELETE item
@app.route('/api/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM item WHERE id=%s", (id,))
        conn.close()
        return jsonify({"message": "deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# START SERVER
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
