from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from urllib.parse import quote

app = Flask(__name__)
CORS(app, resources={r"/": {"origins": "*"}})

# CONFIGURAÇÕES ATUALIZADAS
MEU_WHATSAPP = "353832097328"  # <-- SEU NÚMERO DA IRLANDA (SEM +)
GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbwwZSIXrm5uv3TlsAlZ2E8NRxtNdNbR8o5rQ8fFfaGRd-XC2zaYgxD7ECq_80c51T2T/exec"

@app.route("/", methods=["POST"])
def receber():
    data = request.form.to_dict()

    # ENVIO PARA A PLANILHA GOOGLE SHEETS
    try:
        requests.post(GOOGLE_SHEET_URL, data=data)
    except Exception as e:
        print("Erro ao enviar para planilha:", e)

    # DADOS DO FORMULÁRIO
    nome = data.get("Nome", "")
    categoria = data.get("Categoria", "")
    opcao = data.get("Opcao", "")
    email = data.get("Email", "")
    whatsapp = data.get("WhatsApp", "")

    # MENSAGEM PARA O WHATSAPP
    mensagem = (
        f"Olá, meu nome é {nome}.\n"
        f"Gostaria de simular: {categoria} - {opcao}.\n"
        f"Meu WhatsApp: {whatsapp}\n"
        f"Meu Email: {email}"
    )

    # LINK FINAL DO WHATSAPP
    link = f"https://wa.me/{MEU_WHATSAPP}?text={quote(mensagem)}"

    return jsonify({"status": "ok", "whatsapp": link})
