from flask import Blueprint, request, jsonify
from app.models import db
from app.models.category import Category
from app.models.questions import Question
from app.schemas.questions import MessageResponse, QuestionResponse, QuestionCreate, CategoryBase
from pydantic import ValidationError



questions_bp = Blueprint('questions', __name__, url_prefix='/questions')


@questions_bp.route('/', methods=['GET'])
def get_questions():
    questions = Question.query.all()
    questions_data = [
        {
            **QuestionResponse.model_validate(q).model_dump(),
            "category": CategoryBase.model_validate(q.category).model_dump() if q.category else None
        }
        for q in questions
    ]
    return jsonify(questions_data), 200


@questions_bp.route('/<int:question_id>', methods=['GET'])
def get_question(question_id):
    question = Question.query.get(question_id)
    if not question:
        return jsonify({"error": "Question not found"}), 404
    return jsonify(QuestionResponse.model_validate(question).model_dump()), 200


@questions_bp.route('/', methods=['POST'])
def create_question():
    data = request.get_json()

    try:
        question_data = QuestionCreate(**data)
    except ValidationError as e:
        return jsonify(e.errors()), 400

    category_id = question_data.category_id
    category = Category.query.get(category_id)

    if not category:
        return jsonify({"error": "Invalid category_id"}), 400

    question = Question(text=question_data.text, category_id=category_id)
    db.session.add(question)
    db.session.commit()

    return jsonify(MessageResponse(message="Question created", id=question.id).model_dump()), 201


@questions_bp.route('/<int:question_id>', methods=['PUT'])
def update_question(question_id):
    data = request.get_json()
    print("Received data:", data)
    if not data:
        return jsonify({"error": "Invalid JSON body"}), 400

    question = Question.query.get(question_id)
    if not question:
        return jsonify({"error": "Question not found"}), 404

    if "text" in data and data["text"]:
        question.text = data["text"]

    if "category_id" in data and data["category_id"] is not None:
        try:
            category_id = int(data["category_id"])
        except (ValueError, TypeError):
            return jsonify({"error": "category_id must be an integer"}), 400

        category = Category.query.get(category_id)
        if not category:
            return jsonify({"error": "Invalid category_id"}), 400

        question.category_id = category_id

    db.session.commit()
    return jsonify(MessageResponse(message="Question updated", id=question.id).model_dump()), 200


@questions_bp.route('/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    from app.models.responses import Response
    question = Question.query.get(question_id)
    if not question:
        return jsonify({"error": "Question not found"}), 404

    Response.query.filter_by(question_id=question_id).delete()

    db.session.delete(question)
    db.session.commit()
    return jsonify(MessageResponse(message=f"Question {question_id} deleted").model_dump()), 200


@questions_bp.route("/categories", methods=["POST"])
def create_category():
    data = request.get_json()
    if not data or not data.get("name"):
        return jsonify({"error": "Category name is required"}), 400

    existing_category = Category.query.filter_by(name=data["name"]).first()
    if existing_category:
        return jsonify({"error": "Category already exists"}), 400

    category = Category(name=data["name"])
    db.session.add(category)
    db.session.commit()
    return jsonify(MessageResponse(message="Category created", id=category.id).model_dump()), 201


@questions_bp.route("/categories", methods=["GET"])
def get_categories():
    categories = Category.query.all()
    return jsonify([{"id": c.id, "name": c.name} for c in categories]), 200


@questions_bp.route("/categories/<int:category_id>", methods=["PUT"])
def update_category(category_id):
    data = request.get_json()
    if not data or not data.get("name"):
        return jsonify({"error": "Category name is required"}), 400

    category = Category.query.get(category_id)
    if not category:
        return jsonify({"error": "Category not found"}), 404

    category.name = data["name"]
    db.session.commit()

    return jsonify({"message": f"Category {category_id} updated", "category": {"id": category.id, "name": category.name}}), 200




@questions_bp.route("/categories/<int:category_id>", methods=["DELETE"])
def delete_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return jsonify({"error": "Category not found"}), 404

    from app.models.responses import Response
    from app.models.questions import Question


    questions_to_delete = Question.query.filter_by(category_id=category_id).all()


    for question in questions_to_delete:
        db.session.query(Response).filter(Response.question_id == question.id).delete()


    db.session.query(Question).filter(Question.category_id == category_id).delete()


    db.session.delete(category)
    db.session.commit()

    return jsonify({"message": f"Category {category_id} deleted"}), 200
