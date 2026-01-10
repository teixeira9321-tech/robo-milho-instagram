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
    # Iniciamos o cliente limpando qualquer rastro anterior
    cl = Client()
    
    print("🔎 Buscando imagem...")
    url = "https://images.unsplash.com/photo-1551727041-5b347d65b633?q=80&w=1080"
    with open('post.jpg', 'wb') as f:
        f.write(requests.get(url).content)

    print("🤖 IA criando legenda...")
    model = genai.GenerativeModel('gemini-pro')
    try:
        legenda = model.generate_content("Crie uma legenda sobre milho verde para Instagram.").text
    except:
        legenda = "O melhor milho verde! 🌽 #milho"

    print("🚀 Resolvendo CSRF Token e fazendo login...")
    try:
        # Simulamos um navegador Android super atualizado
        cl.set_user_agent("Instagram 269.0.0.18.75 Android (26/8.0.0; 480dpi; 1080x1920; samsung; SM-G960F; starlte; exynos9810; pt_BR; 443213142)")
        
        # O segredo para o CSRF: delay aleatório antes de logar
        time.sleep(random.randint(20, 40))
        
        # Tentativa de login direto
        cl.login(USER, PASS)
        print("✅ Login autorizado!")
        
        time.sleep(10)
        print("📤 Enviando postagem...")
        # Forçamos o upload a esperar o processamento do token
        media = cl.photo_upload("post.jpg", legenda)
        
        if media:
            print(f"✨ SUCESSO! Post ID: {media.pk}")
            
    except Exception as e:
        # Se der erro de CSRF de novo, o código tentará limpar os cookies
        if "CSRF" in str(e):
            print("⚠️ Erro de Token detectado. Tentando limpeza de cache...")
            cl.logout()
            time.sleep(5)
        print(f"❌ Detalhe do Erro: {e}")

if __name__ == "__main__":
    robo_autonomo()
