import os
import shutil
import time
import warnings
from instagrapi import Client
import google.generativeai as genai 

# --- CONFIGURAÇÕES E LIMPEZA ---
warnings.simplefilter("ignore") 
PASTA_NOVOS = "conteudo_novo"
PASTA_POSTADOS = "conteudo_postado"

def diagnostico_matematico_ia(api_key):
    """
    REALIZA UMA AUDITORIA NA CONTA GOOGLE.
    Em vez de adivinhar o modelo, ele lista o que existe disponível.
    """
    print("🔬 Iniciando Auditoria de Modelos Disponíveis...")
    try:
        genai.configure(api_key=api_key)
        # Pede para a API listar tudo que essa chave pode acessar
        modelos_disponiveis = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                # Limpa o nome (remove 'models/') para usar no código
                nome_limpo = m.name.replace('models/', '')
                modelos_disponiveis.append(nome_limpo)
        
        print(f"📊 Estatística: Encontrados {len(modelos_disponiveis)} modelos compatíveis.")
        
        if not modelos_disponiveis:
            print("❌ ZERO modelos encontrados. Sua chave API pode estar restrita ou errada.")
            return None
            
        # Seleciona o melhor modelo baseado na lista REAL
        # Prioridade: Flash > Pro > Outros
        melhor_escolha = modelos_disponiveis[0] # Pega o primeiro por padrão
        
        for modelo in modelos_disponiveis:
            if 'flash' in modelo and '1.5' in modelo:
                melhor_escolha = modelo
                break
            elif 'pro' in modelo and '1.5' in modelo:
                melhor_escolha = modelo
        
        print(f"✅ Modelo Eleito Matematicamente: {melhor_escolha}")
        return melhor_escolha

    except Exception as e:
        print(f"❌ Falha Crítica na Auditoria: {e}")
        return None

def limpar_lixo_thumbnail(arquivo_video):
    try:
        nome_base = os.path.basename(arquivo_video)
        caminho_thumb = os.path.join(PASTA_NOVOS, f"{nome_base}.jpg")
        if os.path.exists(caminho_thumb):
            os.remove(caminho_thumb)
    except Exception:
        pass

def motor_elite_final():
    print("🚀 INICIANDO MOTOR DE ELITE (MODO CIENTÍFICO)...")

    # 1. Variáveis de Ambiente
    insta_session = os.environ.get("INSTA_SESSION")
    gemini_key = os.environ.get("GEMINI_KEY")

    if not insta_session or not gemini_key:
        print("❌ ERRO: Chaves ausentes.")
        return

    # 2. Configuração de Pastas
    for pasta in [PASTA_NOVOS, PASTA_POSTADOS]:
        if not os.path.exists(pasta):
            os.makedirs(pasta)

    # 3. Seleção de Arquivo
    extensoes = ('.mp4', '.mov', '.avi', '.jpg', '.png')
    arquivos = sorted([f for f in os.listdir(PASTA_NOVOS) if f.lower().endswith(extensoes)])

    if not arquivos:
        print(f"📭 Nada para postar em '{PASTA_NOVOS}'.")
        return

    escolhido = arquivos[0]
    caminho_origem = os.path.join(PASTA_NOVOS, escolhido)
    print(f"📦 Mídia: {escolhido}")

    # 4. Login Instagram
    cl = Client()
    try:
        with open("session.json", "w") as f:
            f.write(insta_session)
        cl.load_settings("session.json")
        print("✅ Instagram Conectado.")
    except Exception as e:
        print(f"❌ Erro Login: {e}")
        return

    # 5. Geração de Legenda (LÓGICA MATEMÁTICA)
    print("🧠 Calculando melhor rota de IA...")
    
    # PASSO 1: Descobrir qual modelo existe DE VERDADE na sua conta
    modelo_real = diagnostico_matematico_ia(gemini_key)
    
    legenda_final = "Milho Premium! 🌽 #agronegocio" # Backup

    if modelo_real:
        try:
            print(f"🔌 Conectando no modelo comprovado: {modelo_real}...")
            model = genai.GenerativeModel(modelo_real)
            prompt = f"Crie uma legenda curta e apetitosa para Instagram sobre milho verde premium. Use emojis. Sem aspas. Arquivo: {escolhido}"
            
            response = model.generate_content(prompt)
            if response and response.text:
                legenda_final = response.text.strip()
                print("✅ SUCESSO ABSOLUTO NA IA.")
        except Exception as e:
            print(f"⚠️ Erro inesperado na geração: {e}")
    else:
        print("⚠️ Usando legenda padrão (Falha na Auditoria).")

    # 6. Postagem
    sucesso = False
    try:
        print("📤 Postando...")
        if escolhido.lower().endswith(('.mp4', '.mov', '.avi')):
            cl.video_upload(caminho_origem, legenda_final)
            limpar_lixo_thumbnail(escolhido)
        else:
            cl.photo_upload(caminho_origem, legenda_final)
        
        print("✨ POSTADO COM SUCESSO!")
        sucesso = True
    except Exception as e:
        print(f"❌ Erro Upload: {e}")

    # 7. Mover Arquivo
    if sucesso:
        destino = os.path.join(PASTA_POSTADOS, escolhido)
        if os.path.exists(destino):
            timestamp = int(time.time())
            destino = os.path.join(PASTA_POSTADOS, f"{timestamp}_{escolhido}")
        shutil.move(caminho_origem, destino)
        print(f"🔄 Movido para postados.")

if __name__ == "__main__":
    motor_elite_final()
