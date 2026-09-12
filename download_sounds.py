import urllib.request
import ssl
import time
import os

ssl._create_default_https_context = ssl._create_unverified_context

sounds = {
    'Dog': 'https://upload.wikimedia.org/wikipedia/commons/7/7b/Dog_barking.ogg',
    'Cat': 'https://upload.wikimedia.org/wikipedia/commons/9/91/Kitten_meow.ogg',
    'Cow': 'https://upload.wikimedia.org/wikipedia/commons/d/d3/Cow_moo.ogg',
    'Pig': 'https://upload.wikimedia.org/wikipedia/commons/9/9a/Pig_oink.ogg',
    'Frog': 'https://upload.wikimedia.org/wikipedia/commons/7/78/Frog_croaking.ogg',
    'Lion': 'https://upload.wikimedia.org/wikipedia/commons/6/61/Lion_roar.ogg',
    'Monkey': 'https://upload.wikimedia.org/wikipedia/commons/b/b5/Monkey_chatter.ogg',
    'Elephant': 'https://upload.wikimedia.org/wikipedia/commons/6/6f/Elephant_trumpet.ogg',
    'Chicken': 'https://upload.wikimedia.org/wikipedia/commons/6/68/Chicken_clucking.ogg',
    'Sheep': 'https://upload.wikimedia.org/wikipedia/commons/f/fb/Sheep_bleat.ogg',
    'Duck': 'https://upload.wikimedia.org/wikipedia/commons/1/1a/Duck_quack.ogg',
    'Horse': 'https://upload.wikimedia.org/wikipedia/commons/c/c5/Horse_whinny.ogg'
}

opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')]
urllib.request.install_opener(opener)

os.makedirs('static/sounds/animals', exist_ok=True)

for name, url in sounds.items():
    try:
        filename = f"{name}.ogg".lower()
        urllib.request.urlretrieve(url, f"static/sounds/animals/{filename}")
        print(f"Downloaded {filename}")
        time.sleep(1) # prevent 429
    except Exception as e:
        print(f"Failed to download {filename}: {e}")
