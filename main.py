import os
import random
import time
from google import genai
from google.genai import types
from instagrapi import Client
from instagrapi.exceptions import ClientError, BadPassword

# --- CONFIGURAÇÕES DE ALTA PERFORMANCE ---
MAX_TENTATIVAS = 3  # Se falhar, tenta 3 vezes antes de desistir
TEMPERATURA_IA = 0.8 # De 0.0 a 1.0 (0.8 é criativo e vendedor)
DELAY_HUMANO = [2, 5] # Espera entre 2 a 5 segundos (Anti-Bloqueio)

def motor_cyber_milho():
    print("🚀 SISTEMA INICIADO: Protocolo 'Cyber-Agro' Ativado...")
    
    # 1. VALIDAÇÃO DE AMBIENTE (FAIL-FAST)
    insta_session = os.environ.get("INSTA_SESSION")
    gemini_key = os.environ.get("GEMINI_KEY")

    if not insta_session or not gemini_key:
        print("❌ CRÍTICO: Credenciais ausentes. Abortando missão.")
        return

    # 2. INICIALIZAÇÃO DOS MOTORES
    try:
        # Configuração IA (Google GenAI SDK Novo)
        client_google = genai.Client(api_key=gemini_key)
        
        # Configuração Instagram
        cl = Client()
        cl.delay_range = DELAY_HUMANO # Simula comportamento humano
        
        # Carregamento de Sessão Segura
        with open("session.json", "w") as f:
            f.write(insta_session)
        cl.load_settings("session.json")
        print("✅ Conectividade: Instagram & Google OK.")
        
    except Exception as e:
        print(f"❌ Falha na Inicialização: {e}")
        return

    # 3. SELEÇÃO DE MÍDIA INTELIGENTE
    pasta = "fotos_postar"
    try:
        arquivos = [f for f in os.listdir(pasta) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.mp4', '.mov'))]
        if not arquivos:
            print("⚠️ ALERTA: Estoque de mídia vazio.")
            return
            
        escolhido = random.choice(arquivos)
        caminho_completo = os.path.join(pasta, escolhido)
        ext = escolhido.lower().split('.')[-1]
        print(f"📦 Mídia Carregada: {escolhido} | Tipo: {ext.upper()}")
        
    except Exception as e:
        print(f"❌ Erro de Sistema de Arquivos: {e}")
        return

    # 4. GERAÇÃO DE CONTEÚDO (IA GENERATIVA COM RETRY)
    print("🧠 Processando neuro-legenda com Gemini 1.5 Flash...")
    legenda_final = "Milho verde de outro mundo! 🌽 #milhopremium" # Backup
    
    for tentativa in range(MAX_TENTATIVAS):
        try:
            # Configuração avançada de prompt para vendas
            prompt_sistema = (
                "Você é um especialista em marketing digital para o agronegócio. "
                "Escreva uma legenda curta (max 2 linhas), urgente e irresistível "
                "para vender milho verde premium hoje. Use 3 emojis."
            )
            
            response = client_google.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt_sistema,
                config=types.GenerateContentConfig(
                    temperature=TEMPERATURA_IA, # Controla a criatividade
                    candidate_count=1
                )
            )
            legenda_final = response.text.strip()
            print("✨ SUCESSO IA: Legenda gerada e validada.")
            break # Sai do loop se der certo
        except Exception as ia_err:
            print(f"⚠️ Tentativa IA {tentativa+1}/{MAX_TENTATIVAS} falhou: {ia_err}")
            time.sleep(2) # Espera 2 segundos antes de tentar de novo

    # 5. UPLOAD DE ALTA PRECISÃO
    print(f"📤 Iniciando transmissão para o Instagram... (Aguarde)")
    try:
        media = None
        if ext in ['mp4', 'mov']:
            # Upload de vídeo
            media = cl.video_upload(caminho_completo, legenda_final)
        else:
            # Upload de foto
            media = cl.photo_upload(caminho_completo, legenda_final)
            
        if media:
            print(f"🏆 MISSÃO CUMPRIDA! Post Online: https://www.instagram.com/p/{media.code}/")
            
            # Opcional: Remover arquivo após postar para não repetir (Descomente se quiser)
            # os.remove(caminho_completo) 
            # print("🗑️ Arquivo removido do estoque.")

    except ClientError as e:
        print(f"❌ Erro API Instagram: {e}")
    except Exception as e:
        print(f"❌ Erro Genérico no Upload: {e}")

if __name__ == "__main__":
    motor_cyber_milho()
