from flask_wtf import FlaskForm
from sqlalchemy.orm import defaultload
from sqlalchemy.sql.expression import select
from sqlalchemy.sql.functions import user
from werkzeug.utils import validate_arguments
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField,SelectField,DateField
from wtforms import validators,TextAreaField,URLField
from wtforms.validators import ValidationError, DataRequired, EqualTo
from wtforms.validators import DataRequired,Length
from app.models import *


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    forename = StringField('Фамилия', validators=[DataRequired()])
    surname = StringField('Имя', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = Customers.query.filter_by(login=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

class AddHeroForm(FlaskForm):
    namehero = StringField('HeroName', validators=[DataRequired()])
    strength = IntegerField('Strength', validators=[DataRequired()])
    dexterity =  IntegerField('dexterity', validators=[DataRequired()])
    physique =  IntegerField('physique', validators=[DataRequired()])
    intelligence =  IntegerField('intelligence', validators=[DataRequired()])
    wisdom = IntegerField('wisdom', validators=[DataRequired()])
    charisma =  IntegerField('charisma', validators=[DataRequired()])
    classhero = SelectField('classhero', validators=[DataRequired()], choices=[('bard', 'Бард'),
    ('Barbarian', 'Варвар'), ('Fighter', 'Воин'),("Wizard","Волшебник"),("Druid","Друид"),("Cleric","Жнец"),
    ('Artificer', 'Изобретатель'), ('Warlock', 'Колдун'),("Monk","Монах"),("Paladin","Паладин"),
    ("Rogue","Плут"),("Ranger","Следопыт"),("Sorcerer","Чародей")
    ])
    herolevel =  IntegerField('Herolevel', validators=[DataRequired()])
    submit = SubmitField('CreateHero')
    def validate_namehero(self, namehero):
        user = Hero.query.filter_by(namehero=namehero.data).first()
        if user is not None:
            raise ValidationError('Please use a different heroname.')

class AddBookForm(FlaskForm):
    namebook = StringField('Namebook', validators=[DataRequired()])
    submit = SubmitField('CreateBook')
    def validate_namebook(self, namebook):
        book = Book.query.filter_by(namebook=namebook.data).first()
        if book is not None:
            raise ValidationError('Please use a different namebook.')

class AddSkillForm(FlaskForm):
    skill = StringField('Skill', validators=[DataRequired()])
    discription = TextAreaField('discription', validators=[DataRequired(),Length(max=1500)])
    skilllevel=IntegerField('dexterity', validators=[DataRequired()])
    submit = SubmitField('CreateSkill')
    def validate_skill(self, skill):
        skill = Skill.query.filter_by(skill=skill.data).first()
        if skill is not None:
            raise ValidationError('Please use a different skill.')

class AddPlaceForm(FlaskForm):
    place = IntegerField('Place', validators=[DataRequired()])
    submit = SubmitField('CreatePlace')
    def validate_namebook(self, place):
        places = Place.query.filter_by(place=place.data).first()
        if places is not None:
            raise ValidationError('Please use a different place.')

class AddNewsForm(FlaskForm):
    title=StringField("Title",validators=[DataRequired()])
    discription = TextAreaField('discription', validators=[DataRequired(),Length(max=1500)])
    submit = SubmitField('CreateNews')
    def validate_title(self, title):
        titeles = News.query.filter_by(title=title.data).first()
        if titeles is not None:
            raise ValidationError('Please use a different title.')

class GiveRoleForm(FlaskForm):
    namerole=SelectField('namerole',validators=[DataRequired()], choices=[('Dangeon_master', 'Мастер')])
    user =  SelectField("Выберите имя пользователя, которому вы хотите выдать роль",validators=[DataRequired()])
    submit = SubmitField('GiveRole')
    def validate_user(self,user):
        titeles = Customers.query.filter_by(login=user.data).first()
        if titeles is None:
            raise ValidationError('Такого пользователя не существует')
        roleusers=RoleUser.query.filter_by(login=user.data,namerole='Dangeon_master').first()    
        if roleusers is not None:
            raise ValidationError('Данный пользователь уже является мастером')

class ViewMoreInfoHeroForm(FlaskForm):
    namehero=SelectField('Выберите персонажа, о котором хотите юзнать больше',validators=[DataRequired()])
    submit=SubmitField('SeeMoreinfo')
    def validate_namehero(self,namehero):
        heroes = Hero.query.filter_by(namehero=namehero.data).first()
        if heroes is None:
            raise ValidationError('Такого героя не существует')
        
class InfoHero(FlaskForm):
    strength = IntegerField('Strength', validators=[DataRequired()])
    dexterity =  IntegerField('dexterity', validators=[DataRequired()])
    physique =  IntegerField('physique', validators=[DataRequired()])
    intelligence =  IntegerField('intelligence', validators=[DataRequired()])
    wisdom = IntegerField('wisdom', validators=[DataRequired()])
    charisma =  IntegerField('charisma', validators=[DataRequired()])
    herolevel =  IntegerField('Herolevel', validators=[DataRequired()])
    submit = SubmitField('EditHero')

class AddCompanyForm(FlaskForm):
    namecompany = StringField('Company', validators=[DataRequired()])
    dangeonmaster=SelectField('Dangeon_master',validators=[DataRequired()])
    discription = TextAreaField('discription', validators=[DataRequired(),Length(max=500)])
    submit = SubmitField('CreateCompany')
    def validate_dangeonmaster(self,dangeonmaster):
        titeles = RoleUser.query.filter_by(login=dangeonmaster.data,namerole='Dangeon_master').first()
        if titeles is None:
            raise ValidationError('Такого пользователя не существует')
    def validate_namecompany(self,namecompany):
        company = Company.query.filter_by(namecompany=namecompany.data).first()
        if company is not None:
            raise ValidationError('Такая компания уже существует')

class AddBookCompanyForm(FlaskForm):
    namecompany = SelectField('Company', validators=[DataRequired()])
    namebook = SelectField('Namebook', validators=[DataRequired()])
    submit = SubmitField('AddBook')
    def validate_namecompany(self,namecompany):
        company = Company.query.filter_by(namecompany=namecompany.data).first()
        if company is None:
            raise ValidationError('Такая компания не существует')
        #namebook=namebook.data
        #bookcompany=BookCompany.query.filter_by(namecompany=namecompany.data, namebook=namebook.data).first()    
        #if bookcompany is not None:
        #    raise ValidationError('Данный пользователь уже является мастером')

class AddPlayerInCompanyForm(FlaskForm):
    namecompany = SelectField('Company', validators=[DataRequired()])
    player =  SelectField("Выберите имя пользователя, которого вы хотите добавить в компанию",validators=[DataRequired()])
    submit = SubmitField('AddPlayer')
    def validate_user(self,player):
        titeles = Customers.query.filter_by(login=user.data).first()
        if titeles is None:
            raise ValidationError('Такого пользователя не существует')
    def validate_namecompany(self,namecompany):
        company = Company.query.filter_by(namecompany=namecompany.data).first()
        if company is None:
            raise ValidationError('Такая компания не существует')

class AddPlayForm(FlaskForm):
    namecompany = SelectField('Company', validators=[DataRequired()])
    numberroom =  SelectField("Выберите место проведения",validators=[DataRequired()])
    datet=DateField('Выберите дату',validators=[DataRequired()])
    submit = SubmitField('AddPlay')
    def validate_numberroom(self,numberroom):
        titeles = Place.query.filter_by(numberroom=numberroom.data).first()
        if titeles is None:
            raise ValidationError('Такого пользователя не существует')
    def validate_namecompany(self,namecompany):
        company = Company.query.filter_by(namecompany=namecompany.data).first()
        if company is None:
            raise ValidationError('Такая компания не существует')

class AddPlayerPlayForm(FlaskForm):
    login = SelectField('Customers', validators=[DataRequired()])
    idgame =  SelectField("Выберите № игры",validators=[DataRequired()])
    submit = SubmitField('AddPlayer')
    def validate_login(self,login):
        titeles = Customers.query.filter_by(login=login.data).first()
        if titeles is None:
            raise ValidationError('Такого пользователя не существует')
    def validate_idgame(self,idgame):
        idgames = Play.query.filter_by(id=idgame.data).first()
        if idgames is None:
            raise ValidationError('Такая компания не существует')

class GiveArtefact(FlaskForm):  
    namehero = SelectField('Имя персонажа', validators=[DataRequired()])
    artefact =  StringField("Artefact",validators=[DataRequired()])
    discription = TextAreaField('discription',validators=[DataRequired()])
    submit = SubmitField('GiveArtefact')
    def validate_namehero(self,namehero):
        titeles = Hero.query.filter_by(namehero=namehero.data).first()
        if titeles is None:
            raise ValidationError('Такого пользователя не существует')
    def validate_artefact(self,artefact):
        artefacts = Artefact.query.filter_by(artefactname=artefact.data).first()
        if artefacts is not None:
            raise ValidationError('Такой артефакт уже выдан')

class AddSkillHeroForm(FlaskForm):
    skill=SelectField('Skill',validators=[DataRequired()])
    submit = SubmitField('AddSkill')
    def validate_skill(self, skill):
        skills = Skill.query.filter_by(skill=skill.data).first()
        if skills is None:
            raise ValidationError('Такой скилл уже есть у персонажа')

class EditorForm(FlaskForm):
    namecompany=SelectField('Company',validators=[DataRequired()])
    submit=SubmitField('SeeMoreInfoCompany')
    def validate_namecompany(self, namecompany):
        skills = Company.query.filter_by(namecompany=namecompany.data).first()
        if skills is None:
            raise ValidationError('Такой компании нет')

class EditCompanyForm(FlaskForm):
    discription = TextAreaField('discription', validators=[DataRequired(),Length(max=500)])
    submit=SubmitField('Update_company')
