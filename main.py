
import os
import requests
import google.generativeai as genai
from instagrapi import Client

# Pega as senhas escondidas nos Secrets do GitHub
USER = os.environ.get("INSTA_USER")
PASS = os.environ.get("INSTA_PASS")
genai.configure(api_key=os.environ.get("GEMINI_KEY"))

def robo_autonomo():
    print("🔎 Buscando imagem de milho...")
    # Link direto para foto de milho
    url = "https://images.unsplash.com/photo-1551727041-5b347d65b633?auto=format&fit=crop&w=1080&q=80"
    with open('post.jpg', 'wb') as f:
        f.write(requests.get(url).content)

    print("🤖 IA criando legenda...")
    model = genai.GenerativeModel('gemini-pro')
    try:
        res = model.generate_content("Crie uma legenda curta e alegre sobre milho verde e roça.")
        legenda = res.text
    except:
        legenda = "O melhor do milho verde para você! 🌽 #milho #roça"

    print("🚀 Postando no Instagram...")
    cl = Client()
    cl.login(USER, PASS)
    cl.photo_upload("post.jpg", legenda)
    print("✨ Sucesso!")

if __name__ == "__main__":
    robo_autonomo()
