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
    # Muda o ID do dispositivo para parecer um celular novo e evitar a lista negra
    cl.set_device_settings({
        "app_version": "269.0.0.18.75",
        "android_version": random.randint(26, 30),
        "android_release": str(random.randint(9, 12)),
        "model": random.choice(["SM-G960F", "Pixel 4", "SM-A505FN"]),
        "manufacturer": random.choice(["samsung", "google", "xiaomi"])
    })

    print("🔎 Buscando imagem...")
    url = "https://images.unsplash.com/photo-1551727041-5b347d65b633?auto=format&fit=crop&w=1080&q=80"
    img_data = requests.get(url).content
    with open('post.jpg', 'wb') as f:
        f.write(img_data)

    print("🤖 IA criando legenda...")
    model = genai.GenerativeModel('gemini-pro')
    try:
        legenda = model.generate_content("Crie uma legenda sobre milho verde para Instagram.").text
    except:
        legenda = "O melhor milho verde! 🌽 #milho"

    print("🚀 Tentando login seguro...")
    try:
        # Tenta logar com um atraso aleatório para enganar o sistema
        time.sleep(random.randint(10, 30))
        cl.login(USER, PASS)
        print("✅ Login realizado!")
        
        print("📤 Enviando postagem...")
        cl.photo_upload("post.jpg", legenda)
        print("✨ SUCESSO TOTAL!")
    except Exception as e:
        print(f"⚠️ Erro de Login: {e}")
        print("DICA: Verifique se sua senha no GitHub Secret está 100% correta.")

if __name__ == "__main__":
    robo_autonomo()
    
