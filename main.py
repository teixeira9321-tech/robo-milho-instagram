import os
import requests
import time
import google.generativeai as genai
from instagrapi import Client
from instagrapi.exceptions import ClientError

USER = os.environ.get("INSTA_USER")
PASS = os.environ.get("INSTA_PASS")
genai.configure(api_key=os.environ.get("GEMINI_KEY"))

def robo_autonomo():
    cl = Client()
    session_file = "session.json"

    print("🔎 Buscando imagem...")
    url = "https://images.unsplash.com/photo-1551727041-5b347d65b633?q=80&w=1080"
    response = requests.get(url)
    with open('post.jpg', 'wb') as f:
        f.write(response.content)

    print("🤖 IA criando legenda...")
    model = genai.GenerativeModel('gemini-pro')
    try:
        legenda = model.generate_content("Crie uma legenda sobre milho verde para Instagram.").text
    except:
        legenda = "O melhor milho verde! 🌽 #milho"

    print("🚀 Tentando login com bypass de IP...")
    try:
        # Tenta carregar sessão anterior se existir
        if os.path.exists(session_file):
            cl.load_settings(session_file)
        
        cl.login(USER, PASS)
        cl.dump_settings(session_file) # Salva a sessão para a próxima vez
        
        time.sleep(10)
        print("📤 Enviando postagem...")
        media = cl.photo_upload("post.jpg", legenda)
        
        if media:
            print(f"✅ SUCESSO! Post ID: {media.pk}")
    except ClientError as e:
        print(f"❌ Erro do Instagram: {e}")
        print("DICA: O Instagram bloqueou o IP. Tente entrar na conta pelo celular e clicar em 'Fui eu'.")
    except Exception as e:
        print(f"❌ Erro Geral: {e}")

if __name__ == "__main__":
    robo_autonomo()
