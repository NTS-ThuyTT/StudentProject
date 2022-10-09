from website import db

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    frstname = db.Column(db.String(100))
    lstname = db.Column(db.String(100))
    email = db.Column(db.String(100))
    birthday = db.Column(db.Date())
    birthplace = db.Column(db.String(1000))
    point = db.Column(db.Integer)
