class Config:
    SECRET_KEY = 'qwerty'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1111@localhost/carsharing'  # Подключение к PostgreSQL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_NAME = 'carsharing_session'
