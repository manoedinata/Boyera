from flask_migrate import upgrade

from boyera import create_app

app = create_app()
with app.app_context():
    # Upgrade
    upgrade()
