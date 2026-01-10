import os
import requests
import time
import google.generativeai as genai
from instagrapi import Client

USER = os.environ.get("INSTA_USER")
PASS = os.environ.get("INSTA_PASS")
genai.configure(api_key=os.environ.get("GEMINI_KEY"))

def robo_autonomo():
    cl = Client()
    
    # Busca imagem
    url = "https://images.unsplash.com/photo-1551727041-5b347d65b633?auto=format&fit=crop&w=1080&q=80"
    with open('post.jpg', 'wb') as f:
        f.write(requests.get(url).content)

    # IA gera legenda
    model = genai.GenerativeModel('gemini-pro')
    try:
        legenda = model.generate_content("Crie uma legenda sobre milho verde com emojis.").text
    except:
        legenda = "O melhor milho verde! 🌽 #milho"

    print("🚀 Tentando postar...")
    try:
        # 1. Faz o login
        cl.login(USER, PASS)
        time.sleep(15) # Espera 15 segundos para o sistema 'respirar'
        
        # 2. Faz o upload da foto
        # Usamos 'upload_photo' que é mais estável na nuvem
        media = cl.photo_upload("post.jpg", legenda)
        
        if media:
            print(f"✅ SUCESSO! Post ID: {media.pk}")
        else:
            print("⚠️ O Instagram aceitou o comando, mas não gerou um ID de postagem.")
            
    except Exception as e:
        print(f"❌ Erro real: {e}")

if __name__ == "__main__":
    robo_autonomo()
