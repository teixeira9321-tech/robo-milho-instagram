import os
import requests
import time
import random
import google.generativeai as genai
from instagrapi import Client

USER = os.environ.get("INSTA_USER")
PASS = os.environ.get("INSTA_PASS")
genai.configure(api_key=os.environ.get("GEMINI_KEY"))

def robo_autonomo():
    cl = Client()
    # SIMULAÇÃO DE DISPOSITIVO REAL
    cl.set_device_settings({
        "app_version": "269.0.0.18.75",
        "android_version": 26,
        "android_release": "8.0.0",
        "model": "SM-G960F",
        "manufacturer": "samsung"
    })

    print("🔎 Buscando imagem...")
    # Link de imagem de alta qualidade
    url = "https://images.unsplash.com/photo-1551727041-5b347d65b633?q=80&w=1080"
    with open('post.jpg', 'wb') as f:
        f.write(requests.get(url).content)

    print("🤖 IA criando legenda...")
    model = genai.GenerativeModel('gemini-pro')
    try:
        legenda = model.generate_content("Crie uma legenda sobre milho verde para o Instagram com hashtags.").text
    except:
        legenda = "O melhor milho verde! 🌽 #milhopremium"

    print("🚀 Iniciando login e postagem...")
    try:
        # Tenta logar com um pequeno atraso humano
        time.sleep(random.randint(5, 15))
        cl.login(USER, PASS)
        
        # O SEGREDO: Upload com verificação
        media = cl.photo_upload("post.jpg", legenda)
        
        if media:
            print(f"✅ SUCESSO ABSOLUTO! Link: https://www.instagram.com/p/{media.code}/")
        else:
            print("⚠️ O upload foi aceito, mas o Instagram não retornou o link do post.")

    except Exception as e:
        print(f"❌ ERRO TÉCNICO: {e}")

if __name__ == "__main__":
    robo_autonomo()
