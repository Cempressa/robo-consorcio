from flask import Flask, request, jsonify, redirect
from flask_cors import CORS # Importante para evitar erros de domínio
import requests
import os
import json
import re

app = Flask(__name__)
CORS(app) # Permite que seu site fale com o servidor sem bloqueios

# CONFIGURAÇÕES
MEU_WHATSAPP = "353832097328"
MAKE_URL = "https://hook.us2.make.com/2nyg3x5v07l1arfgg8k36bsorrem4hru"

@app.route('/lead', methods=['POST'])
def lead():
    # 1. Tenta pegar dados via JSON (do Fetch/JS) ou via Form (Tradicional)
    if request.is_json:
        dados = request.get_json()
    else:
        dados = request.form.to_dict()

    if not dados:
        return jsonify({"error": "Dados não recebidos"}), 400

    # 2. Limpeza extra do Celular (Garantia de segurança)
    celular_bruto = dados.get('celular', '')
    celular_limpo = re.sub(r'\D', '', celular_bruto)
    dados['celular_limpo'] = celular_limpo

    # 3. Envia os dados para o Make (Planilha/CRM)
    try:
        requests.post(MAKE_URL, json=dados, timeout=8)
    except Exception as e:
        print(f"Erro ao enviar para o Make: {e}")

    # 4. Prepara as variáveis para o Redirecionamento
    produto = dados.get('produto', 'Consórcio')
    nome = dados.get('nome', 'Cliente')
    
    # Mensagem personalizada para o seu WhatsApp
    mensagem = f"Olá! Sou {nome}, vim pelo site e quero simular um {produto}."
    
    # Criamos a URL de redirecionamento
    # DICA: Se você usa Typebot, pode trocar o link_wa pelo link do bot
    link_wa = f"https://api.whatsapp.com/send?phone={MEU_WHATSAPP}&text={mensagem.replace(' ', '%20')}"

    # 5. RETORNO PARA O JAVASCRIPT
    # Como seu JS espera um JSON com a URL, respondemos assim:
    return jsonify({"redirect_url": link_wa}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
