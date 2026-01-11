import os
import random
from google import genai
from instagrapi import Client

# --- CONFIGURAÇÃO DE ELITE ---
def robo_milho_blindado():
    print("🛡️ Iniciando Protocolo de Auditoria e Postagem...")
    
    insta_session = os.environ.get("INSTA_SESSION")
    gemini_key = os.environ.get("GEMINI_KEY")

    if not insta_session or not gemini_key:
        print("❌ CRÍTICO: Chaves de acesso não encontradas.")
        return

    # 1. Conexão com o Google (Sem forçar versão, deixando o Auto-Detect)
    client_google = genai.Client(api_key=gemini_key)

    # 2. Conexão Instagram
    cl = Client()
    try:
        with open("session.json", "w") as f:
            f.write(insta_session)
        cl.load_settings("session.json")
        print("✅ Conexão Instagram: ESTÁVEL")
    except Exception as e:
        print(f"❌ Erro Instagram: {e}")
        return

    # 3. Seleção de Mídia
    pasta = "fotos_postar"
    try:
        arquivos = [f for f in os.listdir(pasta) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.mp4', '.mov'))]
        if not arquivos:
            print("⚠️ Pasta vazia.")
            return
        escolhido = random.choice(arquivos)
        caminho = os.path.join(pasta, escolhido)
        print(f"📦 Mídia Selecionada: {escolhido}")
    except:
        print("❌ Erro ao ler pasta.")
        return

    # 4. INTELIGÊNCIA ARTIFICIAL (ROTAÇÃO DE MODELOS)
    print("🤖 Iniciando negociação com a IA...")
    
    # Lista de modelos para tentar (do mais rápido para o mais compatível)
    modelos_para_tentar = [
        "gemini-1.5-flash",          # Tenta o rápido primeiro
        "gemini-1.5-flash-latest",   # Tenta a versão latest
        "gemini-1.5-pro",            # Tenta o pro (mais potente)
        "gemini-pro"                 # Tenta o clássico (quase impossível falhar)
    ]
    
    legenda_final = "O melhor milho verde da região! 🌽 #milhopremium"
    sucesso_ia = False

    for modelo in modelos_para_tentar:
        try:
            print(f"🔄 Tentando conectar com modelo: {modelo}...")
            response = client_google.models.generate_content(
                model=modelo,
                contents="Crie uma legenda curta, muito vendedora e animada para Instagram de venda de milho verde. Use emojis."
            )
            legenda_final = response.text
            sucesso_ia = True
            print(f"✅ SUCESSO! Conectado ao modelo: {modelo}")
            break # Se funcionou, para de tentar os outros
        except Exception as e:
            # Se der erro 404, ele apenas avisa e tenta o próximo da lista
            print(f"⚠️ Falha no {modelo}: {str(e)[:50]}...") # Mostra só o começo do erro
            continue

    if not sucesso_ia:
        print("⚠️ Todos os modelos falharam. Usando legenda de contingência.")

    # 5. Upload
    print(f"📝 Legenda definida: {legenda_final[:30]}...")
    try:
        ext = escolhido.lower().split('.')[-1]
        if ext in ['mp4', 'mov']:
            cl.video_upload(caminho, legenda_final)
        else:
            cl.photo_upload(caminho, legenda_final)
        print("✨ OPERAÇÃO CONCLUÍDA COM SUCESSO.")
    except Exception as e:
        print(f"❌ Falha no Upload: {e}")

if __name__ == "__main__":
    robo_milho_blindado()
