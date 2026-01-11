import os
import random
import google.generativeai as genai
from instagrapi import Client

# Configurações de ambiente
SESSION_JSON = os.environ.get("INSTA_SESSION")
GEMINI_KEY = os.environ.get("GEMINI_KEY")

def robo_milho_premium_final():
    if not SESSION_JSON or not GEMINI_KEY:
        print("❌ ERRO: Secrets não configurados corretamente.")
        return

    cl = Client()
    
    try:
        # 1. Autenticação via Sessão do Termux
        with open("session.json", "w") as f:
            f.write(SESSION_JSON)
        cl.load_settings("session.json")
        print("✅ Sessão validada via Token Termux.")

        # 2. Seleção de Mídia Real (fotos_postar)
        pasta = "fotos_postar"
        arquivos = [f for f in os.listdir(pasta) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.mp4', '.mov'))]
        
        if not arquivos:
            print(f"❌ ERRO: Pasta '{pasta}' vazia.")
            return
        
        escolhido = random.choice(arquivos)
        caminho = os.path.join(pasta, escolhido)
        ext = escolhido.lower().split('.')[-1]
        print(f"📦 Mídia selecionada: {escolhido}")

        # 3. Inteligência Artificial (Ajuste para Evitar o Erro 404)
        print("🤖 Gerando legenda estratégica...")
        try:
            genai.configure(api_key=GEMINI_KEY)
            # MUDANÇA CRÍTICA: Adicionado o sufixo -latest para estabilidade
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            prompt = "Crie uma legenda curta, vendedora e criativa para um post de milho verde premium. Use emojis."
            legenda = model.generate_content(prompt).text
        except Exception as ia_err:
            print(f"⚠️ Erro na IA: {ia_err}. Usando legenda reserva.")
            legenda = "O melhor milho verde da região, fresquinho todo dia! 🌽 #milhopremium"

        # 4. Upload de Alta Performance
        if ext in ['mp4', 'mov']:
            print("🎥 Postando Vídeo...")
            media = cl.video_upload(caminho, legenda)
        else:
            print("📸 Postando Foto...")
            media = cl.photo_upload(caminho, legenda)
        
        if media:
            print(f"✨ SUCESSO! Post realizado: {media.code}")

    except Exception as e:
        print(f"❌ FALHA NO MOTOR: {e}")

if __name__ == "__main__":
    robo_milho_premium_final()
