import os
import random
from google import genai
from instagrapi import Client

def robo_milho_definitivo():
    insta_session = os.environ.get("INSTA_SESSION")
    gemini_key = os.environ.get("GEMINI_KEY")

    # Configuração de Elite do Google (Forçando v1 estável)
    client_google = genai.Client(
        api_key=gemini_key,
        http_options={'api_version': 'v1'} 
    )
    cl = Client()
    
    try:
        with open("session.json", "w") as f:
            f.write(insta_session)
        cl.load_settings("session.json")
        print("✅ Conexão Instagram: OK")

        # Seleção de Mídia
        pasta = "fotos_postar"
        arquivos = [f for f in os.listdir(pasta) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.mp4', '.mov'))]
        escolhido = random.choice(arquivos)
        caminho = os.path.join(pasta, escolhido)
        print(f"📦 Mídia: {escolhido}")

        # IA com Força Total
        print("🤖 Gerando legenda estratégica...")
        try:
            # Note o modelo simples 'gemini-1.5-flash'
            response = client_google.models.generate_content(
                model="gemini-1.5-flash",
                contents="Crie uma legenda vendedora para milho verde premium. Use emojis."
            )
            legenda = response.text
        except Exception as ia_err:
            print(f"⚠️ IA ainda em ajuste: {ia_err}")
            legenda = "O melhor milho verde da região! 🌽 #milhopremium"

        # Postagem
        ext = escolhido.lower().split('.')[-1]
        if ext in ['mp4', 'mov']:
            cl.video_upload(caminho, legenda)
        else:
            cl_insta.photo_upload(caminho, legenda)
        
        print(f"✨ SUCESSO! Post realizado.")

    except Exception as e:
        print(f"❌ FALHA: {e}")

if __name__ == "__main__":
    robo_milho_definitivo()
