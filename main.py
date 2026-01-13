import os
import shutil  # Biblioteca essencial para mover arquivos
import requests
import time
from instagrapi import Client

# --- CONFIGURAÇÕES DE PASTAS ---
# Alterado para separar o que é novo do que já foi usado
PASTA_NOVOS = "conteudo_novo"
PASTA_POSTADOS = "conteudo_postado"

def motor_corrigido_sem_papo():
    print("🤐 INICIANDO PROTOCOLO 'SEM CONVERSA FIADA'...")
    
    # 1. Verificação de Ambiente
    insta_session = os.environ.get("INSTA_SESSION")
    gemini_key = os.environ.get("GEMINI_KEY")

    if not insta_session or not gemini_key:
        print("❌ CRÍTICO: Chaves de segurança (Secrets) não encontradas.")
        return

    # 2. Configuração de Diretórios (Auto-Correção)
    # Se as pastas não existirem, o robô cria sozinho para evitar erros
    for pasta in [PASTA_NOVOS, PASTA_POSTADOS]:
        if not os.path.exists(pasta):
            os.makedirs(pasta)
            print(f"📂 Pasta criada automaticamente: {pasta}")

    # 3. Seleção de Mídia (Lógica de Fila)
    # Melhoria: Usa 'sorted' para você controlar a ordem (ex: 01.jpg, 02.mp4)
    # Filtra apenas arquivos de imagem e vídeo válidos
    extensoes_validas = ('.jpg', '.jpeg', '.png', '.mp4', '.mov', '.mkv')
    arquivos = sorted([f for f in os.listdir(PASTA_NOVOS) if f.lower().endswith(extensoes_validas)])
    
    if not arquivos:
        print(f"📭 A pasta '{PASTA_NOVOS}' está vazia. Nada para postar hoje.")
        return

    # Pega sempre o primeiro da fila
    escolhido = arquivos[0]
    caminho_origem = os.path.join(PASTA_NOVOS, escolhido)
    print(f"📦 Mídia Selecionada da Fila: {escolhido}")

    # 4. Conexão Instagram (Com Retentativa)
    cl = Client()
    try:
        # Tenta usar configurações salvas para parecer mais humano
        cl.load_settings("session.json") if os.path.exists("session.json") else None
        
        # Injeta a sessão via env (Login sem senha, mais seguro)
        with open("session.json", "w") as f:
            f.write(insta_session)
        cl.load_settings("session.json")
        print("✅ Instagram: Conectado com sucesso.")
    except Exception as e:
        print(f"❌ Erro Crítico no Login: {e}")
        return

    # 5. GERAÇÃO DE LEGENDA (Cérebro Gemini)
    print("🧠 Gerando legenda blindada...")
    legenda_final = "Milho verde de alta qualidade! 🌽 #milhopremium #agronegocio" # Fallback de segurança
    
    prompt_sistema = """
    Atue como um Social Media Manager especialista em Agronegócio.
    Escreva uma legenda para esta foto/vídeo de milho verde.
    
    REGRAS OBRIGATÓRIAS:
    1. NÃO use introduções ("Aqui está", "Opções").
    2. NÃO faça listas numeradas.
    3. Texto curto, persuasivo e direto.
    4. Use emojis relacionados a milho/campo.
    5. Foco em apetite ou qualidade do produto.
    
    Responda APENAS com o texto da legenda final.
    """

    try:
        # Lógica Simplificada: Tenta o modelo Flash direto (mais rápido e barato)
        modelo = "gemini-1.5-flash"
        url_gen = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={gemini_key}"
        payload = {"contents": [{"parts": [{"text": prompt_sistema}]}]}
        headers = {'Content-Type': 'application/json'}
        
        r_gen = requests.post(url_gen, headers=headers, json=payload, timeout=15)
        
        if r_gen.status_code == 200:
            texto_ia = r_gen.json()['candidates'][0]['content']['parts'][0]['text']
            # Limpeza cirúrgica
            legenda_final = texto_ia.replace("*", "").strip()
            print("✅ SUCESSO! Legenda gerada pela IA.")
        else:
            print(f"⚠️ IA Falhou (Status {r_gen.status_code}). Usando legenda padrão.")

    except Exception as e:
        print(f"⚠️ Erro na conexão com IA: {e}. Usando legenda padrão.")

    # 6. Upload e Movimentação (Ação Final)
    print(f"📤 Iniciando upload para o Instagram...")
    sucesso_upload = False

    try:
        ext = escolhido.lower().split('.')[-1]
        
        if ext in ['mp4', 'mov', 'mkv']:
            # O FFmpeg instalado no YAML vai garantir que isso não trave
            print("🎥 Processando vídeo (Isso pode levar alguns segundos)...")
            cl.video_upload(caminho_origem, legenda_final)
        else:
            print("📸 Processando imagem...")
            cl.photo_upload(caminho_origem, legenda_final)
            
        print("✨ POSTAGEM REALIZADA COM SUCESSO!")
        sucesso_upload = True
        
    except Exception as e:
        print(f"❌ ERRO FATAL NO UPLOAD: {e}")
        # Se der erro no upload, NÃO movemos o arquivo. Ele tenta de novo no próximo horário.

    # 7. Organização Pós-Postagem (Evita Repetição)
    if sucesso_upload:
        try:
            caminho_destino = os.path.join(PASTA_POSTADOS, escolhido)
            
            # Se já existir arquivo com mesmo nome na pasta de postados, renomeia
            if os.path.exists(caminho_destino):
                nome, extensao = os.path.splitext(escolhido)
                timestamp = int(time.time())
                novo_nome = f"{nome}_{timestamp}{extensao}"
                caminho_destino = os.path.join(PASTA_POSTADOS, novo_nome)
            
            shutil.move(caminho_origem, caminho_destino)
            print(f"🔄 Arquivo movido para '{PASTA_POSTADOS}'. Ciclo concluído.")
            
        except Exception as e:
            print(f"⚠️ Postou, mas erro ao mover arquivo: {e}")

if __name__ == "__main__":
    motor_corrigido_sem_papo()
