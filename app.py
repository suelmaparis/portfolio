import os
from flask import Flask, render_template, request, flash, redirect, url_for
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = 'um_valor_secreto_aqui'

@app.route('/send_email', methods=['GET', 'POST'])
def send_email():
    if request.method == 'POST':
        first_name = request.form.get('first_name', '')
        last_name = request.form.get('last_name', '')
        email = request.form.get('email', '')
        message = request.form.get('message', '')

        if not (first_name and last_name and email and message):
            flash('Todos os campos são obrigatórios.')
            return redirect(url_for('index'))

        try:
            msg = MIMEText(f"Mensagem de {first_name} {last_name} <{email}>:\n\n{message}")
            msg['Subject'] = 'Novo formulário recebido'
            msg['From'] = 'seuemail@dominio.com'
            msg['To'] = 'suelmacruz22@gmail.com'

            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login('suelmacruz22@gmail.com', 'bhlvaxeixzgowitx')
                server.send_message(msg)

            flash('Email enviado com sucesso!')
        except Exception as e:
            print(e)
            flash('Erro ao enviar o email.')

        return redirect(url_for('index'))
    else:
        # Se acessarem /send_email por GET, redireciona para a home
        return redirect(url_for('index'))
    
@app.route('/')
def index():
    return render_template('index.html')