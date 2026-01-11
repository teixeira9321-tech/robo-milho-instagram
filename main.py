import os
import random
import google.generativeai as genai
from instagrapi import Client
from instagrapi.types import StoryMedia

# Configurações de ambiente
SESSION_JSON = os.environ.get("INSTA_SESSION")
GEMINI_KEY = os.environ.get("GEMINI_KEY")

def robo_milho_premium_v3():
    if not SESSION_JSON:
        print("❌ ERRO CRÍTICO: Secret INSTA_SESSION não configurado.")
        return

    cl = Client()
    
    try:
        # 1. Autenticação via Sessão (Alta Performance)
        with open("session.json", "w") as f:
            f.write(SESSION_JSON)
        cl.load_settings("session.json")
        print("✅ Autenticação realizada via Token Termux.")

        # 2. Seleção Inteligente de Mídia (Fotos ou Vídeos)
        pasta = "fotos_postar"
        # Filtra arquivos suportados
        arquivos = [f for f in os.listdir(pasta) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.mp4', '.mov'))]
        
        if not arquivos:
            print(f"❌ ERRO: A pasta '{pasta}' está vazia.")
            return
        
        escolhido = random.choice(arquivos)
        caminho = os.path.join(pasta, escolhido)
        ext = escolhido.lower().split('.')[-1]
        print(f"📦 Mídia selecionada: {escolhido}")

        # 3. Inteligência Artificial (Modelo 1.5 Flash - Alta Velocidade)
        print("🤖 Gerando legenda estratégica...")
        try:
            genai.configure(api_key=GEMINI_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = "Crie uma legenda curta e irresistível para vender milho verde premium. Use emojis."
            legenda = model.generate_content(prompt).text
        except Exception as ia_err:
            print(f"⚠️ IA indisponível ({ia_err}). Usando legenda reserva.")
            legenda = "O melhor milho verde da região, fresquinho todo dia! 🌽 #milhopremium"

        # 4. Upload Diferenciado (Foto vs Vídeo)
        print(f"📤 Iniciando upload de {ext.upper()}...")
        
        if ext in ['mp4', 'mov']:
            # Lógica para Vídeo (Reels/Feed)
            media = cl.video_upload(caminho, legenda)
        else:
            # Lógica para Foto
            media = cl.photo_upload(caminho, legenda)
        
        if media:
            print(f"✨ SUCESSO! Post realizado com ID: {media.pk}")
            print(f"🔗 Link: https://www.instagram.com/p/{media.code}/")

    except Exception as e:
        print(f"❌ FALHA NO MOTOR: {e}")

if __name__ == "__main__":
    robo_milho_premium_v3()
