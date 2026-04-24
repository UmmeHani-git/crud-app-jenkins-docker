from flask import Flask, request, jsonify
import pymysql
import os

app = Flask(name)

def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor
    )

# -----------------------------
# GET ALL ITEMS
# -----------------------------
@app.route('/items', methods=['GET'])
def get_items():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM item")
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

# -----------------------------
# CREATE ITEM
# -----------------------------
@app.route('/items', methods=['POST'])
def create_item():
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO item (name) VALUES (%s)", (data['name'],))
    conn.commit()
    conn.close()
    return jsonify({"message": "created"})

# -----------------------------
# UPDATE ITEM
# -----------------------------
@app.route('/items/<int:id>', methods=['PUT'])
def update_item(id):
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE item SET name=%s WHERE id=%s", (data['name'], id))
    conn.commit()
    conn.close()
    return jsonify({"message": "updated"})

# -----------------------------
# DELETE ITEM
# -----------------------------
@app.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM item WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "deleted"})

# -----------------------------
# STATS (COUNT)
# -----------------------------
@app.route('/stats', methods=['GET'])
def get_stats():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as total FROM item")
    result = cursor.fetchone()
    conn.close()
    return jsonify(result)

# -----------------------------
# RUN APP
# -----------------------------
if name == 'main':
    app.run(host='0.0.0.0', port=5000)
