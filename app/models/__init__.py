from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='medewerker')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Lid(db.Model):
    __tablename__ = 'leden'
    id = db.Column(db.Integer, primary_key=True)
    voornaam = db.Column(db.String(100), nullable=False)
    achternaam = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefoon = db.Column(db.String(20))
    adres = db.Column(db.String(255))
    postcode = db.Column(db.String(10))
    plaats = db.Column(db.String(100))
    lidnummer = db.Column(db.String(20), unique=True)
    actief = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    leningen = db.relationship('Lening', backref='lid', lazy=True)

class Boek(db.Model):
    __tablename__ = 'boeken'
    id = db.Column(db.Integer, primary_key=True)
    titel = db.Column(db.String(255), nullable=False)
    auteur = db.Column(db.String(200))
    isbn = db.Column(db.String(20), unique=True)
    uitgever = db.Column(db.String(200))
    jaar_uitgave = db.Column(db.Integer)
    categorie = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    exemplaren = db.relationship('Exemplaar', backref='boek', lazy=True)

class Exemplaar(db.Model):
    __tablename__ = 'exemplaren'
    id = db.Column(db.Integer, primary_key=True)
    boek_id = db.Column(db.Integer, db.ForeignKey('boeken.id'), nullable=False)
    barcode = db.Column(db.String(50), unique=True)
    status = db.Column(db.String(20), default='beschikbaar')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    leningen = db.relationship('Lening', backref='exemplaar', lazy=True)

class Lening(db.Model):
    __tablename__ = 'leningen'
    id = db.Column(db.Integer, primary_key=True)
    exemplaar_id = db.Column(db.Integer, db.ForeignKey('exemplaren.id'))
    lid_id = db.Column(db.Integer, db.ForeignKey('leden.id'), nullable=False)
    datum_uitgeleend = db.Column(db.DateTime, default=datetime.utcnow)
    datum_terug_gepland = db.Column(db.Date)
    datum_teruggekeerd = db.Column(db.DateTime)
    boete_bedrag = db.Column(db.Numeric(6, 2), default=0)
    betaald = db.Column(db.Boolean, default=False)
