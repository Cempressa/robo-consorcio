from flask import Flask, request, redirect
import requests
import os
import json

app = Flask(__name__)

# CONFIGURAÇÕES
MEU_WHATSAPP = "353832097328"
MAKE_URL = "https://hook.us2.make.com/2nyg3x5v07l1arfgg8k36bsorrem4hru"

def obter_credenciais():
    """Tenta carregar as credenciais do Google da variável de ambiente ou do arquivo local"""
    # 1. Tenta ler do Render (Variável de Ambiente)
    if "GOOGLE_CREDS" in os.environ:
        try:
            return json.loads(os.environ.get("GOOGLE_CREDS"))
        except Exception as e:
            print(f"Erro ao ler GOOGLE_CREDS do Render: {e}")
    
    # 2. Tenta ler do arquivo local (Cursor/PC)
    caminho_local = "chave_google.json"
    if os.path.exists(caminho_local):
        with open(caminho_local, "r") as f:
            conteudo = f.read()
            if conteudo.strip(): # Verifica se não está vazio
                return json.loads(conteudo)
    
    print("AVISO: Nenhuma credencial válida encontrada!")
    return None

@app.route('/lead', methods=['POST', 'GET']) # Aceita GET para facilitar seus testes
def lead():
    # Pega dados tanto de formulário (POST) quanto de link (GET)
    if request.method == 'POST':
        dados = request.form.to_dict()
    else:
        dados = request.args.to_dict()
    
    # 1. Envia os dados para a Planilha via Make
    try:
        requests.post(MAKE_URL, json=dados, timeout=5)
    except Exception as e:
        print(f"Erro ao enviar para o Make: {e}")

    # 2. Prepara o redirecionamento para o WhatsApp
    produto = dados.get('produto', 'Consórcio')
    nome = dados.get('nome', 'Cliente')
    
    mensagem = f"Olá! Sou {nome}, vim pelo site e quero simular um {produto}."
    link_wa = f"https://api.whatsapp.com/send?phone={MEU_WHATSAPP}&text={mensagem}"

    return redirect(link_wa)

if __name__ == '__main__':
    # Configuração de porta para o Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
