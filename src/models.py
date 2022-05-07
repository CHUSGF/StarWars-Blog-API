from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class MyModel():
    @classmethod
    def get_by_id(cls, id):
        record = cls.query.get(id)
        return record

class User(db.Model, MyModel):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship("Favorite", backref = "user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }

class People(db.Model, MyModel): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    favorites = db.relationship("Favorite", backref = "people")

    def serialize(self):
        return {     
            "name": self.name,
        }

class Favorite(db.Model, MyModel):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    def serialize(self):
        people = People.get_by_id(self.people_id)
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id,
            "planet_id": self.planet_id,
        }


class Planet(db.Model, MyModel): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    favorites = db.relationship("Favorite", backref = "planet")


    def serialize(self):
        return {     
            "name": self.name,
            "id": self.id,
        }