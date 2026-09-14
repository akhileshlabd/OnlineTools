import sqlite3

def migrate():
    conn = sqlite3.connect('blogs.db')
    c = conn.cursor()
    
    # 1. Add author_name to comments
    try:
        c.execute("ALTER TABLE comments ADD COLUMN author_name TEXT DEFAULT 'Anonymous'")
        print("Added author_name to comments.")
    except Exception as e:
        print("comments.author_name might already exist:", e)
        
    # 2. Add is_hidden to blogs
    try:
        c.execute("ALTER TABLE blogs ADD COLUMN is_hidden INTEGER DEFAULT 0")
        print("Added is_hidden to blogs.")
    except Exception as e:
        print("blogs.is_hidden might already exist:", e)

    conn.commit()
    conn.close()
    print("V2 Migration complete!")

if __name__ == '__main__':
    migrate()
