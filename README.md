bashnano README.md
Vervang alles met placeholders:
markdownWebgebaseerd bibliotheekbeheersysteem voor Vista College gebouwd met Python Flask en PostgreSQL.

## 🎯 Wat is dit?

Vista Leest is een compleet systeem om boeken, leden en leningen te beheren. 
Studenten kunnen inloggen, boeken zoeken, reserveren. Medewerkers kunnen leningen registreren met barcode scanner.

## 🚀 Features

✅ Inloggen met leerlingnummer
✅ Boeken uit/inleveren (barcode scanner)
✅ Reserveringen
✅ Automatische herinneringen via email
✅ Boete berekening (€0,50/dag)
✅ Rollen: Admin, Medewerker, Student
✅ Dagelijks backup
✅ Nederlands taal
✅ Bootstrap 5 responsive design

## 💻 Tech Stack

- **Backend**: Python 3.14.5 + Flask
- **Database**: PostgreSQL 18.4
- **Frontend**: Bootstrap 5 + HTML/CSS/JS
- **Barcode**: QuaggaJS (webcam-based)
- **Email**: Flask-Mail + Gmail SMTP
- **Server**: Linux (Arch-based)

## 📋 Requirements

python 3.14+
postgresql 18.4
pip + venv

Zie `requirements.txt` voor Python dependencies.

## 🛠️ Installation

### 1. Clone & Setup

```bash
git clone https://github.com/c1nq/vistabieb.git
cd vistabieb
```

### 2. Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate.fish  # fish shell
# of: source .venv/bin/activate  # bash
pip install -r requirements.txt
```

### 3. Database

```bash
# Create database
sudo -u postgres psql
CREATE DATABASE vistabieb OWNER postgres;
\q

# Load schema
psql -d vistabieb -f schema.sql

# Create admin user
python setup_user.py
# Username: admin
# Password: admin123
```

### 4. Environment Variables

```bash
nano .env
```

Zet (met je eigen Gmail app password):
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=<your_app_password>
MAIL_DEFAULT_SENDER=your_email@gmail.com
SECRET_KEY=dev-key-change-in-production

### 5. Run

```bash
python run.py
```

Open: http://localhost:5000

Login: admin / admin123

## 📚 Documenten

Zie project root voor:
- `BEHOEFTEANALYSE.txt` - Wat wilt de klant?
- `FUNCTIONEEL_ONTWERP.txt` - Hoe werkt het systeem?
- `TECHNISCH_ONTWERP.txt` - Hoe is het gebouwd?

## 🗂️ Projectstructuur
vistabieb/
├── app/
│   ├── models/         # Database models
│   ├── routes/         # Flask routes & handlers
│   ├── templates/      # HTML templates
│   └── static/         # CSS
├── config.py           # Configuration
├── run.py              # Start server
├── schema.sql          # Database schema
├── seed_data.py        # Test data
├── setup_user.py       # Create admin user
├── backup.sh           # Backup script
├── stuur_herinneringen.py  # Email reminders
└── requirements.txt    # Dependencies

## 🔐 Rollen

**Admin**
- Alles beheren (boeken, leden, leningen)
- Herinneringen versturen
- Database info zien

**Medewerker**
- Boeken uitlenen/inleveren (barcode)
- Boeken en leden toevoegen
- Leningen beheren

**Student**
- Boeken zoeken
- Boeken reserveren
- Eigen leningen zien

## 📧 Email Setup

Gmail:
1. Go to myaccount.google.com/apppasswords
2. Generate app password for Mail
3. Put in .env (MAIL_PASSWORD)

## 🔄 Backup & Restore

### Backup (handmatig)

```bash
./backup.sh
```

### Cron (automatisch dagelijks 00:00)

```bash
0 0 * * * /bin/bash /path/to/vistabieb/backup.sh >> /path/to/vistabieb/backups/backup.log 2>&1
```

### Restore

```bash
dropdb vistabieb
createdb -O postgres vistabieb
psql -d vistabieb -f backups/vistabieb_YYYY-MM-DD.sql
```

## 🧪 Test Data

```bash
python seed_data.py
```

Laadt:
- 5 boeken
- 15 exemplaren
- 4 leden
- 4 leningen (test herinneringen)

## 🚢 Deployment (Production)

### 1. Gunicorn + Nginx

```bash
pip install gunicorn
gunicorn --workers 4 --bind 127.0.0.1:5000 app:app
```

### 2. Systemd Service

Create `/etc/systemd/system/vistabieb.service`:

```ini
[Unit]
Description=Vista Leest
After=network.target

[Service]
User=<your_user>
WorkingDirectory=/path/to/vistabieb
Environment="PATH=/path/to/vistabieb/.venv/bin"
ExecStart=/path/to/vistabieb/.venv/bin/gunicorn --workers 4 --bind 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target
```

Start:
```bash
sudo systemctl start vistabieb
sudo systemctl enable vistabieb
```

### 3. HTTPS (Let's Encrypt)

```bash
sudo certbot certonly --standalone -d yourdomain.com
```

Configure Nginx with SSL.

## 📖 API Endpoints

### Leningen
- `POST /api/exemplaar/<barcode>` - Lookup exemplaar
- `POST /api/leningen/checkout` - Uitlenen
- `POST /api/leningen/return` - Inleveren + boete

### Herinneringen
- `POST /herinneringen/stuur` - Email versturen

## 🐛 Development

### Database Shell

```bash
psql -d vistabieb
```

### Flask Shell

```bash
python
>>> from app import create_app, db
>>> app = create_app()
>>> with app.app_context():
>>>     from app.models import User
>>>     users = User.query.all()
```

### Logs

```bash
journalctl -u vistabieb -f
```

## 📞 Contact

Klant: Vista College
Contact: [contact details]

## 📅 Timeline

- **Week 1**: Database + login
- **Week 2**: Features (barcode, reserveringen)
- **Week 3**: Polish + testing
- **Final**: Live deployment

## ✅ Done

- [x] Database schema
- [x] Flask app setup
- [x] Authentication (leerlingnummer)
- [x] CRUD voor leden, boeken, leningen
- [x] Barcode scanner (QuaggaJS)
- [x] Reserveringen
- [x] Email herinneringen
- [x] Backup script
- [x] Bootstrap styling
- [x] Dutch translation
- [x] Deployment ready

## 📝 License

School project Vista College

---

Open source library management system
