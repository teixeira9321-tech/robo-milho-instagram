import os
import shutil
import requests
import time
from instagrapi import Client

# --- CONFIGURAÇÕES ---
PASTA_NOVOS = "conteudo_novo"
PASTA_POSTADOS = "conteudo_postado"

def motor_elite_v2():
    print("🚀 INICIANDO MOTOR DE ELITE V2...")

    # 1. Verificação de Ambiente
    insta_session = os.environ.get("INSTA_SESSION")
    gemini_key = os.environ.get("GEMINI_KEY")

    if not insta_session or not gemini_key:
        print("❌ ERRO: Secrets (Chaves) não configuradas no GitHub.")
        return

    # 2. Criação de Pastas (Garante que existem)
    for pasta in [PASTA_NOVOS, PASTA_POSTADOS]:
        if not os.path.exists(pasta):
            os.makedirs(pasta)
            print(f"📂 Pasta verificada/criada: {pasta}")

    # 3. Seleção de Mídia
    extensoes = ('.jpg', '.jpeg', '.png', '.mp4', '.mov', '.avi')
    # Lista arquivos e ordena para pegar sempre o primeiro
    arquivos = sorted([f for f in os.listdir(PASTA_NOVOS) if f.lower().endswith(extensoes)])

    if not arquivos:
        print(f"📭 Pasta '{PASTA_NOVOS}' vazia. Nada para postar.")
        return

    escolhido = arquivos[0]
    caminho_origem = os.path.join(PASTA_NOVOS, escolhido)
    print(f"📦 Mídia da vez: {escolhido}")

    # 4. Login Instagram (Blindado)
    cl = Client()
    try:
        # Tenta criar o arquivo de sessão com o que tem na Secret
        with open("session.json", "w") as f:
            f.write(insta_session)
        cl.load_settings("session.json")
        cl.login(os.environ.get("INSTA_USER", ""), os.environ.get("INSTA_PASS", "")) # Fallback se tiver user/pass
        print("✅ Instagram Conectado.")
    except Exception as e:
        print(f"⚠️ Aviso de Login: {e}")
        # Se der erro no load, tenta seguir se a sessão ainda for válida na memória
        pass

    # 5. Geração de Legenda (Gemini 1.5 Flash)
    print("🧠 Criando legenda...")
    legenda = "Milho Premium! 🌽 #agronegocio" # Legenda padrão
    
    prompt = f"Crie uma legenda curta, atraente e vendedora para Instagram sobre milho verde premium. Use emojis. Sem aspas. Foco: Sabor e Qualidade. Arquivo: {escolhido}"

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        req = requests.post(url, json=payload, headers={'Content-Type': 'application/json'}, timeout=10)
        
        if req.status_code == 200:
            legenda = req.json()['candidates'][0]['content']['parts'][0]['text'].strip()
            print("✅ Legenda IA Gerada.")
        else:
            print(f"⚠️ Erro IA: {req.status_code} - Usando padrão.")
    except Exception as e:
        print(f"⚠️ Erro Conexão IA: {e}")

    # 6. Postagem
    sucesso = False
    try:
        print("📤 Postando...")
        if escolhido.lower().endswith(('.mp4', '.mov', '.avi')):
            cl.video_upload(caminho_origem, legenda)
        else:
            cl.photo_upload(caminho_origem, legenda)
        print("✨ POSTADO COM SUCESSO!")
        sucesso = True
    except Exception as e:
        print(f"❌ Erro no Upload: {e}")

    # 7. Mover Arquivo (A parte mais importante)
    if sucesso:
        destino = os.path.join(PASTA_POSTADOS, escolhido)
        if os.path.exists(destino):
            # Se já existe lá, renomeia para não dar erro
            timestamp = int(time.time())
            destino = os.path.join(PASTA_POSTADOS, f"{timestamp}_{escolhido}")
        
        shutil.move(caminho_origem, destino)
        print(f"🔄 Arquivo movido para '{PASTA_POSTADOS}'.")

if __name__ == "__main__":
    motor_elite_v2()
