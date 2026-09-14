import sqlite3
import re

def make_slug(brand, model):
    s = f"{brand} {model}".lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')

phones_data = [
    # 2026 Apple
    {"brand": "Apple", "model": "iPhone 18 Pro Max", "image_url": "https://fdn2.gsmarena.com/vv/bigpic/apple-iphone-15-pro-max.jpg", "screen_size": "6.9 inches", "display_type": "LTPO Super Retina XDR OLED", "refresh_rate": "120Hz", "processor": "Apple A20 Pro (2 nm)", "ram": "12 GB", "storage": "1 TB", "battery": "4800 mAh", "fast_charging": "45W", "camera_main": "48 MP", "camera_selfie": "24 MP", "weight": "225 g", "water_resistance": "IP68", "network_5g": "Yes", "os": "iOS 20", "price": "$1299"},
    {"brand": "Apple", "model": "iPhone 18 Pro", "image_url": "https://fdn2.gsmarena.com/vv/bigpic/apple-iphone-15-pro.jpg", "screen_size": "6.3 inches", "display_type": "LTPO Super Retina XDR OLED", "refresh_rate": "120Hz", "processor": "Apple A20 Pro (2 nm)", "ram": "12 GB", "storage": "512 GB", "battery": "3500 mAh", "fast_charging": "45W", "camera_main": "48 MP", "camera_selfie": "24 MP", "weight": "195 g", "water_resistance": "IP68", "network_5g": "Yes", "os": "iOS 20", "price": "$1099"},
    {"brand": "Apple", "model": "iPhone 18", "image_url": "https://fdn2.gsmarena.com/vv/bigpic/apple-iphone-15.jpg", "screen_size": "6.1 inches", "display_type": "Super Retina XDR OLED", "refresh_rate": "120Hz", "processor": "Apple A19 (3 nm)", "ram": "8 GB", "storage": "256 GB", "battery": "3400 mAh", "fast_charging": "30W", "camera_main": "48 MP", "camera_selfie": "12 MP", "weight": "170 g", "water_resistance": "IP68", "network_5g": "Yes", "os": "iOS 20", "price": "$799"},
    
    # 2025 Apple
    {"brand": "Apple", "model": "iPhone 17 Pro Max", "image_url": "https://fdn2.gsmarena.com/vv/bigpic/apple-iphone-15-pro-max.jpg", "screen_size": "6.9 inches", "display_type": "LTPO Super Retina XDR OLED", "refresh_rate": "120Hz", "processor": "Apple A19 Pro (3 nm)", "ram": "12 GB", "storage": "512 GB", "battery": "4600 mAh", "fast_charging": "35W", "camera_main": "48 MP", "camera_selfie": "24 MP", "weight": "221 g", "water_resistance": "IP68", "network_5g": "Yes", "os": "iOS 19", "price": "$1199"},
    {"brand": "Apple", "model": "iPhone 17 Air", "image_url": "https://fdn2.gsmarena.com/vv/bigpic/apple-iphone-15.jpg", "screen_size": "6.6 inches", "display_type": "Super Retina XDR OLED", "refresh_rate": "120Hz", "processor": "Apple A19 (3 nm)", "ram": "8 GB", "storage": "256 GB", "battery": "3800 mAh", "fast_charging": "30W", "camera_main": "48 MP", "camera_selfie": "24 MP", "weight": "155 g", "water_resistance": "IP68", "network_5g": "Yes", "os": "iOS 19", "price": "$899"},
    
    # 2026 Samsung
    {"brand": "Samsung", "model": "Galaxy S26 Ultra", "image_url": "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-s24-ultra-5g-sm-s928-u.jpg", "screen_size": "6.9 inches", "display_type": "Dynamic AMOLED 3X", "refresh_rate": "144Hz", "processor": "Snapdragon 8 Gen 5 (2 nm)", "ram": "16 GB", "storage": "1 TB", "battery": "5500 mAh", "fast_charging": "65W", "camera_main": "200 MP", "camera_selfie": "12 MP", "weight": "230 g", "water_resistance": "IP68", "network_5g": "Yes", "os": "Android 16", "price": "$1399"},
    {"brand": "Samsung", "model": "Galaxy S26", "image_url": "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-s24.jpg", "screen_size": "6.2 inches", "display_type": "Dynamic AMOLED 3X", "refresh_rate": "120Hz", "processor": "Snapdragon 8 Gen 5 (2 nm)", "ram": "12 GB", "storage": "256 GB", "battery": "4200 mAh", "fast_charging": "45W", "camera_main": "50 MP", "camera_selfie": "12 MP", "weight": "165 g", "water_resistance": "IP68", "network_5g": "Yes", "os": "Android 16", "price": "$849"},
    {"brand": "Samsung", "model": "Galaxy Z Fold 7", "image_url": "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-z-fold5-5g.jpg", "screen_size": "7.8 inches", "display_type": "Foldable Dynamic AMOLED 2X", "refresh_rate": "120Hz", "processor": "Snapdragon 8 Gen 4 (3 nm)", "ram": "16 GB", "storage": "512 GB", "battery": "4800 mAh", "fast_charging": "45W", "camera_main": "200 MP", "camera_selfie": "12 MP", "weight": "235 g", "water_resistance": "IPX8", "network_5g": "Yes", "os": "Android 15", "price": "$1799"},

    # 2025 Samsung
    {"brand": "Samsung", "model": "Galaxy S25 Ultra", "image_url": "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-s24-ultra-5g-sm-s928-u.jpg", "screen_size": "6.86 inches", "display_type": "Dynamic AMOLED 2X", "refresh_rate": "120Hz", "processor": "Snapdragon 8 Gen 4 (3 nm)", "ram": "12 GB", "storage": "512 GB", "battery": "5000 mAh", "fast_charging": "45W", "camera_main": "200 MP", "camera_selfie": "12 MP", "weight": "219 g", "water_resistance": "IP68", "network_5g": "Yes", "os": "Android 15", "price": "$1299"},
    
    # 2026 Google
    {"brand": "Google", "model": "Pixel 11 Pro XL", "image_url": "https://fdn2.gsmarena.com/vv/bigpic/google-pixel-8-pro.jpg", "screen_size": "6.8 inches", "display_type": "Super Actua OLED", "refresh_rate": "120Hz", "processor": "Google Tensor G6 (2 nm)", "ram": "16 GB", "storage": "512 GB", "battery": "5200 mAh", "fast_charging": "45W", "camera_main": "50 MP", "camera_selfie": "42 MP", "weight": "215 g", "water_resistance": "IP68", "network_5g": "Yes", "os": "Android 17", "price": "$1099"},
    {"brand": "Google", "model": "Pixel 11", "image_url": "https://fdn2.gsmarena.com/vv/bigpic/google-pixel-8.jpg", "screen_size": "6.3 inches", "display_type": "Actua OLED", "refresh_rate": "120Hz", "processor": "Google Tensor G6 (2 nm)", "ram": "12 GB", "storage": "256 GB", "battery": "4700 mAh", "fast_charging": "35W", "camera_main": "50 MP", "camera_selfie": "10.5 MP", "weight": "185 g", "water_resistance": "IP68", "network_5g": "Yes", "os": "Android 17", "price": "$799"},
    
    # 2025 Google
    {"brand": "Google", "model": "Pixel 10 Pro", "image_url": "https://fdn2.gsmarena.com/vv/bigpic/google-pixel-8-pro.jpg", "screen_size": "6.3 inches", "display_type": "Super Actua OLED", "refresh_rate": "120Hz", "processor": "Google Tensor G5 (3 nm)", "ram": "16 GB", "storage": "256 GB", "battery": "4700 mAh", "fast_charging": "35W", "camera_main": "50 MP", "camera_selfie": "42 MP", "weight": "199 g", "water_resistance": "IP68", "network_5g": "Yes", "os": "Android 16", "price": "$999"},

    # 2026/2025 OnePlus & Xiaomi
    {"brand": "OnePlus", "model": "OnePlus 14", "image_url": "https://fdn2.gsmarena.com/vv/bigpic/oneplus-12.jpg", "screen_size": "6.82 inches", "display_type": "LTPO AMOLED", "refresh_rate": "144Hz", "processor": "Snapdragon 8 Gen 5 (2 nm)", "ram": "16 GB", "storage": "512 GB", "battery": "6000 mAh", "fast_charging": "120W", "camera_main": "50 MP", "camera_selfie": "32 MP", "weight": "215 g", "water_resistance": "IP68", "network_5g": "Yes", "os": "Android 16", "price": "$899"},
    {"brand": "Xiaomi", "model": "Xiaomi 16 Ultra", "image_url": "https://fdn2.gsmarena.com/vv/bigpic/xiaomi-14-ultra.jpg", "screen_size": "6.73 inches", "display_type": "LTPO AMOLED", "refresh_rate": "120Hz", "processor": "Snapdragon 8 Gen 5 (2 nm)", "ram": "16 GB", "storage": "1 TB", "battery": "5500 mAh", "fast_charging": "90W", "camera_main": "50 MP", "camera_selfie": "32 MP", "weight": "225 g", "water_resistance": "IP68", "network_5g": "Yes", "os": "Android 16", "price": "$1299"},
    {"brand": "Nothing", "model": "Phone (4)", "image_url": "https://fdn2.gsmarena.com/vv/bigpic/nothing-phone2.jpg", "screen_size": "6.7 inches", "display_type": "LTPO AMOLED", "refresh_rate": "120Hz", "processor": "Snapdragon 8 Gen 3 (4 nm)", "ram": "12 GB", "storage": "256 GB", "battery": "5000 mAh", "fast_charging": "45W", "camera_main": "50 MP", "camera_selfie": "32 MP", "weight": "195 g", "water_resistance": "IP54", "network_5g": "Yes", "os": "Android 15", "price": "$649"}
]

def init_db():
    conn = sqlite3.connect('mobiles.db')
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS phones')
    c.execute('''
        CREATE TABLE phones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT UNIQUE,
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
    
    insert_data = []
    for p in phones_data:
        slug = make_slug(p["brand"], p["model"])
        # Ensure correct order
        tup = (slug, p["brand"], p["model"], p["image_url"], p["screen_size"], p["display_type"],
               p["refresh_rate"], p["processor"], p["ram"], p["storage"], p["battery"], 
               p["fast_charging"], p["camera_main"], p["camera_selfie"], p["weight"], 
               p["water_resistance"], p["network_5g"], p["os"], p["price"])
        insert_data.append(tup)
        
    c.executemany('''
        INSERT INTO phones (slug, brand, model, image_url, screen_size, display_type, refresh_rate, processor, ram, storage, battery, fast_charging, camera_main, camera_selfie, weight, water_resistance, network_5g, os, price)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', insert_data)
    
    conn.commit()
    conn.close()
    print(f"Successfully seeded DB with {len(phones_data)} flagship phones for 2025/2026!")

if __name__ == '__main__':
    init_db()
