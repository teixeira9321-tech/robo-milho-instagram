import os
import requests
import time
import google.generativeai as genai
from instagrapi import Client

USER = os.environ.get("INSTA_USER")
PASS = os.environ.get("INSTA_PASS")
genai.configure(api_key=os.environ.get("GEMINI_KEY"))

def robo_autonomo():
    print("🔎 Buscando imagem de milho...")
    url = "https://images.unsplash.com/photo-1551727041-5b347d65b633?auto=format&fit=crop&w=1080&q=80"
    with open('post.jpg', 'wb') as f:
        f.write(requests.get(url).content)

    print("🤖 IA criando legenda...")
    model = genai.GenerativeModel('gemini-pro')
    try:
        legenda = model.generate_content("Crie uma legenda sobre milho verde.").text
    except:
        legenda = "O melhor milho verde! 🌽"

    print("🚀 Iniciando login...")
    cl = Client()
    # Espera 5 segundos antes de logar para não parecer robô imediato
    time.sleep(5)
    cl.login(USER, PASS)
    
    print("📤 Enviando post...")
    cl.photo_upload("post.jpg", legenda)
    print("✨ Sucesso!")

if __name__ == "__main__":
    robo_autonomo()
