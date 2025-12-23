from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from compile import db  # Импортируем db из compile.py

# Модель User для пользователей
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(20), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Модель Car для машин
class Car(db.Model):
    __tablename__ = 'car'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mark = db.Column(db.String(50))
    model = db.Column(db.String(50))
    year = db.Column(db.Integer)
    number = db.Column(db.String(50))
    geoposition = db.Column(db.String(50))
    status = db.Column(db.String(20), default='доступен')
    maintenance = db.relationship('Maintenance', backref='car', cascade='all, delete-orphan', lazy=True)
    mileage = db.Column(db.Integer, nullable=False)  # Пробег
    
# Модель Rental для аренд
class Rental(db.Model):
    rental_id = db.Column(db.Integer, primary_key=True)  # Идентификатор аренды
    user_id = db.Column(db.Integer, db.ForeignKey('client.client_id'), nullable=False)  # Ссылка на клиента
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)  # Ссылка на машину
    rental_start_date = db.Column(db.DateTime, nullable=False)  # Дата начала аренды
    rental_end_date = db.Column(db.DateTime)  # Дата окончания аренды
    rental_cost = db.Column(db.Numeric(12, 2), nullable=True)  # Стоимость аренды
    tariff_id = db.Column(db.Integer, db.ForeignKey('tariff.tariff_id'), nullable=False)  # Ссылка на тариф

    client = db.relationship('Client', backref='rentals', lazy=True)
    car = db.relationship('Car', backref='rentals', lazy=True)
    tariff = db.relationship('Tariff', backref='rentals', lazy=True)

    def __repr__(self):
        return f'<Rental {self.rental_id}>'

# Модель Tariff для тарифов
class Tariff(db.Model):
    tariff_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    cost_per_minute = db.Column(db.Numeric(10, 2), nullable=False)  # Стоимость за минуту
    cost_per_hour = db.Column(db.Numeric(10, 2), nullable=False)  # Стоимость за час
    conditions = db.Column(db.Text, nullable=True)

# Модель Client для клиентов
class Client(db.Model, UserMixin):
    client_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    passport_details = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Client {self.full_name}>'

    # Flask-Login methods
    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.client_id)

    def get_role(self):
        return "client"

# Модель Payment для платежей
class Payment(db.Model):
    payment_id = db.Column(db.Integer, primary_key=True)
    rental_id = db.Column(db.Integer, db.ForeignKey('rental.rental_id'), nullable=False)  # Внешний ключ на аренду
    payment_date = db.Column(db.DateTime, nullable=False)
    payment_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False)

    def __init__(self, rental_id, payment_date, payment_amount, status):
        self.rental_id = rental_id
        self.payment_date = payment_date
        self.payment_amount = payment_amount
        self.status = status

# Модель Maintenance для обслуживания машин
class Maintenance(db.Model):
    maintenance_id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    maintenance_date = db.Column(db.DateTime, nullable=False)
    maintenance_type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    notes = db.Column(db.String(200))

    def __repr__(self):
        return f'<Maintenance {self.maintenance_id}: Car {self.car_id}>'

# Модель Admin для администраторов
class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    admin_password = db.Column(db.String(255), nullable=False)  

    def set_password(self, password):
        self.admin_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.admin_password, password)


class Support(db.Model):
    __tablename__ = 'support'

    id = db.Column(db.Integer, primary_key=True)  # Идентификатор
    user_name = db.Column(db.String(100), unique=True, nullable=False)  # Имя пользователя
    password = db.Column(db.String(200), nullable=False)  
    email = db.Column(db.String(100), unique=True, nullable=False)  # Электронная почта
    full_name = db.Column(db.String(100), nullable=False)  # Полное имя
    phone = db.Column(db.String(20))  # Телефон
    role = db.Column(db.String(50), nullable=False, default='Support')  # Роль

    def __repr__(self):
        return f'<Support {self.user_name}>'
    # Flask-Login requires the following methods
    @property
    def is_active(self):
        # Return True or False based on whether the user is active
        return True  # Modify based on your actual logic (e.g., check if the account is enabled)

    def get_id(self):
        return str(self.id)  # This is how Flask-Login retrieves the user's ID

    @property
    def is_authenticated(self):
        return True  # Modify if you have a custom check for authentication

    @property
    def is_anonymous(self):
        return False  # Modify if you allow anonymous users