from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Planet(db.Model, SerializerMixin):
    __tablename__ = 'planets'

    # Add serialization rules
    serialize_rules = ('-missions',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    distance_from_earth = db.Column(db.Integer)
    nearest_star = db.Column(db.String)

    # Add relationship
    missions = db.relationship('Mission', back_populates='planet', cascade='all, delete-orphan')
    scientists = association_proxy('missions', 'scientist')





class Scientist(db.Model, SerializerMixin):
    __tablename__ = 'scientists'

    # Add serialization rules
    serialize_rules = ('-missions.scientist',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    field_of_study = db.Column(db.String, nullable=False)

    # Add relationship
    missions = db.relationship('Mission', back_populates='scientist', cascade='all, delete-orphan')
    planets = association_proxy('missions', 'planet')

        
    @validates('name')
    def validates_name(self, key, new_name):
        if new_name:
            return new_name
        raise ValueError('Name must be included.')
    
    @validates('field_of_study')
    def validate_name(self, key, field_of_study):
        if not field_of_study:
            raise ValueError("Scientist must have a field of study")
        return field_of_study


class Mission(db.Model, SerializerMixin):
    __tablename__ = 'missions'

    # Add serialization rules
    serialize_rules = ('-planet.missions','-scientist.missions')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    scientist_id = db.Column(db.Integer, db.ForeignKey('scientists.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))

    # Add relationships
    planet = db.relationship('Planet', back_populates='missions')
    scientist = db.relationship('Scientist', back_populates='missions')

    # Add validation
    @validates('name')
    def validate_name(self, key, name):
        if name:
            return name
        raise ValueError("Mission must have a name")
        
    
    @validates('scientist_id')
    def validate_scientist_id(self, key, scientist_id):
        if not scientist_id:
            raise ValueError("Mission must have a Scientist ID")
        return scientist_id
    
    @validates('planet_id')
    def validate_planet_id(self, key, planet_id):
        if not planet_id:
            raise ValueError("Mission must have a Planet ID")
        return planet_id


# add any models you may need.
