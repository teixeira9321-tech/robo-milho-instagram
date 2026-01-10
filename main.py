import os
import requests
import time
import google.generativeai as genai
from instagrapi import Client

# Credenciais do ambiente GitHub
USER = os.environ.get("INSTA_USER")
PASS = os.environ.get("INSTA_PASS")
genai.configure(api_key=os.environ.get("GEMINI_KEY"))

def robo_autonomo():
    cl = Client()
    
    print("🔎 Buscando imagem temática...")
    # Link direto de uma foto de milho para teste rápido e seguro
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
        # Prompt direto para evitar erros de resposta da IA
        res = model.generate_content("Crie uma legenda curta para Instagram sobre milho verde com emojis.")
        legenda = res.text
    except:
        legenda = "O melhor do milho verde direto para você! 🌽 #milho #roça"

    print("🚀 Realizando login seguro...")
    try:
        # Removemos o comando problemático e usamos apenas o login direto
        cl.login(USER, PASS)
        print("✅ Login realizado com sucesso!")
        
        print("📤 Enviando postagem ao perfil @milhopremium_...")
        cl.photo_upload("post.jpg", legenda)
        print("✨ SUCESSO TOTAL!")
    except Exception as e:
        print(f"⚠️ Erro de Login/Postagem: {e}")
        print("DICA: Verifique se sua senha no GitHub Secret está correta e sem espaços.")

if __name__ == "__main__":
    robo_autonomo()
