with open('routes/admin.py', 'r') as f:
    content = f.read()

make_slug_fn = """
def make_slug(title):
    import re
    return re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')

def get_db_connection():
"""

content = content.replace("def get_db_connection():", make_slug_fn)

with open('routes/admin.py', 'w') as f:
    f.write(content)
