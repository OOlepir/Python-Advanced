from app.models import db

class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    category = db.relationship('Category', back_populates='questions')


    responses = db.relationship("Response", backref="question", cascade="all, delete", lazy="dynamic")

    def __repr__(self):
        return f'Question(id={self.id}, text={self.text})'

class Statistic(db.Model):
    __tablename__ = 'statistics'
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete="CASCADE"), primary_key=True)
    agree_count = db.Column(db.Integer, nullable=False, default=0)
    disagree_count = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f'<Statistic(question_id={self.question_id}, agree={self.agree_count}, disagree={self.disagree_count})>'
