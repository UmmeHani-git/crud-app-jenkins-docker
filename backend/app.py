from flask import Flask, request, jsonify
import pymysql
import os

app = Flask(__name__)

def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

# -----------------------------
# HEALTH CHECK
# -----------------------------
@app.route('/health')
def health():
    return jsonify({"status": "ok"})

# -----------------------------
# GET ALL ITEMS
# -----------------------------
@app.route('/api/items', methods=['GET'])
def get_items():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items")
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

# -----------------------------
# CREATE ITEM
# -----------------------------
@app.route('/api/items', methods=['POST'])
def create_item():
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name) VALUES (%s)", (data['name'],))
    conn.close()
    return jsonify({"message": "created"})

# -----------------------------
# UPDATE ITEM
# -----------------------------
@app.route('/api/items/<int:id>', methods=['PUT'])
def update_item(id):
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET name=%s WHERE id=%s", (data['name'], id))
    conn.close()
    return jsonify({"message": "updated"})

# -----------------------------
# DELETE ITEM
# -----------------------------
@app.route('/api/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id=%s", (id,))
    conn.close()
    return jsonify({"message": "deleted"})

# -----------------------------
# STATS
# -----------------------------
@app.route('/api/stats', methods=['GET'])
def get_stats():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as total FROM items")
    result = cursor.fetchone()
    conn.close()
    return jsonify(result)

# -----------------------------
# RUN APP
# -----------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
