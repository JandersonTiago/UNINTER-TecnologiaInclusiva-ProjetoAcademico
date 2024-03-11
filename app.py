# Importando as bibliotecas necessárias
from flask import Flask, render_template, request
from twilio.rest import Client
from decouple import config
from dotenv import load_dotenv

# Carregando as variáveis de ambiente do arquivo .env
load_dotenv()

# Inicializando o aplicativo Flask
app = Flask(__name__)

# Rota principal que renderiza o template index.html
@app.route('/')
def index():
    return render_template('index.html')

# Rota para processar o formulário e enviar a mensagem via WhatsApp
@app.route('/enviar-mensagem', methods=['POST'])
def enviar_mensagem():
    # Obtendo os dados do formulário
    opcao = request.form.get('opcao')
    email = request.form.get('email')
    telefone = request.form.get('telefone')
    recado = request.form.get('recado')

    # Obtendo as credenciais do Twilio a partir das variáveis de ambiente
    account_sid = config('TWILIO_ACCOUNT_SID')
    auth_token = config('TWILIO_AUTH_TOKEN')
    twilio_phone_number = config('TWILIO_PHONE_NUMBER')
    whatsapp_admin_number = config('TWILIO_WHATSAPP_NUMBER')

    # Inicializando o cliente Twilio
    client = Client(account_sid, auth_token)

    # Construindo o corpo da mensagem
    message_body = f"Opção: {opcao}\nEmail: {email}\nTelefone: {telefone}\nRecado: {recado}"

    # Enviando a mensagem via WhatsApp usando a API do Twilio
    message = client.messages.create(
        body=message_body,
        from_=f"whatsapp:{twilio_phone_number}",
        to=f"whatsapp:{whatsapp_admin_number}"
    )

    # Registrando informações no log do aplicativo Flask
    app.logger.info(f'Mensagem enviada via WhatsApp SID: {message.sid}')

    # Retornando uma mensagem de sucesso para o usuário
    return 'Mensagem enviada com sucesso para o WhatsApp!'

# Iniciando o aplicativo Flask quando este script é executado
if __name__ == '__main__':
    app.run(debug=True)
