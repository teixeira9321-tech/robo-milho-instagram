import os
import random
import requests
from instagrapi import Client

def motor_corrigido_sem_papo():
    print("🤐 INICIANDO PROTOCOLO 'SEM CONVERSA FIADA'...")
    
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

    # 3. GERAÇÃO DE LEGENDA BLINDADA
    print("🧠 Gerando legenda direta (sem listas)...")
    legenda_final = "Milho verde premium! 🌽 #milho" # Reserva
    
    # PROMPT "SNIPER" - AQUI ESTÁ A MÁGICA
    prompt_sistema = """
    Atue como um Social Media Manager profissional.
    Sua tarefa é escrever a legenda para esta foto de milho verde.
    
    REGRAS OBRIGATÓRIAS:
    1. NÃO escreva introduções como "Aqui estão opções" ou "Claro".
    2. NÃO faça listas numeradas (1, 2, 3).
    3. Escreva APENAS UMA legenda final, pronta para publicar.
    4. Use emojis.
    5. O texto deve ser persuasivo e curto.
    
    Responda APENAS com o texto da legenda.
    """

    try:
        # Scanner de modelos (mantido)
        url_list = f"https://generativelanguage.googleapis.com/v1beta/models?key={gemini_key}"
        r_list = requests.get(url_list, timeout=10)
        modelo_escolhido = "gemini-1.5-flash" # Padrão caso falhe o scan
        
        if r_list.status_code == 200:
            dados = r_list.json()
            if 'models' in dados:
                for m in dados['models']:
                    if 'generateContent' in m.get('supportedGenerationMethods', []):
                        modelo_escolhido = m['name'].replace("models/", "")
                        break
        
        # Chamada com o novo Prompt Blindado
        url_gen = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo_escolhido}:generateContent?key={gemini_key}"
        payload = {"contents": [{"parts": [{"text": prompt_sistema}]}]}
        headers = {'Content-Type': 'application/json'}
        
        r_gen = requests.post(url_gen, headers=headers, json=payload, timeout=10)
        
        if r_gen.status_code == 200:
            texto_ia = r_gen.json()['candidates'][0]['content']['parts'][0]['text']
            # Limpeza extra de segurança (caso a IA teime)
            texto_limpo = texto_ia.replace("Aqui estão algumas opções:", "").replace("**", "").strip()
            # Pega só a primeira linha se ele ainda tentar fazer lista
            if "\n1." in texto_limpo:
                 texto_limpo = texto_limpo.split("\n1.")[0]
            
            legenda_final = texto_limpo
            print("✅ SUCESSO! Legenda limpa gerada.")
        else:
            print(f"⚠️ Erro IA: {r_gen.status_code}")

    except Exception as e:
        print(f"❌ Erro na IA: {e}")

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
    motor_corrigido_sem_papo()
