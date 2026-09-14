import sqlite3

def init_db():
    conn = sqlite3.connect('mobiles.db')
    c = conn.cursor()
    
    c.execute('DROP TABLE IF EXISTS phones')
    
    # Create table with expanded features
    c.execute('''
        CREATE TABLE phones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT,
            model TEXT,
            image_url TEXT,
            screen_size TEXT,
            display_type TEXT,
            refresh_rate TEXT,
            processor TEXT,
            ram TEXT,
            storage TEXT,
            battery TEXT,
            fast_charging TEXT,
            camera_main TEXT,
            camera_selfie TEXT,
            weight TEXT,
            water_resistance TEXT,
            network_5g TEXT,
            os TEXT,
            price TEXT
        )
    ''')
    
    # Sample real-world data with expanded features
    phones = [
        ("Apple", "iPhone 15 Pro Max", "https://fdn2.gsmarena.com/vv/bigpic/apple-iphone-15-pro-max.jpg", "6.7 inches", "LTPO Super Retina XDR OLED", "120Hz", "Apple A17 Pro (3 nm)", "8 GB", "256 GB", "4441 mAh", "27W", "48 MP", "12 MP", "221 g", "IP68", "Yes", "iOS 17", "$1199"),
        ("Apple", "iPhone 15", "https://fdn2.gsmarena.com/vv/bigpic/apple-iphone-15.jpg", "6.1 inches", "Super Retina XDR OLED", "60Hz", "Apple A16 Bionic (4 nm)", "6 GB", "128 GB", "3349 mAh", "20W", "48 MP", "12 MP", "171 g", "IP68", "Yes", "iOS 17", "$799"),
        ("Samsung", "Galaxy S24 Ultra", "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-s24-ultra-5g-sm-s928-u.jpg", "6.8 inches", "Dynamic LTPO AMOLED 2X", "120Hz", "Snapdragon 8 Gen 3 (4 nm)", "12 GB", "256 GB", "5000 mAh", "45W", "200 MP", "12 MP", "232 g", "IP68", "Yes", "Android 14", "$1299"),
        ("Samsung", "Galaxy S23", "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-s23-5g.jpg", "6.1 inches", "Dynamic AMOLED 2X", "120Hz", "Snapdragon 8 Gen 2 (4 nm)", "8 GB", "128 GB", "3900 mAh", "25W", "50 MP", "12 MP", "168 g", "IP68", "Yes", "Android 13", "$799"),
        ("Google", "Pixel 8 Pro", "https://fdn2.gsmarena.com/vv/bigpic/google-pixel-8-pro.jpg", "6.7 inches", "LTPO OLED", "120Hz", "Google Tensor G3 (4 nm)", "12 GB", "128 GB", "5050 mAh", "30W", "50 MP", "10.5 MP", "213 g", "IP68", "Yes", "Android 14", "$999"),
        ("OnePlus", "OnePlus 12", "https://fdn2.gsmarena.com/vv/bigpic/oneplus-12.jpg", "6.82 inches", "LTPO AMOLED", "120Hz", "Snapdragon 8 Gen 3 (4 nm)", "12 GB", "256 GB", "5400 mAh", "100W", "50 MP", "32 MP", "220 g", "IP65", "Yes", "Android 14", "$799"),
        ("Nothing", "Phone (2)", "https://fdn2.gsmarena.com/vv/bigpic/nothing-phone2.jpg", "6.7 inches", "LTPO AMOLED", "120Hz", "Snapdragon 8+ Gen 1 (4 nm)", "8 GB", "128 GB", "4700 mAh", "45W", "50 MP", "32 MP", "201 g", "IP54", "Yes", "Android 13", "$599"),
        ("Samsung", "Galaxy Z Fold5", "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-z-fold5-5g.jpg", "7.6 inches", "Foldable Dynamic AMOLED 2X", "120Hz", "Snapdragon 8 Gen 2 (4 nm)", "12 GB", "256 GB", "4400 mAh", "25W", "50 MP", "4 MP", "253 g", "IPX8", "Yes", "Android 13", "$1799")
    ]
    
    c.executemany('''
        INSERT INTO phones (brand, model, image_url, screen_size, display_type, refresh_rate, processor, ram, storage, battery, fast_charging, camera_main, camera_selfie, weight, water_resistance, network_5g, os, price)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', phones)
    
    conn.commit()
    conn.close()
    print("mobiles.db initialized and seeded with expanded features.")

if __name__ == '__main__':
    init_db()
