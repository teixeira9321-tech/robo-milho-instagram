import os
import random
import time
from google import genai
from google.genai import types
from instagrapi import Client
from instagrapi.exceptions import ClientError

# --- CONFIGURAÇÕES DE ALTA PERFORMANCE ---
MAX_TENTATIVAS = 3
TEMPERATURA_IA = 0.85
DELAY_HUMANO = [2, 5]

def motor_cyber_milho_v2():
    print("🚀 SISTEMA V2: Iniciando Protocolo de Correção de Rota...")
    
    insta_session = os.environ.get("INSTA_SESSION")
    gemini_key = os.environ.get("GEMINI_KEY")

    if not insta_session or not gemini_key:
        print("❌ CRÍTICO: Credenciais ausentes.")
        return

    try:
        # --- A CORREÇÃO MÁGICA ESTÁ AQUI EMBAIXO ---
        # Adicionei http_options={'api_version': 'v1'} para sair do modo Beta
        client_google = genai.Client(
            api_key=gemini_key,
            http_options={'api_version': 'v1'} 
        )
        
        cl = Client()
        cl.delay_range = DELAY_HUMANO
        
        with open("session.json", "w") as f:
            f.write(insta_session)
        cl.load_settings("session.json")
        print("✅ Conectividade: Rota V1 (Produção) Ativada.")
        
    except Exception as e:
        print(f"❌ Falha na Inicialização: {e}")
        return

    # SELEÇÃO DE MÍDIA
    pasta = "fotos_postar"
    try:
        arquivos = [f for f in os.listdir(pasta) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.mp4', '.mov'))]
        if not arquivos:
            print("⚠️ Estoque vazio.")
            return
        escolhido = random.choice(arquivos)
        caminho_completo = os.path.join(pasta, escolhido)
        ext = escolhido.lower().split('.')[-1]
        print(f"📦 Mídia: {escolhido}")
    except:
        return

    # GERAÇÃO DE CONTEÚDO (IA)
    print("🧠 Solicitando legenda na Rota V1...")
    legenda_final = "Milho verde premium! 🌽 Sabor inigualável. #milho"
    
    for tentativa in range(MAX_TENTATIVAS):
        try:
            prompt = "Crie uma legenda curta e muito vendedora para Instagram de milho verde. Use emojis."
            
            # Chamada otimizada para V1
            response = client_google.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=TEMPERATURA_IA,
                    candidate_count=1
                )
            )
            legenda_final = response.text.strip()
            print("✨ SUCESSO ABSOLUTO: A IA respondeu!")
            break 
        except Exception as ia_err:
            print(f"⚠️ Tentativa {tentativa+1} falhou: {ia_err}")
            time.sleep(1)

    # UPLOAD
    print(f"📤 Postando...")
    try:
        if ext in ['mp4', 'mov']:
            media = cl.video_upload(caminho_completo, legenda_final)
        else:
            media = cl.photo_upload(caminho_completo, legenda_final)
            
        if media:
            print(f"🏆 POST NO AR: https://www.instagram.com/p/{media.code}/")
    except Exception as e:
        print(f"❌ Erro Upload: {e}")

if __name__ == "__main__":
    motor_cyber_milho_v2()
