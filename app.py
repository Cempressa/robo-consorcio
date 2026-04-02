from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import re
from urllib.parse import quote

app = Flask(__name__)

# 1. MELHORIA NO CORS: Configuração explícita para evitar o erro de 'preflight'
CORS(app, resources={r"/*": {"origins": "*"}}) 

# CONFIGURAÇÕES
MEU_WHATSAPP = "55353832097328" 
MAKE_URL = "https://hook.us2.make.com/c4edcl8ia2ggai52xi3igwxvor1qywxm"

# 2. ROTA ATUALIZADA: Adicionado 'OPTIONS' para responder ao teste de segurança do navegador
@app.route('/lead', methods=['POST', 'OPTIONS'])
def lead():
    # Responde automaticamente ao teste 'OPTIONS' do navegador
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200

    # Detecta os dados
    if request.is_json:
        dados = request.get_json()
    else:
        dados = request.form.to_dict()

    if not dados:
        return jsonify({"error": "Dados vazios"}), 400

    # Limpeza do celular para a Planilha
    celular_raw = dados.get('celular', '')
    celular_limpo = re.sub(r'\D', '', celular_raw)
    dados['celular_limpo'] = celular_limpo

    # 1. Envia para o Make (Planilha)
    try:
        requests.post(MAKE_URL, json=dados, timeout=5)
    except Exception as e:
        print(f"Erro ao avisar o Make: {e}")

    # 2. Prepara o Link do WhatsApp
    produto = dados.get('produto', 'Consórcio')
    nome = dados.get('nome', 'Cliente')
    
    mensagem = f"Olá! Sou {nome}, vim pelo site e quero simular um {produto}."
    link_wa = f"https://api.whatsapp.com/send?phone={MEU_WHATSAPP}&text={quote(mensagem)}"

    return jsonify({"whatsapp_url": link_wa}), 200

if __name__ == '__main__':
    # O Render usa a variável de ambiente PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
