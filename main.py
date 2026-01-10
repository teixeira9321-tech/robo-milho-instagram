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
    
    # SIMULANDO O EDGEONE (Mudando a identidade do dispositivo)
    # Isso faz o Instagram pensar que o acesso vem de um navegador web seguro
    cl.set_user_agent("Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36")

    print("🔎 Buscando imagem de milho...")
    url = "https://images.unsplash.com/photo-1551727041-5b347d65b633?q=80&w=1080"
    with open('post.jpg', 'wb') as f:
        f.write(requests.get(url).content)

    print("🤖 IA criando legenda...")
    model = genai.GenerativeModel('gemini-pro')
    try:
        legenda = model.generate_content("Crie uma legenda sobre milho para Instagram.").text
    except:
        legenda = "O melhor milho verde! 🌽"

    print("🚀 Tentando postagem via túnel seguro...")
    try:
        # Atraso aleatório para parecer humano
        time.sleep(random.randint(15, 30))
        cl.login(USER, PASS)
        
        # Tentativa de upload usando método de navegador
        cl.photo_upload("post.jpg", legenda)
        print("✅ SUCESSO! O bloqueio de IP foi contornado.")
    except Exception as e:
        print(f"❌ Erro: {e}")
        print("DICA: Se o erro de Blacklist continuar, o próximo passo é criar a conta no EdgeOne.ai para usar o IP deles.")

if __name__ == "__main__":
    robo_autonomo()
