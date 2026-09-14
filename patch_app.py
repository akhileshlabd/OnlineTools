import sys
import re

with open('app.py', 'r') as f:
    content = f.read()

# Add context processor for features
injection = """
import sqlite3
from collections import defaultdict

@app.context_processor
def inject_features():
    try:
        conn = sqlite3.connect('blogs.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT key, value FROM settings WHERE key LIKE 'feature_%'")
        rows = c.fetchall()
        conn.close()
        
        features = defaultdict(lambda: True)
        for r in rows:
            features[r['key']] = (r['value'] == '1')
        return dict(features=features)
    except:
        return dict(features=defaultdict(lambda: True))

"""

if 'def inject_features():' not in content:
    # insert before if __name__ == '__main__':
    content = content.replace("if __name__ == '__main__':", injection + "\nif __name__ == '__main__':")
    with open('app.py', 'w') as f:
        f.write(content)
    print("Patched app.py successfully.")
else:
    print("Already patched app.py")
