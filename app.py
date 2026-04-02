from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import re

app = Flask(__name__)
CORS(app) # Permite que o GitHub Pages envie dados para o Render

# CONFIGURAÇÕES
MEU_WHATSAPP = "353832097328"
MAKE_URL = "https://hook.us2.make.com/c4edcl8ia2ggai52xi3igwxvor1qywxm"

@app.route('/lead', methods=['POST'])
def lead():
    # Detecta se os dados vieram via JSON ou Formulário
    if request.is_json:
        dados = request.get_json()
    else:
        dados = request.form.to_dict()

    if not dados:
        return jsonify({"error": "Dados vazios"}), 400

    # Limpeza do celular para o Make
    celular_limpo = re.sub(r'\D', '', dados.get('celular', ''))
    dados['celular_limpo'] = celular_limpo

    # 1. Envia para o Make (Planilha)
    try:
        requests.post(MAKE_URL, json=dados, timeout=10)
    except Exception as e:
        print(f"Erro Make: {e}")

    # 2. Prepara Redirecionamento
    produto = dados.get('produto', 'Consórcio')
    nome = dados.get('nome', 'Cliente')
    
    mensagem = f"Olá! Sou {nome}, vim pelo site e quero simular um {produto}."
    link_wa = f"https://api.whatsapp.com/send?phone={MEU_WHATSAPP}&text={mensagem.replace(' ', '%20')}"

    # Retorna o link para o JavaScript fazer o redirecionamento
    return jsonify({"redirect_url": link_wa}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
