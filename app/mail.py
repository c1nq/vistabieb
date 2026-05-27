from datetime import date, timedelta
from flask_mail import Message
from app.models import db, Lening, Herinnering

REMINDER_TYPES = {
    1: {
        'name': '3 dagen voor deadline',
        'subject': 'Herinnering: uw boek is bijna terug verwacht',
        'days_before': 3
    },
    2: {
        'name': 'Op deadline dag',
        'subject': 'Herinnering: uw boek is vandaag terug verwacht',
        'days_before': 0
    },
    3: {
        'name': '7 dagen na deadline',
        'subject': 'Herinnering: uw boek is te laat - boete wordt berekend',
        'days_before': -7
    }
}

def get_reminder_html(lening, reminder_type):
    config = REMINDER_TYPES[reminder_type]
    boek_titel = lening.exemplaar.boek.titel if lening.exemplaar else 'Onbekend boek'
    lid_naam = f"{lening.lid.voornaam} {lening.lid.achternaam}"

    if reminder_type == 1:
        body = f"Geachte {lid_naam},<br><br>dit is een vriendelijke herinnering dat uw geleende boek \"{boek_titel}\" over 3 dagen terug verwacht wordt.<br><br>Terugbrengen voor: <strong>{lening.datum_terug_gepland.strftime('%d-%m-%Y')}</strong><br><br>Dank u wel,<br>Vista Leest Bibliotheek"
    elif reminder_type == 2:
        body = f"Geachte {lid_naam},<br><br>het geleende boek \"{boek_titel}\" moet vandaag teruggegeven worden.<br><br>Terugbrengen voor: <strong>{lening.datum_terug_gepland.strftime('%d-%m-%Y')}</strong><br><br>Dank u wel,<br>Vista Leest Bibliotheek"
    else:  # type 3
        overdue_days = (date.today() - lening.datum_terug_gepland).days
        body = f"Geachte {lid_naam},<br><br>het geleende boek \"{boek_titel}\" is <strong>{overdue_days} dagen</strong> te laat ingeleverd.<br><br>Boete: €0,50 per dag (max €5,00)<br><br>Dank u wel,<br>Vista Leest Bibliotheek"

    return body

def stuur_herinneringen(app):
    with app.app_context():
        from flask_mail import Mail
        mail = Mail(app)
        today = date.today()
        result = {'sent': 0, 'skipped': 0, 'errors': []}

        for reminder_type, config in REMINDER_TYPES.items():
            trigger_date = today + timedelta(days=config['days_before'])

            leningen = Lening.query.filter(
                Lening.datum_teruggekeerd == None,
                Lening.datum_terug_gepland == trigger_date
            ).all()

            for lening in leningen:
                try:
                    # Check if already sent
                    existing = Herinnering.query.filter_by(
                        lening_id=lening.id,
                        type=reminder_type
                    ).first()

                    if existing:
                        result['skipped'] += 1
                        continue

                    # Send email
                    html_body = get_reminder_html(lening, reminder_type)
                    msg = Message(
                        subject=config['subject'],
                        recipients=[lening.lid.email],
                        html=html_body
                    )
                    mail.send(msg)

                    # Record in DB
                    herinnering = Herinnering(
                        lening_id=lening.id,
                        type=reminder_type,
                        sent=True
                    )
                    db.session.add(herinnering)
                    db.session.commit()

                    result['sent'] += 1

                except Exception as e:
                    result['errors'].append(f"Lening {lening.id}: {str(e)}")

        return result
