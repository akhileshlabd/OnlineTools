import sqlite3
import re
from flask import Blueprint, render_template, request, jsonify, redirect, url_for

mobiles_bp = Blueprint('mobiles', __name__, url_prefix='/mobiles')

def get_db_connection():
    conn = sqlite3.connect('mobiles.db')
    conn.row_factory = sqlite3.Row
    return conn

def extract_num(val):
    if not val or val == '-': return None
    m = re.search(r'\d+(\.\d+)?', str(val))
    return float(m.group()) if m else None

def evaluate_winners(p1, p2):
    rules = {
        'price': False, 'screen_size': True, 'refresh_rate': True,
        'ram': True, 'storage': True, 'camera_main': True,
        'camera_selfie': True, 'battery': True, 'fast_charging': True,
        'weight': False
    }
    
    w1, w2 = {} , {}
    for key, higher_better in rules.items():
        v1, v2 = p1.get(key), p2.get(key)
        n1, n2 = extract_num(v1), extract_num(v2)
        if n1 is not None and n2 is not None:
            if n1 == n2:
                w1[key], w2[key] = True, True
            elif (n1 > n2 and higher_better) or (n1 < n2 and not higher_better):
                w1[key] = True
            else:
                w2[key] = True

    for key in ['network_5g', 'water_resistance']:
        v1, v2 = str(p1.get(key, '')).lower(), str(p2.get(key, '')).lower()
        if v1 == v2 and v1 and v1 != '-':
            w1[key], w2[key] = True, True
        elif key == 'water_resistance':
            n1, n2 = extract_num(v1), extract_num(v2)
            if n1 and n2:
                if n1 > n2: w1[key] = True
                elif n2 > n1: w2[key] = True

    return w1, w2

@mobiles_bp.route('/', methods=['GET'])
def index():
    # Fetch 4 popular phones to show on the hub page
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT brand, model, slug, image_url FROM phones LIMIT 4")
    popular_phones = [dict(row) for row in c.fetchall()]
    conn.close()
    return render_template('hub_mobiles.html', popular_phones=popular_phones)

@mobiles_bp.route('/compare', methods=['GET'])
@mobiles_bp.route('/compare-phones', methods=['GET']) # Legacy redirect or alias
def compare_phones_base():
    if request.path == '/mobiles/compare-phones':
        return redirect('/mobiles/compare', code=301)
    return render_template('compare_phones.html', p1=None, p2=None)

@mobiles_bp.route('/compare/<slug1>-vs-<slug2>', methods=['GET'])
def compare_phones_seo(slug1, slug2):
    if slug1 > slug2:
        return redirect(url_for('mobiles.compare_phones_seo', slug1=slug2, slug2=slug1), code=301)
        
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM phones WHERE slug = ?", (slug1,))
    p1 = c.fetchone()
    
    c.execute("SELECT * FROM phones WHERE slug = ?", (slug2,))
    p2 = c.fetchone()
    conn.close()
    
    if not p1 or not p2:
        return "One or both phones not found in database.", 404
        
    p1_dict, p2_dict = dict(p1), dict(p2)
    w1, w2 = evaluate_winners(p1_dict, p2_dict)
    
    return render_template('compare_phones.html', p1=p1_dict, p2=p2_dict, w1=w1, w2=w2)

@mobiles_bp.route('/api/search', methods=['GET'])
def api_search():
    q = request.args.get('q', '').strip()
    if not q:
        return jsonify([])
        
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT slug, brand, model FROM phones WHERE model LIKE ? OR brand LIKE ? LIMIT 10", (f'%{q}%', f'%{q}%'))
    results = c.fetchall()
    conn.close()
    
    return jsonify([dict(row) for row in results])
