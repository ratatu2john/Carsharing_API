from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from datetime import datetime

# Инициализация базы данных, миграций и LoginManager
db = SQLAlchemy()  
migrate = Migrate()
login_manager = LoginManager()  

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # Загружаем конфигурацию из объекта Config

    # Инициализация компонентов приложения
    db.init_app(app)  
    migrate.init_app(app, db)  
    login_manager.init_app(app)

    # Указание маршрута для перенаправления неавторизованных пользователей
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    # Импортируем и регистрируем блюпринты
    from admin import admin_bp  # Блюпринт для админки
    from auth import auth_bp  # Блюпринт для аутентификации
    from cars_routes import cars_bp  # Блюпринт для автомобилей (cars)
    from main import main_bp  # Блюпринт для основной логики
    from clients_routes import clients_bp  # Импортируем Blueprint для работы с клиентами
    from tariffs_routes import tariffs_bp  # Блюпринт для тарифов
    from rentals_routes import rentals_bp  # Блюпринт для аренды
    from maintenance_routes import maintenance_bp  # Импортируем Blueprint для обслуживания
    from payments_routes import payments_bp  # Импортируем Blueprint для платежей
    from client import client_bp
    from support import support_bp
  
    # Регистрируем блюпринты с их соответствующими URL префиксами
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(cars_bp, url_prefix='/cars')
    app.register_blueprint(clients_bp, url_prefix='/clients')  # Регистрируем Blueprint для работы с клиентами
    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(tariffs_bp, url_prefix='/tariffs')
    app.register_blueprint(rentals_bp, url_prefix='/rentals')
    app.register_blueprint(maintenance_bp, url_prefix='/maintenance_routes')  # Регистрируем Blueprint для обслуживания
    app.register_blueprint(payments_bp, url_prefix='/payments')  # Регистрируем Blueprint для работы с платежами
    app.register_blueprint(client_bp, url_prefix='/client')
    app.register_blueprint(support_bp, url_prefix='/support')
    

    return app

# Функция для загрузки пользователя
@login_manager.user_loader
def load_user(user_id):
    from models import Admin  # Импортируем модель Admin
    return Admin.query.get(int(user_id))  # Загружаем пользователя по его ID
