from app.models import db

class Response(db.Model):
    __tablename__ = "responses"

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete="CASCADE"), nullable=False)
    is_agree = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'Response(question_id={self.question_id}, is_agree={self.is_agree})'
