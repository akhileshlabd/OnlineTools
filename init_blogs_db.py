import sqlite3

def init_db():
    conn = sqlite3.connect('blogs.db')
    c = conn.cursor()
    # Drop existing to apply new schema with images and comments
    c.execute('DROP TABLE IF EXISTS blogs')
    c.execute('DROP TABLE IF EXISTS comments')
    
    c.execute('''
        CREATE TABLE blogs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            slug TEXT UNIQUE NOT NULL,
            content TEXT NOT NULL,
            image_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    c.execute('''
        CREATE TABLE comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            blog_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(blog_id) REFERENCES blogs(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("blogs.db recreated with image support and comments!")

if __name__ == '__main__':
    init_db()
