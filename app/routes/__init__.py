from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from app.models import db, User, Lid, Boek, Exemplaar, Lening, Reservering
from datetime import datetime, timedelta

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        leerlingnummer = request.form.get('leerlingnummer')
        password = request.form.get('password')
        user = User.query.filter_by(leerlingnummer=leerlingnummer).first()
        
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

@main.route('/boeken/<int:id>/edit', methods=['GET', 'POST'])
def boeken_edit(id):
    if not check_login():
        return redirect(url_for('auth.login'))
    
    boek = Boek.query.get_or_404(id)
    
    if request.method == 'POST':
        boek.titel = request.form.get('titel')
        boek.auteur = request.form.get('auteur')
        boek.isbn = request.form.get('isbn')
        boek.uitgever = request.form.get('uitgever')
        boek.jaar_uitgave = request.form.get('jaar_uitgave')
        boek.categorie = request.form.get('categorie')
        db.session.commit()
        return redirect(url_for('main.boeken_list'))
    
    return render_template('boeken_form.html', boek=boek)

# LENINGEN
@main.route('/leningen')
def leningen_list():
    if not check_login():
        return redirect(url_for('auth.login'))
    
    leningen = Lening.query.all()
    return render_template('leningen_list.html', leningen=leningen, now=datetime.now().date())

@main.route('/leningen/new/<int:lid_id>/<int:boek_id>', methods=['POST'])
def leningen_new(lid_id, boek_id):
    if not check_login():
        return redirect(url_for('auth.login'))
    
    # Zoek beschikbaar exemplaar
    exemplaar = Exemplaar.query.filter_by(boek_id=boek_id, status='beschikbaar').first()
    if not exemplaar:
        return 'Geen beschikbare exemplaren', 400
    
    lid = Lid.query.get_or_404(lid_id)
    lening = Lening(
        exemplaar_id=exemplaar.id,
        lid_id=lid_id,
        datum_terug_gepland=(datetime.now() + timedelta(days=21)).date()
    )
    exemplaar.status = 'uitgeleend'
    db.session.add(lening)
    db.session.commit()
    
    return redirect(url_for('main.leningen_list'))

@main.route('/leningen/<int:id>/return', methods=['POST'])
def leningen_return(id):
    if not check_login():
        return redirect(url_for('auth.login'))

    lening = Lening.query.get_or_404(id)
    lening.exemplaar.status = 'beschikbaar'
    lening.datum_teruggekeerd = datetime.now()

    # Boete berekenen
    if datetime.now().date() > lening.datum_terug_gepland:
        dagen_te_laat = (datetime.now().date() - lening.datum_terug_gepland).days
        lening.boete_bedrag = dagen_te_laat * 0.50  # €0.50 per dag

    db.session.commit()
    return redirect(url_for('main.leningen_list'))

# RESERVERINGEN
@main.route('/reserveringen')
def reserveringen_list():
    if not check_login():
        return redirect(url_for('auth.login'))

    reserveringen = Reservering.query.all()
    return render_template('reserveringen_list.html', reserveringen=reserveringen)

@main.route('/reserveringen/new/<int:boek_id>', methods=['GET', 'POST'])
def reserveringen_new(boek_id):
    if not check_login():
        return redirect(url_for('auth.login'))

    boek = Boek.query.get_or_404(boek_id)
    leden = Lid.query.all()

    if request.method == 'POST':
        lid_id = request.form.get('lid_id')

        # Check for duplicate actief reservation
        existing = Reservering.query.filter_by(
            lid_id=lid_id,
            boek_id=boek_id,
            status='actief'
        ).first()
        if existing:
            return render_template('reserveringen_form.html',
                                 boek=boek,
                                 leden=leden,
                                 error='Dit lid heeft al een actieve reservering voor dit boek')

        reservering = Reservering(lid_id=lid_id, boek_id=boek_id)
        db.session.add(reservering)
        db.session.commit()
        return redirect(url_for('main.reserveringen_list'))

    return render_template('reserveringen_form.html', boek=boek, leden=leden)

@main.route('/reserveringen/<int:id>/cancel', methods=['POST'])
def reserveringen_cancel(id):
    if not check_login():
        return redirect(url_for('auth.login'))

    reservering = Reservering.query.get_or_404(id)
    reservering.status = 'geannuleerd'
    db.session.commit()
    return redirect(url_for('main.reserveringen_list'))
