from flask import Blueprint, request, jsonify
from app.models import db
from app.models.category import Category
from app.models.questions import Question  # Додаємо імпорт Question

questions_bp = Blueprint('questions', __name__, url_prefix='/questions')

@questions_bp.route('/', methods=['GET'])
def get_questions():
    questions = Question.query.all()
    return jsonify([{"id": q.id, "text": q.text, "category_id": q.category_id} for q in questions]), 200

@questions_bp.route('/<int:question_id>', methods=['GET'])
def get_question(question_id):
    question = Question.query.get(question_id)
    if not question:
        return jsonify({"error": "Question not found"}), 404
    return jsonify({"id": question.id, "text": question.text, "category_id": question.category_id}), 200

@questions_bp.route('/', methods=['POST'])
def create_question():
    data = request.json
    if not data or "text" not in data or "category_id" not in data:
        return jsonify({"error": "Question text and category_id are required"}), 400

    category = Category.query.get(data["category_id"])
    if not category:
        return jsonify({"error": "Invalid category_id"}), 400

    question = Question(text=data["text"], category_id=data["category_id"])
    db.session.add(question)
    db.session.commit()
    return jsonify({"message": "Question created", "question": {"id": question.id, "text": question.text}}), 201

@questions_bp.route('/<int:question_id>', methods=['PUT'])
def update_question(question_id):
    data = request.json
    question = Question.query.get(question_id)
    if not question:
        return jsonify({"error": "Question not found"}), 404

    if "text" in data:
        question.text = data["text"]
    if "category_id" in data:
        category = Category.query.get(data["category_id"])
        if not category:
            return jsonify({"error": "Invalid category_id"}), 400
        question.category_id = data["category_id"]

    db.session.commit()
    return jsonify({"message": "Question updated", "question": {"id": question.id, "text": question.text}}), 200

@questions_bp.route('/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    question = Question.query.get(question_id)
    if not question:
        return jsonify({"error": "Question not found"}), 404

    db.session.delete(question)
    db.session.commit()
    return jsonify({"message": f"Question {question_id} deleted"}), 200

@questions_bp.route("/categories", methods=["POST"])
def create_category():
    data = request.json
    if not data or "name" not in data:
        return jsonify({"error": "Category name is required"}), 400

    category = Category(name=data["name"])
    db.session.add(category)
    db.session.commit()
    return jsonify({"message": "Category created", "category": {"id": category.id, "name": category.name}}), 201

@questions_bp.route("/categories", methods=["GET"])
def get_categories():
    categories = Category.query.all()
    return jsonify([{"id": c.id, "name": c.name} for c in categories]), 200
