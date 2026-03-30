from flask import Flask, request, redirect
import requests

app = Flask(__name__)

@app.route('/lead', methods=['POST'])
def lead():
    # Pega os dados do formulário
    dados = request.form.to_dict()
    print(f"Lead Recebido: {dados}")
    
    # ENVIAR PARA O MAKE (Cole o seu link entre as aspas abaixo)
    make_url = "https://hook.us2.make.com/3uqyvy539qkyqsli7wg5uqvebxrytya3"
    try:
        requests.post(make_url, json=dados)
    except:
        print("Erro ao enviar para o Make")

    # Redireciona para o seu WhatsApp
    meu_whatsapp = "5519993283883" # Já coloquei o seu número do print!
    return redirect(f"https://wa.me/{meu_whatsapp}?text=Olá! Vim pelo site e gostaria de uma simulação de consórcio para {dados.get('produto')}.")
    

if __name__ == '__main__':
    print("🚀 Robô ligado e aguardando leads...")
    app.run(port=5000, debug=True)