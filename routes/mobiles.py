import sqlite3
from flask import Blueprint, render_template, request, jsonify

mobiles_bp = Blueprint('mobiles', __name__, url_prefix='/mobiles')

def get_db_connection():
    conn = sqlite3.connect('mobiles.db')
    conn.row_factory = sqlite3.Row
    return conn

@mobiles_bp.route('/compare-phones', methods=['GET'])
def compare_phones():
    return render_template('compare_phones.html')

@mobiles_bp.route('/api/search', methods=['GET'])
def api_search():
    q = request.args.get('q', '').strip()
    if not q:
        return jsonify([])
        
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT id, brand, model FROM phones WHERE model LIKE ? OR brand LIKE ? LIMIT 10", (f'%{q}%', f'%{q}%'))
    results = c.fetchall()
    conn.close()
    
    return jsonify([dict(row) for row in results])

@mobiles_bp.route('/api/phone/<int:phone_id>', methods=['GET'])
def api_get_phone(phone_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM phones WHERE id = ?", (phone_id,))
    phone = c.fetchone()
    conn.close()
    
    if phone:
        return jsonify(dict(phone))
    return jsonify({"error": "Not found"}), 404
