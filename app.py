import os
import smtplib

from flask import Flask, render_template, request, flash, redirect, url_for
from email.mime.text import MIMEText
from werkzeug.utils import secure_filename

from models import db, Testimonial

app = Flask(__name__)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

app.secret_key = 'um_valor_secreto_aqui'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/send_email', methods=['GET', 'POST'])
def send_email():
    if request.method == 'POST':
        first_name = request.form.get('first_name', '')
        last_name = request.form.get('last_name', '')
        email = request.form.get('email', '')
        message = request.form.get('message', '')

        if not (first_name and last_name and email and message):
            flash('All fields are required.')
            return redirect(url_for('index'))

        try:
            msg = MIMEText(f"New message from {first_name} {last_name} <{email}>:\n\n{message}")
            msg['Subject'] = 'New Message from Your Portfolio'
            msg['From'] = 'seuemail@dominio.com'
            msg['To'] = 'suelmacruz22@gmail.com'

            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login('suelmacruz22@gmail.com', 'bhlvaxeixzgowitx')
                server.send_message(msg)

            flash('Email sent successfully!')
        except Exception as e:
            print(e)
            flash('Error sending email.')

        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))
    
@app.route('/')
def index():
    testimonials = Testimonial.query.all()
    return render_template('index.html', testimonials=testimonials)

@app.route('/add_testimonial', methods=['POST'])
def add_testimonial():
    name = request.form['name']
    role = request.form['role']
    message = request.form['message']

    upload_folder = os.path.join('static', 'assets', 'images', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)

    photo = request.files.get('photo')
    if photo and photo.filename != '':
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(upload_folder, filename))
    else:
        filename = 'default.jpg'

    testimonial = Testimonial(
        name=name,
        role=role,
        message=message,
        image_filename=filename
    )
    db.session.add(testimonial)
    db.session.commit()

    return redirect(url_for('index'))
