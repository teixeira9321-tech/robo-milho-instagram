import os
import random
import requests
from instagrapi import Client

def motor_scanner_automatico():
    print("🛰️ INICIANDO PROTOCOLO SCANNER (AUTO-DESCOBERTA)...")
    
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

    # 2. Mídia
    pasta = "fotos_postar"
    try:
        arquivos = [f for f in os.listdir(pasta) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.mp4', '.mov'))]
        if not arquivos: return
        escolhido = random.choice(arquivos)
        caminho = os.path.join(pasta, escolhido)
        print(f"📦 Mídia: {escolhido}")
    except: return

    # 3. SCANNER DE MODELOS (O PULO DO GATO)
    print("🔍 Perguntando ao Google quais modelos sua chave libera...")
    legenda_final = "Milho verde premium! 🌽 #milho"
    
    try:
        # Passo A: Listar modelos disponíveis para esta chave
        url_list = f"https://generativelanguage.googleapis.com/v1beta/models?key={gemini_key}"
        r_list = requests.get(url_list, timeout=10)
        
        modelo_escolhido = None
        
        if r_list.status_code == 200:
            dados = r_list.json()
            if 'models' in dados:
                # Procura o primeiro modelo que gera texto
                for m in dados['models']:
                    print(f"   -> Encontrado: {m['name']}")
                    if 'generateContent' in m.get('supportedGenerationMethods', []):
                        modelo_escolhido = m['name'] # Ex: models/gemini-1.5-flash
                        print(f"🎯 ALVO TRAVADO: Usaremos {modelo_escolhido}")
                        break
            else:
                print("⚠️ A chave funciona, mas a lista de modelos veio vazia.")
        else:
            print(f"❌ Erro ao listar modelos: {r_list.status_code} (Verifique se a chave é do AI Studio)")

        # Passo B: Gerar legenda usando o modelo encontrado (ou contingência)
        if modelo_escolhido:
            # A URL já vem no formato 'models/nome', então montamos direto
            url_gen = f"https://generativelanguage.googleapis.com/v1beta/{modelo_escolhido}:generateContent?key={gemini_key}"
            
            payload = {"contents": [{"parts": [{"text": "Crie uma legenda curta e vendedora com emojis para milho verde."}]}]}
            headers = {'Content-Type': 'application/json'}
            
            r_gen = requests.post(url_gen, headers=headers, json=payload, timeout=10)
            if r_gen.status_code == 200:
                legenda_final = r_gen.json()['candidates'][0]['content']['parts'][0]['text']
                print("✅ SUCESSO! A IA gerou a legenda.")
            else:
                print(f"⚠️ Erro na geração: {r_gen.status_code}")
        else:
            print("⚠️ Nenhum modelo compatível encontrado. Usando reserva.")

    except Exception as e:
        print(f"❌ Erro crítico no Scanner: {e}")

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
    motor_scanner_automatico()
