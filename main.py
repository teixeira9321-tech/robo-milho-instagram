import os
import requests
import time
import google.generativeai as genai
from instagrapi import Client

# Credenciais lidas dos Secrets do GitHub
USER = os.environ.get("INSTA_USER")
PASS = os.environ.get("INSTA_PASS")
genai.configure(api_key=os.environ.get("GEMINI_KEY"))

def robo_autonomo():
    cl = Client()
    
    print("🔎 Buscando imagem...")
    url = "https://images.unsplash.com/photo-1551727041-5b347d65b633?auto=format&fit=crop&w=1080&q=80"
    try:
        response = requests.get(url)
        with open('post.jpg', 'wb') as f:
            f.write(response.content)
    except Exception as e:
        print(f"Erro ao baixar imagem: {e}")
        return

    print("🤖 IA criando legenda...")
    model = genai.GenerativeModel('gemini-pro')
    try:
        res = model.generate_content("Crie uma legenda criativa sobre milho verde com emojis.")
        legenda = res.text
    except:
        legenda = "O melhor milho verde! 🌽 #milho"

    print("🚀 Tentando postar...")
    try:
        cl.login(USER, PASS)
        time.sleep(15) # Espera de segurança para o Instagram
        media = cl.photo_upload("post.jpg", legenda)
        if media:
            print(f"✅ SUCESSO! Post ID: {media.pk}")
    except Exception as e:
        print(f"❌ Erro real de postagem: {e}")

if __name__ == "__main__":
    robo_autonomo()
