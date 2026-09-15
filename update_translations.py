import json

with open('translations.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

data['hero_title']['en'] = "100% Free & Secure. Zero Server Uploads."
data['hero_title']['es'] = "100% Gratis y Seguro. Cero Subidas al Servidor."
data['hero_title']['pt'] = "100% Grátis e Seguro. Zero Uploads para o Servidor."
data['hero_title']['hi'] = "100% मुफ़्त और सुरक्षित। कोई सर्वर अपलोड नहीं।"

data['hero_subtitle']['en'] = "Your privacy is our priority. Unlike competitors, our powerful PDF and Image tools process files locally in your browser. No data ever leaves your device."
data['hero_subtitle']['es'] = "Tu privacidad es nuestra prioridad. A diferencia de los competidores, nuestras herramientas de PDF e Imágenes procesan los archivos localmente en tu navegador. Ningún dato sale de tu dispositivo."
data['hero_subtitle']['pt'] = "Sua privacidade é nossa prioridade. Ao contrário dos concorrentes, nossas ferramentas de PDF e Imagem processam arquivos localmente em seu navegador. Nenhum dado sai do seu dispositivo."
data['hero_subtitle']['hi'] = "आपकी निजता हमारी प्राथमिकता है। अन्य टूल के विपरीत, हमारे पीडीएफ और इमेज टूल सीधे आपके ब्राउज़र में काम करते हैं। आपका डेटा कभी भी आपके डिवाइस से बाहर नहीं जाता है।"

with open('translations.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
