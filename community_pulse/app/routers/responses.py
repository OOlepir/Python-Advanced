from flask import Blueprint

responses_bp = Blueprint('responses', __name__, url_prefix='/responses')

@responses_bp.route('/', methods=['POST'])
def add_response():
    return 'Ответ добавлен'


@responses_bp.route('/', methods=['GET'])
def get_responses():
    return  "Статистика всех ответов"