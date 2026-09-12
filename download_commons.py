import urllib.request
import urllib.parse
import json
import os
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

animals = ['dog bark', 'cat meow', 'cow moo', 'pig oink', 'frog croak', 'lion roar', 'monkey chatter', 'elephant trumpet', 'chicken cluck', 'sheep bleat', 'duck quack', 'horse whinny']

os.makedirs('static/sounds/animals', exist_ok=True)

for query in animals:
    try:
        search_url = f"https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(query)}&srnamespace=6&format=json"
        req = urllib.request.Request(search_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
            
        if data['query']['search']:
            title = data['query']['search'][0]['title']
            info_url = f"https://commons.wikimedia.org/w/api.php?action=query&titles={urllib.parse.quote(title)}&prop=imageinfo&iiprop=url&format=json"
            req2 = urllib.request.Request(info_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req2) as response2:
                data2 = json.loads(response2.read())
                pages = data2['query']['pages']
                for page_id in pages:
                    url = pages[page_id]['imageinfo'][0]['url']
                    if url.endswith('.ogg') or url.endswith('.wav') or url.endswith('.mp3') or url.endswith('.oga'):
                        animal = query.split()[0]
                        ext = url.split('.')[-1]
                        urllib.request.urlretrieve(url, f"static/sounds/animals/{animal}.{ext}")
                        print(f"Downloaded {animal}")
                        break
                    else:
                        print(f"Skipping {query}, not an audio file: {url}")
        else:
            print(f"No results for {query}")
    except Exception as e:
        print(f"Error on {query}: {e}")
