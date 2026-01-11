import os
import random
import time
import requests 
from instagrapi import Client

def motor_http_universal_corrigido():
    print("🌍 INICIANDO PROTOCOLO UNIVERSAL (HTTP REST)...")
    
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

    # 3. INTELIGÊNCIA ARTIFICIAL (CORRIGIDA)
    print("🤖 Chamando o Google via HTTP Direto...")
    
    legenda_final = "O melhor milho verde da região! 🌽 #milhopremium"
    
    # Tenta Beta (Flash) e depois Produção (Pro)
    endpoints = [
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}",
        f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={gemini_key}"
    ]

    payload = {
        "contents": [{
            "parts": [{"text": "Crie uma legenda curta, vendedora e com emojis para vender milho verde premium."}]
        }]
    }
    headers = {'Content-Type': 'application/json'}

    sucesso_ia = False
    for url in endpoints:
        try:
            modelo_nome = url.split('models/')[1].split(':')[0]
            print(f"🔄 Tentando conectar em: {modelo_nome}...")
            
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            
            if response.status_code == 200:
                dados = response.json()
                try:
                    legenda_final = dados['candidates'][0]['content']['parts'][0]['text']
                    print("✅ SUCESSO! A IA respondeu via HTTP.")
                    sucesso_ia = True
                    break 
                except KeyError: # <--- O ERRO ESTAVA AQUI, AGORA ESTÁ CORRIGIDO
                    print("⚠️ JSON retornou mas sem texto.")
            else:
                print(f"⚠️ Falha HTTP {response.status_code}: {response.text[:100]}...")
                
        except Exception as e:
            print(f"⚠️ Erro de conexão: {e}")

    # 4. Upload
    print(f"📤 Postando...")
    try:
        ext = escolhido.lower().split('.')[-1]
        if ext in ['mp4', 'mov']:
            cl.video_upload(caminho, legenda_final)
        else:
            cl.photo_upload(caminho, legenda_final)
        print("✨ OPERAÇÃO FINALIZADA.")
    except Exception as e:
        print(f"❌ Erro no Upload: {e}")

if __name__ == "__main__":
    motor_http_universal_corrigido()
