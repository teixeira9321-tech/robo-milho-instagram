import os, requests, json, google.generativeai as genai
from instagrapi import Client

# Puxa o "crachá" e a chave da IA
SESSION_DATA = os.environ.get("INSTA_SESSION")
genai.configure(api_key=os.environ.get("GEMINI_KEY"))

def robo_autonomo():
    cl = Client()
    
    print("🚀 Carregando sessão aprovada pelo Termux...")
    # Transforma o texto do Secret em um arquivo de sessão real
    with open("session.json", "w") as f:
        f.write(SESSION_DATA)
    
    cl.load_settings("session.json")
    
    print("🔎 Buscando imagem e gerando legenda...")
    url = "https://images.unsplash.com/photo-1551727041-5b347d65b633?q=80&w=1080"
    img_data = requests.get(url).content
    with open('post.jpg', 'wb') as f: f.write(img_data)
    
    model = genai.GenerativeModel('gemini-pro')
    legenda = model.generate_content("Crie uma legenda sobre milho verde para Instagram.").text

    print("📤 Postando direto (sem precisar de login)...")
    try:
        # Aqui o robô pula o erro de CSRF porque já entra logado
        media = cl.photo_upload("post.jpg", legenda)
        if media:
            print(f"✅ SUCESSO TOTAL! Postado no perfil @milhopremium_")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    robo_autonomo()
