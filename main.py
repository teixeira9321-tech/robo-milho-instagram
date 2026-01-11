import os
import random
import time
import shutil
from google import genai
from instagrapi import Client
from instagrapi.exceptions import ClientError

# --- CONFIGURAÇÕES DE ALTA PERFORMANCE ---
PASTA_MIDIA = "fotos_postar"
ARQUIVO_SESSAO = "session.json"
MODELO_IA = "gemini-1.5-flash" # Modelo de alta velocidade

def limpar_cache_temporario():
    """Remove arquivos residuais para manter o servidor leve."""
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".jpg.remove_me") or file.endswith(".mp4.jpg"):
                try: os.remove(os.path.join(root, file))
                except: pass

def robo_milho_premium_v4():
    print("🚀 Iniciando Motor de Alta Performance...")
    
    # 1. VALIDAÇÃO DE INFRAESTRUTURA
    insta_session = os.environ.get("INSTA_SESSION")
    gemini_key = os.environ.get("GEMINI_KEY")

    if not insta_session or not gemini_key:
        print("❌ CRÍTICO: Secrets do GitHub não encontrados!")
        return

    # 2. INICIALIZAÇÃO DE CLIENTES (SDK NOVO 2026)
    try:
        google_client = genai.Client(api_key=gemini_key)
        cl = Client()
        cl.delay_range = [2, 5] # Delay humano para evitar bloqueios
        
        with open(ARQUIVO_SESSAO, "w") as f:
            f.write(insta_session)
        cl.load_settings(ARQUIVO_SESSAO)
        print("✅ Autenticação Instagram: VALIDADA")
    except Exception as e:
        print(f"❌ Erro na Inicialização: {e}")
        return

    # 3. SELEÇÃO INTELIGENTE DE MÍDIA
    try:
        if not os.path.exists(PASTA_MIDIA):
            os.makedirs(PASTA_MIDIA)
            
        arquivos = [f for f in os.listdir(PASTA_MIDIA) 
                   if f.lower().endswith(('.jpg', '.jpeg', '.png', '.mp4', '.mov'))]
        
        if not arquivos:
            print(f"⚠️ Pasta {PASTA_MIDIA} vazia. Abortando ciclo.")
            return

        escolhido = random.choice(arquivos)
        caminho_completo = os.path.join(PASTA_MIDIA, escolhido)
        ext = escolhido.lower().split('.')[-1]
        print(f"📦 Mídia Selecionada: {escolhido} (Tipo: {ext.upper()})")
    except Exception as e:
        print(f"❌ Erro ao acessar arquivos: {e}")
        return

    # 4. INTELIGÊNCIA ARTIFICIAL (ALTA TECNOLOGIA)
    print("🤖 Gerando legenda estratégica via Gemini 1.5 Flash...")
    try:
        prompt = (
            "Atue como um especialista em marketing digital para agronegócio. "
            "Crie uma legenda curta, altamente vendedora e com emojis para um post "
            "de milho verde premium. Foque em frescor e sabor."
        )
        response = google_client.models.generate_content(
            model=MODELO_IA,
            contents=prompt
        )
        legenda = response.text.strip()
        print("📝 Legenda gerada com sucesso.")
    except Exception as ia_err:
        print(f"⚠️ Falha na IA: {ia_err}. Ativando Legenda de Contingência.")
        legenda = "O milho verde mais fresquinho e selecionado da região! 🌽 Peça já o seu. #milhopremium #agro"

    # 5. EXECUÇÃO DO UPLOAD (BLINDADO)
    try:
        print(f"📤 Enviando {ext.upper()} para o Instagram...")
        if ext in ['mp4', 'mov']:
            # Otimizado para Reels/Vídeo de Feed
            media = cl.video_upload(caminho_completo, legenda)
        else:
            # Otimizado para Fotos
            media = cl.photo_upload(caminho_completo, legenda)
        
        if media:
            print(f"✨ SUCESSO! Post publicado: https://www.instagram.com/p/{media.code}/")
    except ClientError as ce:
        print(f"❌ Erro de API do Instagram: {ce}")
    except Exception as e:
        print(f"❌ Falha inesperada no upload: {e}")
    finally:
        limpar_cache_temporario()
        print("🧹 Limpeza de sistema concluída.")

if __name__ == "__main__":
    # Roda o ciclo
    robo_milho_premium_v4()
