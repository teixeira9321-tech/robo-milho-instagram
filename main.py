import os, requests, time, random, google.generativeai as genai
from instagrapi import Client

USER = os.environ.get("INSTA_USER")
PASS = os.environ.get("INSTA_PASS")
genai.configure(api_key=os.environ.get("GEMINI_KEY"))

def robo():
    cl = Client()
    # Identidade de navegador para evitar erro de Token
    cl.set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    
    # Busca imagem
    res = requests.get("https://images.unsplash.com/photo-1551727041-5b347d65b633?w=1080")
    with open('post.jpg', 'wb') as f: f.write(res.content)

    # IA e Post
    try:
        cl.login(USER, PASS)
        time.sleep(30) # Espera pro Token validar
        cl.photo_upload("post.jpg", "Milho de qualidade! 🌽")
        print("✅ POSTADO!")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__": robo()
