from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import qrcode
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'chave_secreta'

db = SQLAlchemy(app)

class Ingresso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    qr_code_path = db.Column(db.String(200), nullable=False)

def gerar_qr_code(conteudo, ingresso_id):
    qr = qrcode.make(conteudo)
    caminho = f'static/qr_{ingresso_id}.png'
    qr.save(caminho)
    return caminho

@app.route("/", methods=["GET", "POST"])
def comprar():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        
        novo_ingresso = Ingresso(nome=nome, email=email, qr_code_path="")
        db.session.add(novo_ingresso)
        db.session.commit()
        
        novo_ingresso.qr_code_path = gerar_qr_code(f"Ingresso-{novo_ingresso.id}", novo_ingresso.id)
        db.session.commit()

        flash("Ingresso comprado! QR Code gerado.", "success")
        return redirect(url_for("painel"))

    return render_template("index.html")

@app.route("/painel")
def painel():
    ingressos = Ingresso.query.all()
    return render_template("painel.html", ingressos=ingressos)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
@app.route("/", methods=["GET", "HEAD"])
def comprar():
    if request.method == "HEAD":
        return "", 200
    return render_template("index.html")
