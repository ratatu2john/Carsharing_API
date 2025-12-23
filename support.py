from flask import Blueprint, render_template
from models import Maintenance

support_bp = Blueprint('support', __name__)

# Страница Dashboard для Support
@support_bp.route('/dashboard')
def support_dashboard():
    return render_template('support_dashboard.html')  # Страница с кнопкой для управления техническим обслуживанием

# Страница для управления техническим обслуживанием
@support_bp.route('/manage_maintenance')
def manage_maintenance():
    maintenances = Maintenance.query.all()  # Получаем все данные о технических обслуживании
    return render_template('support_maintenance.html', maintenances=maintenances)
