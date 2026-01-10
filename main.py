import os
import requests
import time
import google.generativeai as genai
from instagrapi import Client

# Puxando as senhas do GitHub
USER = os.environ.get("INSTA_USER")
PASS = os.environ.get("INSTA_PASS")
genai.configure(api_key=os.environ.get("GEMINI_KEY"))

def robo_autonomo():
    cl = Client()
    
    print("🔎 Buscando imagem...")
    # Usando uma imagem estável de milho
    url = "https://images.unsplash.com/photo-1551727041-5b347d65b633?q=80&w=1080"
    response = requests.get(url)
    with open('post.jpg', 'wb') as f:
        f.write(response.content)

    print("🤖 IA criando legenda...")
    model = genai.GenerativeModel('gemini-pro')
    try:
        res = model.generate_content("Crie uma legenda divertida sobre milho verde para Instagram.")
        legenda = res.text
    except:
        legenda = "O melhor milho verde! 🌽 #milho #roça"

    print("🚀 Iniciando login...")
    try:
        cl.login(USER, PASS)
        time.sleep(10) # Espera humana
        
        print("📤 Enviando postagem...")
        # Comando padrão e seguro de upload
        media = cl.photo_upload("post.jpg", legenda)
        
        if media:
            print(f"✅ SUCESSO! Post ID: {media.pk}")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    robo_autonomo()
