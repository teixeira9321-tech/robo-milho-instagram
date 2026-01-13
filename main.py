import os
import shutil
import time
import warnings
from instagrapi import Client
import google.generativeai as genai 

# --- CONFIGURAÇÕES GERAIS ---
warnings.simplefilter("ignore") # Limpa logs sujos
PASTA_NOVOS = "conteudo_novo"
PASTA_POSTADOS = "conteudo_postado"

def limpar_lixo_thumbnail(arquivo_video):
    """Remove a capa .jpg que o instagrapi gera"""
    try:
        nome_base = os.path.basename(arquivo_video)
        caminho_thumb = os.path.join(PASTA_NOVOS, f"{nome_base}.jpg")
        if os.path.exists(caminho_thumb):
            os.remove(caminho_thumb)
    except Exception:
        pass

def gerar_legenda_blindada(genai_client, prompt_text):
    """
    Tenta vários modelos em sequência até um funcionar.
    Isso resolve o erro 404 definitivamente.
    """
    # Lista de modelos por ordem de preferência (do melhor para o mais estável)
    modelos_para_tentar = [
        'gemini-1.5-flash',       # O mais rápido (Apelido)
        'gemini-1.5-flash-001',   # Versão congelada/estável (Menos chance de 404)
        'gemini-1.5-pro',         # Versão Pro
        'gemini-pro'              # O clássico (Último recurso, quase nunca falha)
    ]

    for nome_modelo in modelos_para_tentar:
        try:
            print(f"🔄 Tentando conectar no modelo: {nome_modelo}...")
            model = genai_client.GenerativeModel(nome_modelo)
            response = model.generate_content(prompt_text)
            
            if response and response.text:
                return response.text.strip() # Sucesso! Retorna a legenda
                
        except Exception as e:
            # Se der erro 404 ou qualquer outro, apenas avisa e tenta o próximo da lista
            if "404" in str(e):
                print(f"⚠️ Modelo {nome_modelo} não encontrado (404). Tentando o próximo...")
            else:
                print(f"⚠️ Erro no modelo {nome_modelo}: {e}")
            continue # Pula para o próximo loop

    # Se chegou aqui, todos falharam
    return None

def motor_elite_final():
    print("🚀 INICIANDO MOTOR DE ELITE (SISTEMA ANTI-404)...")

    # 1. Verificação de Ambiente
    insta_session = os.environ.get("INSTA_SESSION")
    gemini_key = os.environ.get("GEMINI_KEY")

    if not insta_session or not gemini_key:
        print("❌ ERRO CRÍTICO: Secrets não configuradas.")
        return

    # 2. Configuração da IA
    try:
        genai.configure(api_key=gemini_key)
    except Exception as e:
        print(f"❌ Erro Config IA: {e}")

    # 3. Verificação de Pastas
    for pasta in [PASTA_NOVOS, PASTA_POSTADOS]:
        if not os.path.exists(pasta):
            os.makedirs(pasta)

    # 4. Seleção de Mídia
    extensoes = ('.mp4', '.mov', '.avi', '.jpg', '.png')
    arquivos = sorted([f for f in os.listdir(PASTA_NOVOS) if f.lower().endswith(extensoes)])

    if not arquivos:
        print(f"📭 Nada para postar em '{PASTA_NOVOS}'.")
        return

    escolhido = arquivos[0]
    caminho_origem = os.path.join(PASTA_NOVOS, escolhido)
    print(f"📦 Mídia selecionada: {escolhido}")

    # 5. Login Instagram (Modo Seguro)
    cl = Client()
    try:
        with open("session.json", "w") as f:
            f.write(insta_session)
        cl.load_settings("session.json")
        # Sem timeline_feed() para evitar erros de versão da API, apenas confia na session
        print("✅ Instagram: Sessão carregada.")
    except Exception as e:
        print(f"❌ Erro de Login: {e}")
        return

    # 6. Geração de Legenda (Lógica Blindada)
    print("🧠 Iniciando protocolo de IA...")
    legenda_final = "Milho Premium! 🌽 #agronegocio #milho #qualidade" # Backup final

    prompt = f"Crie uma legenda curta, viral e apetitosa para Instagram sobre milho verde premium. Foco na solução e sabor. Use emojis. Sem aspas. Arquivo: {escolhido}"

    # Chama a função que tenta vários modelos
    resultado_ia = gerar_legenda_blindada(genai, prompt)
    
    if resultado_ia:
        legenda_final = resultado_ia
        print("✅ SUCESSO: Legenda gerada pela IA.")
    else:
        print("⚠️ ALERTA: Todos os modelos falharam. Usando legenda padrão.")

    # 7. Postagem
    sucesso = False
    try:
        print(f"📤 Postando: {escolhido}...")
        if escolhido.lower().endswith(('.mp4', '.mov', '.avi')):
            cl.video_upload(caminho_origem, legenda_final)
        else:
            cl.photo_upload(caminho_origem, legenda_final)
        
        print("✨ POSTAGEM REALIZADA COM SUCESSO!")
        sucesso = True
        
        if escolhido.lower().endswith(('.mp4', '.mov', '.avi')):
            limpar_lixo_thumbnail(escolhido)

    except Exception as e:
        print(f"❌ Falha no Upload: {e}")

    # 8. Mover e Finalizar
    if sucesso:
        destino = os.path.join(PASTA_POSTADOS, escolhido)
        if os.path.exists(destino):
            timestamp = int(time.time())
            destino = os.path.join(PASTA_POSTADOS, f"{timestamp}_{escolhido}")
        
        shutil.move(caminho_origem, destino)
        print(f"🔄 Arquivo movido para '{PASTA_POSTADOS}'.")

if __name__ == "__main__":
    motor_elite_final()
