import sqlite3

def init_db():
    conn = sqlite3.connect('mobiles.db')
    c = conn.cursor()
    
    # Create table
    c.execute('''
        CREATE TABLE IF NOT EXISTS phones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT,
            model TEXT,
            image_url TEXT,
            display TEXT,
            processor TEXT,
            ram TEXT,
            storage TEXT,
            battery TEXT,
            camera_main TEXT,
            camera_selfie TEXT,
            os TEXT,
            price TEXT
        )
    ''')
    
    # Clear existing data for fresh seed
    c.execute('DELETE FROM phones')
    
    # Sample real-world data for the PoC
    phones = [
        ("Apple", "iPhone 15 Pro Max", "https://fdn2.gsmarena.com/vv/bigpic/apple-iphone-15-pro-max.jpg", "6.7 inch LTPO Super Retina XDR OLED, 120Hz", "Apple A17 Pro (3 nm)", "8GB", "256GB / 512GB / 1TB", "4441 mAh", "48 MP + 12 MP + 12 MP", "12 MP", "iOS 17", "$1,199"),
        ("Apple", "iPhone 15", "https://fdn2.gsmarena.com/vv/bigpic/apple-iphone-15.jpg", "6.1 inch Super Retina XDR OLED", "Apple A16 Bionic (4 nm)", "6GB", "128GB / 256GB / 512GB", "3349 mAh", "48 MP + 12 MP", "12 MP", "iOS 17", "$799"),
        ("Samsung", "Galaxy S24 Ultra", "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-s24-ultra-5g-sm-s928-u.jpg", "6.8 inch Dynamic LTPO AMOLED 2X, 120Hz", "Snapdragon 8 Gen 3 (4 nm)", "12GB", "256GB / 512GB / 1TB", "5000 mAh", "200 MP + 50 MP + 10 MP + 12 MP", "12 MP", "Android 14, One UI 6.1", "$1,299"),
        ("Samsung", "Galaxy S23", "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-s23-5g.jpg", "6.1 inch Dynamic AMOLED 2X, 120Hz", "Snapdragon 8 Gen 2 (4 nm)", "8GB", "128GB / 256GB / 512GB", "3900 mAh", "50 MP + 10 MP + 12 MP", "12 MP", "Android 13", "$799"),
        ("Google", "Pixel 8 Pro", "https://fdn2.gsmarena.com/vv/bigpic/google-pixel-8-pro.jpg", "6.7 inch LTPO OLED, 120Hz", "Google Tensor G3 (4 nm)", "12GB", "128GB / 256GB / 512GB / 1TB", "5050 mAh", "50 MP + 48 MP + 48 MP", "10.5 MP", "Android 14", "$999"),
        ("OnePlus", "OnePlus 12", "https://fdn2.gsmarena.com/vv/bigpic/oneplus-12.jpg", "6.82 inch LTPO AMOLED, 120Hz", "Snapdragon 8 Gen 3 (4 nm)", "12GB / 16GB / 24GB", "256GB / 512GB / 1TB", "5400 mAh", "50 MP + 64 MP + 48 MP", "32 MP", "Android 14, OxygenOS 14", "$799"),
        ("Nothing", "Phone (2)", "https://fdn2.gsmarena.com/vv/bigpic/nothing-phone2.jpg", "6.7 inch LTPO AMOLED, 120Hz", "Snapdragon 8+ Gen 1 (4 nm)", "8GB / 12GB", "128GB / 256GB / 512GB", "4700 mAh", "50 MP + 50 MP", "32 MP", "Android 13, Nothing OS 2.5", "$599"),
        ("Samsung", "Galaxy Z Fold5", "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-z-fold5-5g.jpg", "7.6 inch Foldable Dynamic AMOLED 2X, 120Hz", "Snapdragon 8 Gen 2 (4 nm)", "12GB", "256GB / 512GB / 1TB", "4400 mAh", "50 MP + 10 MP + 12 MP", "4 MP (under display) + 10 MP (cover)", "Android 13", "$1,799")
    ]
    
    c.executemany('''
        INSERT INTO phones (brand, model, image_url, display, processor, ram, storage, battery, camera_main, camera_selfie, os, price)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', phones)
    
    conn.commit()
    conn.close()
    print("mobiles.db initialized and seeded with sample data.")

if __name__ == '__main__':
    init_db()
