from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    age = db.Column(db.Integer, unique=False, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    favorite_planet = db.relationship('FavoritePlanet', backref='user')
    favorite_people = db.relationship('FavoritePeople', backref='user')
    favorite_starship = db.relationship('FavoriteStarship', backref='user')

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "email": self.email,
            "favorite_planet": self.favorite_planet,
            "favorite_people": self.favorite_people,
            "favorite_starship": self.favorite_starship
            # do not serialize the password, its a security breach
        }     
    
class FavoritePlanet(db.Model):
    __tablename__ = 'favoriteplanet'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'),nullable=False)
    

    def __repr__(self):
        return '<FavoritePlanet %r>' % self.user_id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            
            # do not serialize the password, its a security breach
        }    

class FavoritePeople(db.Model):
    __tablename__ = 'favoritepeople'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'),nullable=False)
    

    def __repr__(self):
        return '<FavoritePeople %r>' % self.user_id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id,
            
            # do not serialize the password, its a security breach
        }      
    
class FavoriteStarship(db.Model):
    __tablename__ = 'favoritestarship'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    starship_id = db.Column(db.Integer, db.ForeignKey('starship.id'),nullable=False)
    

    def __repr__(self):
        return '<FavoriteStarship %r>' % self.user_id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "starship_id": self.starship_id,
            
            # do not serialize the password, its a security breach
        }   
    
class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    url = db.Column(db.String(80),nullable=False)
    population = db.Column(db.Integer, nullable=False)
    diameter = db.Column(db.Integer,nullable=False)
    terrain = db.Column(db.String(80),nullable=False)
    favorite_planet = db.relationship('FavoritePlanet', backref='planet')


    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "terrain": self.terrain,
            "population": self.population,
            "favorite_planet": self.favorite_planet
            # do not serialize the password, its a security breach
        }    
     
class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    url = db.Column(db.String(80),  nullable=False)
    age = db.Column(db.Integer, nullable=False)
    favorite_people = db.relationship('FavoritePeople', backref='people')


    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "uid": self.id,
            "name": self.name,
            "favorite_people": self.favorite_people
            # do not serialize the password, its a security breach
        }    

   
class Starship(db.Model):
    __tablename__ = 'starship'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    url = db.Column(db.String(80), nullable=False)
    passengers = db.Column(db.Integer, nullable=False)
    favorite_starship = db.relationship('FavoriteStarship', backref='starship')


    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "uid": self.id,
            "name": self.name,
            "favorite_starship": self.favorite_starship
            # do not serialize the password, its a security breach
        } 
   
       
    