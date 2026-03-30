from flask import Flask, request, redirect
import requests
import os

app = Flask(__name__)

# CONFIGURAÇÕES - AJUSTADAS PARA VOCÊ
MEU_WHATSAPP = "5519993283883"  # Seu número corrigido
MAKE_URL = "https://hook.us2.make.com/3uqyvy539qkyqsli7wg5uqvebxryf" # Seu link do Make

@app.route('/lead', methods=['POST'])
def lead():
    # Pega os dados do formulário do site
    dados = request.form.to_dict()
    
    # 1. Envia os dados para a Planilha via Make
    try:
        requests.post(MAKE_URL, json=dados)
    except Exception as e:
        print(f"Erro ao enviar para o Make: {e}")

    # 2. Redireciona o cliente para o seu WhatsApp com mensagem personalizada
    mensagem = f"Olá! Vim pelo site e quero simular um consórcio de {dados.get('produto', 'Imóvel')}."
    link_wa = f"https://wa.me/{MEU_WHATSAPP}?text={mensagem}"
    
    return redirect(link_wa)

if __name__ == '__main__':
    # Configuração vital para o Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
