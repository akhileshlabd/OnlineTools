import sqlite3

def migrate():
    conn = sqlite3.connect('blogs.db')
    c = conn.cursor()
    
    # 1. Add comments_enabled to blogs table
    try:
        c.execute('ALTER TABLE blogs ADD COLUMN comments_enabled INTEGER DEFAULT 1')
        print("Added comments_enabled column to blogs table.")
    except sqlite3.OperationalError:
        print("Column comments_enabled already exists.")
        
    # 2. Create settings table for the global master switch
    c.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    ''')
    
    # Insert default global switch if not exists
    c.execute('INSERT OR IGNORE INTO settings (key, value) VALUES ("global_comments_enabled", "1")')
    
    conn.commit()
    conn.close()
    print("Migration complete!")

if __name__ == '__main__':
    migrate()
