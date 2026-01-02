import os
from supabase import create_client

# Dados do seu projeto que já configuramos
URL_SUPABASE = "https://awnfnetfowepwjvrghxa.supabase.co"
KEY_SUPABASE = "sb_publishable__x416gArfeUe3rXM6SHOew_D7mWfuoY"

def iniciar_robo():
    print("🤖 Robô iniciando...")
    supabase = create_client(URL_SUPABASE, KEY_SUPABASE)
    
    try:
        dados = supabase.table('configuracoes').select('nicho').order('created_at', desc=True).limit(1).execute()
        if dados.data:
            nicho_atual = dados.data[0]['nicho']
            print(f"✅ Sucesso! O nicho detectado foi: {nicho_atual}")
        else:
            print("⚠️ Nenhuma configuração encontrada.")
    except Exception as e:
        print(f"❌ Erro ao ler o banco: {e}")

if __name__ == "__main__":
    iniciar_robo()
