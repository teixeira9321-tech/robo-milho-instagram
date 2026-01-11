import os
import random
import google.generativeai as genai
from instagrapi import Client

# Configurações de ambiente
SESSION_JSON = os.environ.get("INSTA_SESSION")
GEMINI_KEY = os.environ.get("GEMINI_KEY")

def robo_milho_final():
    if not SESSION_JSON or not GEMINI_KEY:
        print("❌ ERRO: Verifique se os Secrets (SESSION e KEY) estão configurados.")
        return

    cl = Client()
    
    try:
        # 1. Autenticação via Sessão do Celular (Samsung A03)
        with open("session.json", "w") as f:
            f.write(SESSION_JSON)
        cl.load_settings("session.json")
        print("✅ Sessão validada via Token.")

        # 2. Seleção de Mídia (Pasta fotos_postar)
        pasta = "fotos_postar"
        arquivos = [f for f in os.listdir(pasta) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.mp4', '.mov'))]
        
        if not arquivos:
            print(f"❌ ERRO: A pasta '{pasta}' está vazia.")
            return
        
        escolhido = random.choice(arquivos)
        caminho = os.path.join(pasta, escolhido)
        ext = escolhido.lower().split('.')[-1]
        print(f"📦 Mídia selecionada: {escolhido}")

        # 3. Inteligência Artificial (Modelo Estável)
        print("🤖 Gerando legenda estratégica...")
        try:
            genai.configure(api_key=GEMINI_KEY)
            # Usando o modelo generativo padrão para máxima compatibilidade
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = "Crie uma legenda curta, vendedora e animada para Instagram sobre milho verde premium. Use emojis."
            legenda = model.generate_content(prompt).text
        except Exception as ia_err:
            print(f"⚠️ Erro na IA: {ia_err}. Usando reserva.")
            legenda = "O milho verde mais fresquinho e saboroso da região! 🌽 #milhopremium"

        # 4. Upload Inteligente (Foto ou Vídeo)
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
    robo_milho_final()
