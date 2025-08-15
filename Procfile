# Heroku Procfile
web: cd backend && gunicorn --bind 0.0.0.0:$PORT app:app
release: cd backend && python -c "from app import db; db.create_all()"
