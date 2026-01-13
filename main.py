import os
import shutil
import time
import warnings
from instagrapi import Client
import google.generativeai as genai 

# --- CONFIGURAÇÕES SILENCIOSAS ---
# Silencia avisos de "Deprecated" do Google para manter o log limpo
warnings.simplefilter("ignore")

PASTA_NOVOS = "conteudo_novo"
PASTA_POSTADOS = "conteudo_postado"

def limpar_lixo_thumbnail(arquivo_video):
    """Remove a capa .jpg que o instagrapi gera automaticamente"""
    try:
        nome_base = os.path.basename(arquivo_video)
        caminho_thumb = os.path.join(PASTA_NOVOS, f"{nome_base}.jpg")
        if os.path.exists(caminho_thumb):
            os.remove(caminho_thumb)
    except Exception:
        pass

def motor_elite_final():
    print("🚀 INICIANDO MOTOR DE ELITE (CORREÇÃO DE ERRO DE ARGUMENTO)...")

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
        print(f"❌ Erro na config da IA: {e}")

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

    # 5. Login Instagram (CORRIGIDO)
    cl = Client()
    try:
        # Cria o arquivo temporário de sessão
        with open("session.json", "w") as f:
            f.write(insta_session)
        cl.load_settings("session.json")
        
        # --- AQUI ESTAVA O ERRO ---
        # Antes: cl.get_timeline_feed(amount=1) -> CAUSAVA O ERRO FATAL
        # Agora: cl.get_timeline_feed() -> Sem argumentos, funciona na versão nova
        cl.get_timeline_feed() 
        print("✅ Instagram Conectado (Teste de feed OK).")
        
    except Exception as e:
        print(f"❌ Erro de Login: {e}")
        # Se falhar o login, aborta para não tentar postar sem conta
        return

    # 6. Geração de Legenda
    print("🧠 Gerando legenda com IA...")
    legenda = "Milho Premium! 🌽 #agronegocio" 

    try:
        # Usando o modelo Flash que é rápido e não dá erro 404
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Crie uma legenda curta e engajadora para Instagram sobre milho verde premium. Foco na solução (sabor, saúde ou lucro). Use emojis. Sem aspas. Arquivo: {escolhido}"
        
        response = model.generate_content(prompt)
        
        if response and response.text:
            legenda = response.text.strip()
            print("✅ Legenda criada pela IA com sucesso.")
        else:
            print("⚠️ IA retornou texto vazio.")
            
    except Exception as e:
        print(f"⚠️ Falha na IA ({e}). Usando legenda padrão.")

    # 7. Postagem
    sucesso = False
    try:
        print("📤 Iniciando Upload...")
        if escolhido.lower().endswith(('.mp4', '.mov', '.avi')):
            cl.video_upload(caminho_origem, legenda)
        else:
            cl.photo_upload(caminho_origem, legenda)
        
        print("✨ POSTAGEM REALIZADA COM SUCESSO!")
        sucesso = True
        
        # Limpeza imediata do lixo gerado pelo instagrapi
        if escolhido.lower().endswith(('.mp4', '.mov', '.avi')):
            limpar_lixo_thumbnail(escolhido)

    except Exception as e:
        print(f"❌ Falha no Upload: {e}")

    # 8. Mover Arquivo e Finalizar
    if sucesso:
        destino = os.path.join(PASTA_POSTADOS, escolhido)
        if os.path.exists(destino):
            timestamp = int(time.time())
            destino = os.path.join(PASTA_POSTADOS, f"{timestamp}_{escolhido}")
        
        shutil.move(caminho_origem, destino)
        print(f"🔄 Arquivo movido para '{PASTA_POSTADOS}'.")

if __name__ == "__main__":
    motor_elite_final()
