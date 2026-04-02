from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import re

app = Flask(__name__)
# Permite que qualquer site acesse (ajuste para o seu github.io se quiser mais segurança depois)
CORS(app) 

# CONFIGURAÇÕES
# Verifique se o número está correto (DDI + DDD + Numero)
MEU_WHATSAPP = "55353832097328" # Exemplo: 55 para Brasil
MAKE_URL = "https://hook.us2.make.com/c4edcl8ia2ggai52xi3igwxvor1qywxm"

@app.route('/lead', methods=['POST'])
def lead():
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

    # 1. Envia para o Make (Planilha) - Sem travar o usuário
    try:
        # Enviamos os dados originais + o celular limpo
        requests.post(MAKE_URL, json=dados, timeout=5)
    except Exception as e:
        print(f"Erro ao avisar o Make: {e}")

    # 2. Prepara o Link do WhatsApp
    produto = dados.get('produto', 'Consórcio')
    nome = dados.get('nome', 'Cliente')
    
    # Criamos a mensagem amigável
    mensagem = f"Olá! Sou {nome}, vim pelo site e quero simular um {produto}."
    
    # Montamos o link final (usando quote para caracteres especiais)
    from urllib.parse import quote
    link_wa = f"https://api.whatsapp.com/send?phone={MEU_WHATSAPP}&text={quote(mensagem)}"

    # O JavaScript espera "whatsapp_url" para fazer o redirecionamento
    return jsonify({"whatsapp_url": link_wa}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
