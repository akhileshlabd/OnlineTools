import json
import os

filepath = 'static/data/characters.json'

with open(filepath, 'r') as f:
    characters = json.load(f)

indian_characters = [
  # Cricket
  {"name": "Virat Kohli", "image": "🏏", "traits": {"isReal": True, "isMale": True, "isAthlete": True, "isIndian": True, "isCricketer": True, "hasBeard": True}},
  {"name": "MS Dhoni", "image": "🚁", "traits": {"isReal": True, "isMale": True, "isAthlete": True, "isIndian": True, "isCricketer": True, "isCaptain": True}},
  {"name": "Sachin Tendulkar", "image": "🏏", "traits": {"isReal": True, "isMale": True, "isAthlete": True, "isIndian": True, "isCricketer": True, "isGod": False, "isAlive": True}},
  {"name": "Rohit Sharma", "image": "🏏", "traits": {"isReal": True, "isMale": True, "isAthlete": True, "isIndian": True, "isCricketer": True, "hasBeard": True}},
  
  # Bollywood
  {"name": "Shah Rukh Khan", "image": "🎬", "traits": {"isReal": True, "isMale": True, "isActor": True, "isIndian": True, "isMuslim": True}},
  {"name": "Amitabh Bachchan", "image": "👓", "traits": {"isReal": True, "isMale": True, "isActor": True, "isIndian": True, "isOld": True, "hasBeard": True, "wearsGlasses": True}},
  {"name": "Salman Khan", "image": "💪", "traits": {"isReal": True, "isMale": True, "isActor": True, "isIndian": True, "isMuslim": True, "isUnmarried": True}},
  {"name": "Rajinikanth", "image": "🕶️", "traits": {"isReal": True, "isMale": True, "isActor": True, "isIndian": True, "isSouthIndian": True, "isOld": True}},
  {"name": "Prabhas (Baahubali)", "image": "⚔️", "traits": {"isReal": True, "isMale": True, "isActor": True, "isIndian": True, "isSouthIndian": True}},
  {"name": "Allu Arjun", "image": "🕺", "traits": {"isReal": True, "isMale": True, "isActor": True, "isIndian": True, "isSouthIndian": True, "isDancer": True}},
  {"name": "Deepika Padukone", "image": "👗", "traits": {"isReal": True, "isFemale": True, "isActor": True, "isIndian": True}},
  {"name": "Priyanka Chopra", "image": "🌐", "traits": {"isReal": True, "isFemale": True, "isActor": True, "isIndian": True, "isAmerican": True}},
  {"name": "Aamir Khan", "image": "🎬", "traits": {"isReal": True, "isMale": True, "isActor": True, "isIndian": True, "isMuslim": True}},
  
  # Politics & History
  {"name": "Narendra Modi", "image": "🇮🇳", "traits": {"isReal": True, "isMale": True, "isPolitician": True, "isIndian": True, "isPrimeMinister": True, "hasBeard": True}},
  {"name": "Mahatma Gandhi", "image": "🕊️", "traits": {"isReal": True, "isMale": True, "isPolitician": True, "isIndian": True, "isAlive": False, "wearsGlasses": True, "isBald": True}},
  {"name": "APJ Abdul Kalam", "image": "🚀", "traits": {"isReal": True, "isMale": True, "isScientist": True, "isPresident": True, "isIndian": True, "isAlive": False, "isMuslim": True}},
  {"name": "B. R. Ambedkar", "image": "📖", "traits": {"isReal": True, "isMale": True, "isPolitician": True, "isIndian": True, "isAlive": False, "wearsGlasses": True}},
  {"name": "Subhas Chandra Bose", "image": "🎖️", "traits": {"isReal": True, "isMale": True, "isPolitician": True, "isSoldier": True, "isIndian": True, "isAlive": False}},
  
  # Business & Tech
  {"name": "Mukesh Ambani", "image": "🏢", "traits": {"isReal": True, "isMale": True, "isBillionaire": True, "isIndian": True, "isBusiness": True}},
  {"name": "Ratan Tata", "image": "🚗", "traits": {"isReal": True, "isMale": True, "isBillionaire": True, "isIndian": True, "isBusiness": True, "isOld": True}},
  {"name": "Sundar Pichai", "image": "💻", "traits": {"isReal": True, "isMale": True, "isTech": True, "isIndian": True, "isAmerican": True, "wearsGlasses": True}},
  
  # Fictional & Mythology
  {"name": "Shaktimaan", "image": "🦸‍♂️", "traits": {"isReal": False, "isMale": True, "hasSuperpowers": True, "isIndian": True, "isTvCharacter": True}},
  {"name": "Chhota Bheem", "image": "💪", "traits": {"isReal": False, "isMale": True, "isCartoon": True, "isIndian": True, "isChild": True}},
  {"name": "Motu", "image": "🥟", "traits": {"isReal": False, "isMale": True, "isCartoon": True, "isIndian": True, "isFat": True, "isBald": True}},
  {"name": "Patlu", "image": "👓", "traits": {"isReal": False, "isMale": True, "isCartoon": True, "isIndian": True, "wearsGlasses": True, "isBald": True}},
  {"name": "Lord Rama", "image": "🏹", "traits": {"isReal": False, "isMale": True, "isGod": True, "isIndian": True, "usesWeapons": True}},
  {"name": "Lord Krishna", "image": "🦚", "traits": {"isReal": False, "isMale": True, "isGod": True, "isIndian": True, "isBlue": True}},
  {"name": "Hanuman", "image": "🐒", "traits": {"isReal": False, "isMale": True, "isGod": True, "isIndian": True, "isAnimal": True, "hasSuperpowers": True}},
  
  # Musicians
  {"name": "A.R. Rahman", "image": "🎹", "traits": {"isReal": True, "isMale": True, "isMusician": True, "isIndian": True, "isSouthIndian": True}},
  {"name": "Arijit Singh", "image": "🎤", "traits": {"isReal": True, "isMale": True, "isMusician": True, "isIndian": True, "hasBeard": True}}
]

# Filter out duplicates by name
existing_names = {c['name'] for c in characters}
for c in indian_characters:
    if c['name'] not in existing_names:
        characters.append(c)

with open(filepath, 'w') as f:
    json.dump(characters, f, indent=2)

print(f"Total characters now: {len(characters)}")
