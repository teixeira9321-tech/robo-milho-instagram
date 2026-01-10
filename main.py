import os
import requests
import random
import time
import google.generativeai as genai
from instagrapi import Client

USER = os.environ.get("INSTA_USER")
PASS = os.environ.get("INSTA_PASS")
genai.configure(api_key=os.environ.get("GEMINI_KEY"))

def robo_autonomo():
    cl = Client()
    
    # Lista de termos para buscar fotos diferentes
    temas = ["corn+field", "corn+food", "pamonha", "milho+verde", "corn+harvest"]
    tema = random.choice(temas)
    
    print(f"🔎 Buscando imagem nova sobre: {tema}...")
    # Usando o Unsplash com um parâmetro de tempo para garantir foto nova
    url = f"https://source.unsplash.com/featured/?{tema}&sig={random.randint(1, 1000)}"
    
    response = requests.get(url)
    with open('post.jpg', 'wb') as f:
        f.write(response.content)

    print("🤖 IA criando legenda...")
    model = genai.GenerativeModel('gemini-pro')
    try:
        res = model.generate_content("Crie uma legenda curta e brasileira sobre milho verde para Instagram.")
        legenda = res.text
    except:
        legenda = "O melhor milho verde do Brasil! 🌽 #milho #premium"

    print("🚀 Tentando postar agora...")
    try:
        cl.login(USER, PASS)
        # Pequena espera para o Instagram processar o login
        time.sleep(10)
        cl.photo_upload("post.jpg", legenda)
        print("✨ POSTADO COM SUCESSO!")
    except Exception as e:
        print(f"⚠️ Erro ao postar: {e}")

if __name__ == "__main__":
    robo_autonomo()
