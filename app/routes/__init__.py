from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from app.models import db, User, Lid, Boek, Exemplaar, Lening

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['role'] = user.role
            return redirect(url_for('main.dashboard'))
        return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

main = Blueprint('main', __name__)

def check_login():
    return 'user_id' in session

@main.route('/')
def index():
    return redirect(url_for('main.dashboard'))

@main.route('/dashboard')
def dashboard():
    if not check_login():
        return redirect(url_for('auth.login'))
    
    leden_count = Lid.query.count()
    boeken_count = Boek.query.count()
    leningen_count = Lening.query.filter(Lening.datum_teruggekeerd == None).count()
    
    return render_template('dashboard.html', 
                         leden=leden_count, 
                         boeken=boeken_count, 
                         leningen=leningen_count)

# LEDEN CRUD
@main.route('/leden')
def leden_list():
    if not check_login():
        return redirect(url_for('auth.login'))
    
    leden = Lid.query.all()
    return render_template('leden_list.html', leden=leden)

@main.route('/leden/add', methods=['GET', 'POST'])
def leden_add():
    if not check_login():
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        lid = Lid(
            voornaam=request.form.get('voornaam'),
            achternaam=request.form.get('achternaam'),
            email=request.form.get('email'),
            telefoon=request.form.get('telefoon'),
            adres=request.form.get('adres'),
            postcode=request.form.get('postcode'),
            plaats=request.form.get('plaats'),
            lidnummer=request.form.get('lidnummer')
        )
        db.session.add(lid)
        db.session.commit()
        return redirect(url_for('main.leden_list'))
    
    return render_template('leden_form.html')

@main.route('/leden/<int:id>/edit', methods=['GET', 'POST'])
def leden_edit(id):
    if not check_login():
        return redirect(url_for('auth.login'))
    
    lid = Lid.query.get_or_404(id)
    
    if request.method == 'POST':
        lid.voornaam = request.form.get('voornaam')
        lid.achternaam = request.form.get('achternaam')
        lid.email = request.form.get('email')
        lid.telefoon = request.form.get('telefoon')
        lid.adres = request.form.get('adres')
        lid.postcode = request.form.get('postcode')
        lid.plaats = request.form.get('plaats')	
        db.session.commit()
        return redirect(url_for('main.leden_list'))
    
    return render_template('leden_form.html', lid=lid)

@main.route('/leden/<int:id>/delete', methods=['POST'])
def leden_delete(id):
    if not check_login():
        return redirect(url_for('auth.login'))
    
    lid = Lid.query.get_or_404(id)
    db.session.delete(lid)
    db.session.commit()
    return redirect(url_for('main.leden_list'))

# BOEKEN CRUD
@main.route('/boeken')
def boeken_list():
    if not check_login():
        return redirect(url_for('auth.login'))
    
    boeken = Boek.query.all()
    return render_template('boeken_list.html', boeken=boeken)

@main.route('/boeken/add', methods=['GET', 'POST'])
def boeken_add():
    if not check_login():
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        boek = Boek(
            titel=request.form.get('titel'),
            auteur=request.form.get('auteur'),
            isbn=request.form.get('isbn'),
            uitgever=request.form.get('uitgever'),
            jaar_uitgave=request.form.get('jaar_uitgave'),
            categorie=request.form.get('categorie')
        )
        db.session.add(boek)
        db.session.commit()
        return redirect(url_for('main.boeken_list'))
    
    return render_template('boeken_form.html')

# LENINGEN
@main.route('/leningen')
def leningen_list():
    if not check_login():
        return redirect(url_for('auth.login'))
    
    leningen = Lening.query.all()
    return render_template('leningen_list.html', leningen=leningen)
