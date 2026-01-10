import os, requests, json, google.generativeai as genai
from instagrapi import Client

# Puxa os dados das chaves do GitHub
SESSION_DATA = os.environ.get("INSTA_SESSION")
GEMINI_API = os.environ.get("GEMINI_KEY")

def robo_autonomo():
    cl = Client()
    
    try:
        print("🚀 Carregando sessão...")
        # Cria o arquivo de sessão a partir do seu Secret
        with open("session.json", "w") as f:
            f.write(SESSION_DATA)
        cl.load_settings("session.json")
        
        print("🔎 Buscando imagem...")
        url = "https://images.unsplash.com/photo-1551727041-5b347d65b633?q=80&w=1080"
        img_res = requests.get(url)
        with open('post.jpg', 'wb') as f: f.write(img_res.content)
        
        print("🤖 Gerando legenda...")
        try:
            genai.configure(api_key=GEMINI_API)
            model = genai.GenerativeModel('gemini-pro')
            legenda = model.generate_content("Crie uma legenda sobre milho verde.").text
        except:
            legenda = "Milho de qualidade! 🌽"

        print("📤 Tentando postar...")
        media = cl.photo_upload("post.jpg", legenda)
        if media:
            print(f"✅ SUCESSO! Post ID: {media.pk}")
            
    except Exception as e:
        print(f"❌ OCORREU UM ERRO TÉCNICO: {e}")

if __name__ == "__main__":
    robo_autonomo()
