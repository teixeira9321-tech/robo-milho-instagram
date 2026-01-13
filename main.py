import os
import shutil
import time
from instagrapi import Client
import google.generativeai as genai # Biblioteca Oficial (Mais estável)

# --- CONFIGURAÇÕES ---
PASTA_NOVOS = "conteudo_novo"
PASTA_POSTADOS = "conteudo_postado"

def limpar_lixo_thumbnail(arquivo_video):
    """Remove a capa .jpg que o instagrapi gera automaticamente"""
    try:
        nome_base = os.path.basename(arquivo_video)
        caminho_thumb = os.path.join(PASTA_NOVOS, f"{nome_base}.jpg")
        if os.path.exists(caminho_thumb):
            os.remove(caminho_thumb)
            print(f"🧹 Lixo removido: {caminho_thumb}")
    except Exception as e:
        print(f"⚠️ Não foi possível limpar thumbnail: {e}")

def motor_elite_final():
    print("🚀 INICIANDO MOTOR DE ELITE (VERSÃO DEFINITIVA)...")

    # 1. Verificação de Ambiente
    insta_session = os.environ.get("INSTA_SESSION")
    gemini_key = os.environ.get("GEMINI_KEY")

    if not insta_session or not gemini_key:
        print("❌ ERRO CRÍTICO: Secrets não configuradas.")
        return

    # 2. Configuração da IA (Via Biblioteca Oficial)
    # Isso resolve o erro 404 para sempre
    try:
        genai.configure(api_key=gemini_key)
        # Configuração de segurança para evitar bloqueios de conteúdo inofensivo
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 1024,
        }
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

    # 5. Login Instagram (Limpo)
    cl = Client()
    try:
        # Cria o arquivo temporário de sessão
        with open("session.json", "w") as f:
            f.write(insta_session)
        cl.load_settings("session.json")
        
        # Teste rápido de validade (opcional, mas bom pra log)
        cl.get_timeline_feed(amount=1) 
        print("✅ Instagram Conectado (Sessão Válida).")
    except Exception as e:
        print(f"❌ Erro de Login (Sessão Inválida ou Expirada): {e}")
        # Não tentamos login com senha aqui para evitar o erro "Both username..."
        return

    # 6. Geração de Legenda (Sem erro 404)
    print("🧠 Gerando legenda com IA...")
    legenda = "Milho Premium! 🌽 #agronegocio" # Fallback

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Crie uma legenda curta e engajadora para Instagram sobre milho verde premium. Foco na solução (sabor, saúde ou lucro). Use emojis. Sem aspas. Arquivo: {escolhido}"
        
        response = model.generate_content(prompt)
        
        if response.text:
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
        if chosen.lower().endswith(('.mp4', '.mov', '.avi')):
            limpar_lixo_thumbnail(escolhido)

    except Exception as e:
        print(f"❌ Falha no Upload: {e}")

    # 8. Mover Arquivo e Finalizar
    if sucesso:
        destino = os.path.join(PASTA_POSTADOS, escolhido)
        # Evita sobrescrever se já existir
        if os.path.exists(destino):
            timestamp = int(time.time())
            destino = os.path.join(PASTA_POSTADOS, f"{timestamp}_{escolhido}")
        
        shutil.move(caminho_origem, destino)
        print(f"🔄 Arquivo movido para '{PASTA_POSTADOS}'.")

if __name__ == "__main__":
    motor_elite_final()
