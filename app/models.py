import datetime
from logging import log
from flask_login.utils import login_user
from sqlalchemy.sql.functions import current_timestamp
from werkzeug.security import generate_password_hash, check_password_hash
from app import Dnd
from flask_login import UserMixin
from sqlalchemy import func
from app import login
from sqlalchemy.orm import relationship
from datetime import datetime

class Customers(UserMixin,Dnd.Model):
        
    __tablename__ = 'customers'
    id = Dnd.Column(Dnd.Integer, primary_key=True)
    login = Dnd.Column(Dnd.String(),unique=True)
    password = Dnd.Column(Dnd.String())
    surname = Dnd.Column(Dnd.String())
    forename = Dnd.Column(Dnd.String())
    #hero=relationship("hero", backref="customers")
    def __init__(self, login, surname, forename):
        self.login = login
        self.surname =  surname
        self.forename = forename

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, passw):
        return check_password_hash(self.password, passw)

    def __repr__(self):
        return f""

class Roles(Dnd.Model):
    __tablename__ = 'roles'

    namerole = Dnd.Column(Dnd.String(), primary_key=True)

    def __init__(self, namerole):
        self.namerole = namerole

    def __repr__(self):
        return f""

class  RoleUser(Dnd.Model):
    __tablename__ = 'roleuser'
    id = Dnd.Column(Dnd.Integer, primary_key=True)
    namerole = Dnd.Column(Dnd.String(), Dnd.ForeignKey('roles.namerole'), nullable=False, index=True)
    login= Dnd.Column(Dnd.String(), Dnd.ForeignKey('customers.login'), nullable=False, index=True)

    def __init__(self, login, namerole):
        self.login = login
        self.namerole =  namerole

    def __repr__(self):
        return f""

class Hero(Dnd.Model):
    __tablename__ = 'hero'
    namehero = Dnd.Column(Dnd.String(), primary_key=True)
    strength = Dnd.Column(Dnd.Integer,nullable=False)
    dexterity = Dnd.Column(Dnd.Integer,nullable=False)
    physique = Dnd.Column(Dnd.Integer,nullable=False)
    intelligence = Dnd.Column(Dnd.Integer,nullable=False)
    wisdom = Dnd.Column(Dnd.Integer,nullable=False)
    charisma = Dnd.Column(Dnd.Integer,nullable=False)
    classhero = Dnd.Column(Dnd.String(),nullable=False)
    #forename = Dnd.Column(Dnd.String())
    login= Dnd.Column(Dnd.String(), Dnd.ForeignKey('customers.login'), nullable=False, index=True)
    herolevel = Dnd.Column(Dnd.Integer,nullable=False)

    def __init__(self, namehero,strength,dexterity,physique,intelligence,wisdom,charisma,classhero,herolevel,login):
        self.namehero = namehero
        self.strength =  strength
        self.dexterity =  dexterity
        self.physique =  physique
        self.intelligence =  intelligence
        self.wisdom =  wisdom
        self.charisma = charisma
        self.classhero =  classhero
        self.herolevel=herolevel
        self.login=login

    def __repr__(self):
        return f""

class Artefact(Dnd.Model):
    __tablename__ = 'artefact'

    artefactname = Dnd.Column(Dnd.String(), primary_key=True)
    discription = Dnd.Column(Dnd.String(),nullable=False)
    namehero= Dnd.Column(Dnd.String(), Dnd.ForeignKey('hero.namehero'), nullable=False, index=True)

    def __init__(self,artefactname, discription, namehero):
        self.artefactname = artefactname
        self.discription =  discription
        self.namehero =namehero

    def __repr__(self):
        return f""

class Skill(Dnd.Model):
    __tablename__ = 'skill'

    skill = Dnd.Column(Dnd.String(), primary_key=True)
    discription = Dnd.Column(Dnd.String(),nullable=False)
    skilllevel= Dnd.Column(Dnd.Integer, nullable=False)

    def __init__(self,skill, discription, skilllevel):
        self.skill = skill
        self.discription =  discription
        self.skilllevel =skilllevel

    def __repr__(self):
        return f""

