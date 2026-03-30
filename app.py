from flask import Flask, request, redirect
import requests
import os

app = Flask(__name__)

# CONFIGURAÇÕES
MEU_WHATSAPP = "353832097328"
MAKE_URL = "https://hook.us2.make.com/3uqyvy539qkyqsli7wg5uqvebxrytya3"

@app.route('/lead', methods=['POST'])
def lead():
    dados = request.form.to_dict()
    
    # Envia para o Make usando 'data' (form-data) que é o que o Make espera
    try:
        requests.post(MAKE_URL, data=dados)
    except Exception as e:
        print(f"Erro no Make: {e}")

    mensagem = f"Olá! Vim pelo site e quero simular um consórcio de {dados.get('produto', 'Imóvel')}."
    link_wa = f"https://wa.me/{MEU_WHATSAPP}?text={mensagem}"
    
    return redirect(link_wa)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
