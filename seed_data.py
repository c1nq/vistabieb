from app import create_app, db
from app.models import Boek, Exemplaar, Lid, Lening
from datetime import datetime, timedelta

app = create_app()

with app.app_context():
    # Clear existing
    db.session.query(Lening).delete()
    db.session.query(Exemplaar).delete()
    db.session.query(Boek).delete()
    db.session.query(Lid).delete()
    
    # Boeken
    boeken = [
        Boek(titel='Python 101', auteur='Mark Lutz', isbn='978-1449355739', categorie='Programmeren'),
        Boek(titel='Clean Code', auteur='Robert C. Martin', isbn='978-0132350884', categorie='Programmeren'),
        Boek(titel='The Pragmatic Programmer', auteur='Hunt & Thomas', isbn='978-0201616224', categorie='Programmeren'),
        Boek(titel='De Hobbit', auteur='J.R.R. Tolkien', isbn='978-9001136888', categorie='Fantasy'),
        Boek(titel='1984', auteur='George Orwell', isbn='978-0451524935', categorie='Sciencefiction'),
    ]
    db.session.add_all(boeken)
    db.session.commit()
    
    # Exemplaren
    exemplaren = []
    for boek in boeken:
        for i in range(3):
            exemplaar = Exemplaar(boek_id=boek.id, barcode=f'EX{boek.id}{i}', status='beschikbaar')
            exemplaren.append(exemplaar)
    db.session.add_all(exemplaren)
    db.session.commit()
    
    # Leden
    leden = [
        Lid(voornaam='Jan', achternaam='Jansen', email='jan@example.com', telefoon='0612345678', 
            adres='Straat 1', postcode='1234AB', plaats='Amsterdam', lidnummer='L001'),
        Lid(voornaam='Maria', achternaam='Müller', email='maria@example.com', telefoon='0687654321',
            adres='Straat 2', postcode='5678CD', plaats='Rotterdam', lidnummer='L002'),
        Lid(voornaam='Peter', achternaam='Pieterse', email='peter@example.com', telefoon='0698765432',
            adres='Straat 3', postcode='9012EF', plaats='Utrecht', lidnummer='L003'),
    ]
    db.session.add_all(leden)
    db.session.commit()
    
    # Leningen
    leningen = [
        Lening(exemplaar_id=1, lid_id=1, datum_uitgeleend=datetime.now() - timedelta(days=5),
               datum_terug_gepland=datetime.now() + timedelta(days=16)),
        Lening(exemplaar_id=2, lid_id=2, datum_uitgeleend=datetime.now() - timedelta(days=2),
               datum_terug_gepland=datetime.now() + timedelta(days=19)),
        Lening(exemplaar_id=4, lid_id=1, datum_uitgeleend=datetime.now() - timedelta(days=10),
               datum_teruggekeerd=datetime.now()),
    ]
    db.session.add_all(leningen)
    db.session.commit()
    
    print('✓ Testdata ingeladen')
