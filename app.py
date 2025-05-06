import os

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from dotenv import load_dotenv


# Carregar variáveis do .env
load_dotenv()

app = Flask(__name__)

# Configurações do Flask-Mail com variáveis do .env
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.secret_key = os.getenv('SECRET_KEY')

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    msg = Message('Novo contato do portfólio',
                  sender=email,
                  recipients=[os.getenv('MAIL_USERNAME')])
    msg.body = f"Nome: {name}\nEmail: {email}\nMensagem: {message}"

    try:
        mail.send(msg)
        flash('Mensagem enviada com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao enviar mensagem: {str(e)}', 'danger')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)


load_dotenv()

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.secret_key = os.getenv('SECRET_KEY')
