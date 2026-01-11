import os
import random
import requests
from instagrapi import Client

def motor_ai_studio_final():
    print("🚀 INICIANDO PROTOCOLO AI STUDIO...")
    
    insta_session = os.environ.get("INSTA_SESSION")
    gemini_key = os.environ.get("GEMINI_KEY")

    if not insta_session or not gemini_key:
        print("❌ CRÍTICO: Chaves não encontradas.")
        return

    # 1. Instagram
    cl = Client()
    try:
        with open("session.json", "w") as f:
            f.write(insta_session)
        cl.load_settings("session.json")
        print("✅ Instagram: Conectado.")
    except Exception as e:
        print(f"❌ Erro Instagram: {e}")
        return

    # 2. Seleção de Mídia
    pasta = "fotos_postar"
    try:
        arquivos = [f for f in os.listdir(pasta) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.mp4', '.mov'))]
        if not arquivos:
            print("⚠️ Pasta vazia.")
            return
        escolhido = random.choice(arquivos)
        caminho = os.path.join(pasta, escolhido)
        print(f"📦 Mídia: {escolhido}")
    except:
        return

    # 3. INTELIGÊNCIA ARTIFICIAL (Compatível com AI Studio)
    print("🤖 Testando modelos disponíveis na sua chave...")
    
    legenda_final = "O milho verde mais saboroso da região! 🌽 #milhopremium"
    
    # O AI Studio costuma liberar o 'gemini-1.5-flash' na porta v1beta
    modelos = [
        "gemini-1.5-flash",
        "gemini-1.5-flash-latest",
        "gemini-pro"
    ]

    sucesso = False
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts": [{"text": "Crie uma legenda curta, vendedora e com emojis para milho verde."}]}]
    }

    for modelo in modelos:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={gemini_key}"
        try:
            print(f"🔄 Tentando {modelo}...", end=" ")
            r = requests.post(url, headers=headers, json=payload, timeout=10)
            if r.status_code == 200:
                legenda_final = r.json()['candidates'][0]['content']['parts'][0]['text']
                print("✅ SUCESSO! Conectado.")
                sucesso = True
                break
            else:
                print(f"❌ ({r.status_code})")
        except:
            print("❌ Erro conexão")

    if not sucesso:
        print("⚠️ IA não respondeu. Usando legenda padrão.")

    # 4. Upload
    print(f"📤 Postando...")
    try:
        ext = escolhido.lower().split('.')[-1]
        if ext in ['mp4', 'mov']:
            cl.video_upload(caminho, legenda_final)
        else:
            cl.photo_upload(caminho, legenda_final)
        print("✨ OPERAÇÃO CONCLUÍDA.")
    except Exception as e:
        print(f"❌ Erro Upload: {e}")

if __name__ == "__main__":
    motor_ai_studio_final()
