from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    existing = User.query.filter_by(username='admin').first()
    if existing:
        print('Admin user already exists')
    else:
        user = User(username='admin', email='admin@vistabieb.nl', role='admin')
        user.set_password('admin123')
        db.session.add(user)
        db.session.commit()
        print('Admin user created')
