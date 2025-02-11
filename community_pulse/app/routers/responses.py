from flask import Blueprint, request, jsonify
from app.models.responses import Response
from app.models.questions import Question, Statistic
from app.models import db


responses_bp = Blueprint('responses', __name__, url_prefix='/responses')

@responses_bp.route('/', methods=['POST'])
def add_response():
    data = request.get_json()
    if not data or 'question_id' not in data or 'is_agree' not in data:
        return jsonify({'error': 'Data is not provided'}), 400

    question = Question.query.get(data['question_id'])
    if not question:
        return jsonify({'error': 'Question not found'}), 400

    response = Response(
        question_id=question.id,
        is_agree=data['is_agree']
    )
    db.session.add(response)
    db.session.commit()

    statistics = Statistic.query.get(question.id)
    if not statistics:
        statistics = Statistic(
            question_id=question.id,
            agree_count=0,
            disagree_count=0
        )
        db.session.add(statistics)

    if data['is_agree']:
        statistics.agree_count += 1
    else:
        statistics.disagree_count += 1

    db.session.commit()

    return jsonify({'message': f'Answer to question number {question.id} saved'}), 201


@responses_bp.route('/', methods=['GET'])
def get_responses():
    statistics = Statistic.query.all()
    responses_data = [
        {
            'question_id': stat.question_id,
            'agree_count': stat.agree_count,
            'disagree_count': stat.disagree_count
        }
        for stat in statistics
    ]
    return jsonify(responses_data)