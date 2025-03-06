from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import hashlib

app = Flask(__name__)

# Veritabanı URI'sini yapılandırma
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///links.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQLAlchemy örneği oluşturma
db = SQLAlchemy(app)

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link_id = db.Column(db.String(6), unique=True, nullable=False)
    original_url = db.Column(db.String(2048), nullable=False)

@app.route('/')
def home():
    return redirect("/olustur", code=301)  # 302 geçici yönlendirme (veya 301 kalıcı yönlendirme)

@app.route("/olustur", methods=["GET"])
def olustur():
    return render_template("olustur.html")

@app.route("/kaydet", methods=["POST"])
def kaydet():
    user_link = request.form["link"]
    link_id = hashlib.md5(user_link.encode()).hexdigest()[:6]

    # Veritabanında daha önce kaydedilmiş mi kontrol et
    existing_link = Link.query.filter_by(original_url=user_link).first()
    if existing_link:
        return f"Bu link zaten oluşturulmuş!<br>Oluşturulan sayfa: <a href='/link/{existing_link.link_id}'>butonatikla.onrender.com/link/{existing_link.link_id}</a>"

    # Yeni link ekleme
    new_link = Link(link_id=link_id, original_url=user_link)
    db.session.add(new_link)
    db.session.commit()
    return f"Oluşturulan sayfa: <a href='/link/{link_id}'>butonatikla.onrender.com/link/{link_id}</a>"

@app.route("/link/<link_id>")
def link_sayfasi(link_id):
    link = Link.query.filter_by(link_id=link_id).first()
    if link:
        return render_template("index.html", link_id=link.link_id, original_url=link.original_url)
    else:
        return "Link bulunamadı.", 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
