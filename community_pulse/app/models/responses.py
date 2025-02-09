from app.models import db

class Response(db.Model):
    __tablename__ = 'response'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    responses = db.relationship('Response', backref='question', lazy='joined')
    is_agree = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'Statistic for Question {self.question_id}: {self.agree_count} agree, {self.disagree_count} disagree'
