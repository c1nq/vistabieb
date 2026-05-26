from app import create_app, db
from app.models import User, Lid, Boek, Exemplaar, Lening

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='localhost', port=5000)
