import os
import requests
import json
import time
import google.generativeai as genai
from instagrapi import Client

# Configurações de ambiente do GitHub
SESSION_JSON = os.environ.get("INSTA_SESSION")
GEMINI_KEY = os.environ.get("GEMINI_KEY")

def robo_milho_premium():
    # 1. Verificação de Segurança do Secret
    if not SESSION_JSON:
        print("❌ ERRO: O Secret 'INSTA_SESSION' está vazio ou não foi configurado.")
        return

    cl = Client()
    
    try:
        # 2. Bypass de Login usando a Sessão do Termux
        print("🚀 Carregando identidade digital (Sessão)...")
        with open("session.json", "w") as f:
            f.write(SESSION_JSON)
        
        # Carrega as configurações sem precisar de login/senha/CSRF
        cl.load_settings("session.json")
        print("✅ Sessão carregada com sucesso!")

        # 3. Preparação da Imagem
        print("🔎 Baixando imagem de milho premium...")
        img_url = "https://images.unsplash.com/photo-1551727041-5b347d65b633?q=80&w=1080"
        img_data = requests.get(img_url).content
        with open("post.jpg", "wb") as f:
            f.write(img_data)

        # 4. Inteligência Artificial para Legenda
        print("🤖 Solicitando legenda para a IA...")
        try:
            genai.configure(api_key=GEMINI_KEY)
            model = genai.GenerativeModel('gemini-pro')
            prompt = "Crie uma legenda curta e vendedora para Instagram sobre milho verde premium com emojis."
            legenda = model.generate_content(prompt).text
        except Exception as ia_err:
            print(f"⚠️ Erro na IA: {ia_err}. Usando legenda padrão.")
            legenda = "O melhor milho verde da região! 🌽 #milhopremium #milho"

        # 5. Execução da Postagem
        print("📤 Enviando para o Instagram...")
        # O upload_photo é o método mais estável para contas profissionais
        media = cl.photo_upload("post.jpg", legenda)
        
        if media:
            print(f"✨ SUCESSO ABSOLUTO! Publicação realizada.")
            print(f"🔗 Link do post: https://www.instagram.com/p/{media.code}/")

    except Exception as e:
        print(f"❌ FALHA TÉCNICA NO PROCESSO: {e}")
        # Se o erro for de sessão expirada, o log avisará
        if "login_required" in str(e).lower():
            print("💡 DICA: Sua sessão do Termux expirou. Gere um novo token no celular.")

if __name__ == "__main__":
    robo_milho_premium()
