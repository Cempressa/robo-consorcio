from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re
from urllib.parse import quote

app = Flask(__name__)
CORS(app, resources={r"/": {"origins": "*"}})

# CONFIGURAÇÕES CORRETAS
MEU_WHATSAPP = "5519996661688"  # SEU NÚMERO
GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbwwZSIXrm5uv3TlsAlZ2E8NRxtNdNbR8o5rQ8fFfaGRd-XC2zaYgxD7ECq_80c51T2T/exec"

@app.route("/", methods=["POST"])
def receber():
    data = request.form.to_dict()

    # Envia para a planilha
    try:
        requests.post(GOOGLE_SHEET_URL, data=data)
    except Exception as e:
        print("Erro ao enviar para planilha:", e)

    # Monta mensagem do WhatsApp
    nome = data.get("Nome", "")
    categoria = data.get("Categoria", "")
    opcao = data.get("Opcao", "")
    email = data.get("Email", "")
    whatsapp = data.get("WhatsApp", "")

    mensagem = (
        f"Olá, meu nome é {nome}.\n"
        f"Gostaria de simular: {categoria} - {opcao}.\n"
        f"Meu WhatsApp: {whatsapp}\n"
        f"Meu Email: {email}"
    )

    link = f"https://wa.me/{MEU_WHATSAPP}?text={quote(mensagem)}"

    return jsonify({"status": "ok", "whatsapp": link})