class SkillHero(Dnd.Model):
    __tablename__ = 'skillhero'
    id = Dnd.Column(Dnd.Integer, primary_key=True)
    namehero= Dnd.Column(Dnd.String(), Dnd.ForeignKey('hero.namehero'), nullable=False, index=True)
    skill = Dnd.Column(Dnd.String(), Dnd.ForeignKey('skill.skill'), nullable=False, index=True)
    #SkillLevel= Dnd.Column(Dnd.Integer, Dnd.ForeignKey('Skill.SkillLevel'), nullable=False, index=True)

    def __init__(self,skill,  namehero): #, SkillLevel
        self.skill = skill
        #self.SkillLevel =SkillLevel
        self.namehero =namehero

    def __repr__(self):
        return f""

class Place(Dnd.Model):
    __tablename__ = 'place'
    numberroom=Dnd.Column(Dnd.String, primary_key=True)
    
    def __init__(self,numberroom ):
        self.numberroom = numberroom
   

    def __repr__(self):
        return f""

class Company(Dnd.Model):
    __tablename__ = 'company'
    namecompany=Dnd.Column(Dnd.String(), primary_key=True)
    discription = Dnd.Column(Dnd.String())
    dungeonmaster = Dnd.Column(Dnd.String(),Dnd.ForeignKey('customers.login'), nullable=False, index=True)

    def __init__(self,namecompany,discription,dungeonmaster):
        self.namecompany = namecompany
        self.discription = discription
        self.dungeonmaster=dungeonmaster

    def __repr__(self):
        return f""

class Play(Dnd.Model):
    __tablename__ = 'play'

    id = Dnd.Column(Dnd.Integer, primary_key=True)
    numberroom= Dnd.Column(Dnd.String, Dnd.ForeignKey('place.numberroom'), nullable=False, index=True)
    datet = Dnd.Column(Dnd.Date(), nullable=False)
    namecompany= Dnd.Column(Dnd.String(), Dnd.ForeignKey('company.namecompany'), nullable=False, index=True)

    def __init__(self,datet,  numberroom, namecompany):
        self.datet = datet
        self.namecompany =namecompany
        self.numberroom =numberroom

    def __repr__(self):
        return f""

class Book(Dnd.Model):
    __tablename__ = 'book'
    namebook=Dnd.Column(Dnd.String(), primary_key=True)
    
    def __init__(self,namebook ):
        self.namebook = namebook
   

    def __repr__(self):
        return f""

class BookCompany(Dnd.Model):
    __tablename__ = 'bookcompany'
    id = Dnd.Column(Dnd.Integer, primary_key=True)
    namebook= Dnd.Column(Dnd.String(), Dnd.ForeignKey('book.namebook'), nullable=False, index=True)
    namecompany= Dnd.Column(Dnd.String(), Dnd.ForeignKey('company.namecompany'), nullable=False, index=True)

    def __init__(self,  namebook, namecompany):
        self.namecompany =namecompany
        self.namebook =namebook

    def __repr__(self):
        return f""       

class News(Dnd.Model):
    __tablename__ = 'news'

    title = Dnd.Column(Dnd.String(), primary_key=True)
    login= Dnd.Column(Dnd.String(), Dnd.ForeignKey('customers.login'), nullable=False, index=True)
    datet = Dnd.Column(Dnd.Date(),default=datetime.utcnow())
    discription = Dnd.Column(Dnd.String(), nullable=False)

    def __init__(self,  title, login,datet,discription):
        self.login =login
        self.title =title
        self.datet=datet
        self.discription=discription

    def __repr__(self):
        return f""      

class CustomersCompany(Dnd.Model):
    __tablename__ = 'customerscompany'
    id = Dnd.Column(Dnd.Integer, primary_key=True)
    login= Dnd.Column(Dnd.String(), Dnd.ForeignKey('customers.login'), nullable=False, index=True)
    namecompany= Dnd.Column(Dnd.String(), Dnd.ForeignKey('company.namecompany'), nullable=False, index=True)

    def __init__(self,  login, namecompany):
        self.login =login
        self.namecompany =namecompany

    def __repr__(self):
        return f""       

class CustomersPlay(Dnd.Model):

    __tablename__ = 'customersplay'
    id = Dnd.Column(Dnd.Integer, primary_key=True)
    login= Dnd.Column(Dnd.String(), Dnd.ForeignKey('customers.login'), nullable=False, index=True)
    idgame= Dnd.Column(Dnd.Integer, Dnd.ForeignKey('play.id'), nullable=False, index=True)

    def __init__(self,  login, idgame):
        self.login =login
        self.idgame =idgame

    def __repr__(self):
        return f""   


@login.user_loader
def load_user(id):
    return Customers.query.get(int(id))

