from datetime import date
from html.entities import name2codepoint
from logging import log
from flask import request
from os import name
import re
from flask import render_template, flash, redirect, url_for
from sqlalchemy.orm import query
from sqlalchemy.sql.functions import current_time, current_timestamp
from werkzeug.utils import validate_arguments
from wtforms.fields import choices
from app import app
from app.forms import *
from .models import Book, Customers, Hero, RoleUser
from app import Dnd
from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    abort,
    redirect,
    url_for,
    current_app,
)
from flask_login import current_user, login_user,logout_user, login_required
from werkzeug.urls import url_parse

@app.route('/')
#def base():
#    if not current_user.is_anonymous:
#        roles=Dnd.session.query(RoleUser.namerole).filter_by(login=current_user.login).all()
#        role=[i[0] for i in roles]
#        role_user=[]
#        role_user_dangeon_master=[]
#        role_user_admin=[]
#        for i in role:
#            if i=="Dangeon_master":
#                role_user_dangeon_master= '<a href='+"{{url_for('editor') }}"+'>Admin</a>'
#            elif i=="Admin":
#                role_user_admin='<html><a href='+"{{url_for('admin') }}"+'>Editor</a></html>'
#            else:
#                role_user="Player"
#        print(role_user_dangeon_master)
#        print(role_user_admin)
#        return render_template('base.html', role_user=role_user,role_user_admin=role_user_admin,role_user_dangeon_master=role_user_dangeon_master)
#    return redirect(url_for('login'))
@app.route('/index')
@login_required
def index():
    #roles=Dnd.session.query(RoleUser.namerole).filter_by(login=current_user.login).all()
    #role=[i[0] for i in roles]
    #role_user=False
    #role_user_dangeon_master=False
    #role_user_admin=False
    #for i in role:
    #    if i=="Dangeon_master":
    #        role_user_angeon_master=True
    #    elif i=="Admin":
    #        role_user_admin=True
    #    else:
    #        role_user="Player"
    news=News.query.all()
    return render_template('index.html', title='Home', news=news)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Customers.query.filter_by(login=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Customers(login=form.username.data,forename=form.forename.data,surname=form.surname.data)
        user.set_password(form.password.data)
        Dnd.session.add(user)
        role=RoleUser(login=form.username.data,namerole='Player')
        Dnd.session.add(role)
        Dnd.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<login>/addhero', methods=['GET', 'POST'])
def addhero(login):
    form = AddHeroForm()
    if form.validate_on_submit():
        hero = Hero(namehero=form.namehero.data, 
        strength=form.strength.data, 
        dexterity=form.dexterity.data,
        wisdom=form.wisdom.data,
        physique=form.physique.data,
        intelligence=form.intelligence.data,
        classhero=form.classhero.data, 
        charisma=form.charisma.data,
        herolevel=form.herolevel.data,
        login=login)
        print(hero)
        Dnd.session.add(hero)
        Dnd.session.commit()
        flash('Congratulations, you are add new hero!')
        return redirect(url_for('login'))
    return render_template('addHero.html', title='Addhero', form=form)


@app.route('/user/<login>', methods=['GET','POST'])
@login_required
def user(login):
    form = ViewMoreInfoHeroForm()
    user = Customers.query.filter_by(login=login).first_or_404()
    heroes = Dnd.session.query(Hero.namehero).filter_by(login=login)
    all_heroes=heroes.all()
    heroes_user=[i[0] for i in all_heroes]
    form.namehero.choices=heroes_user
    namehero=form.namehero.data
    print(namehero)
    if form.validate_on_submit():
        return redirect(url_for('infohero',login=login,namehero=namehero))
    return render_template('user.html',title='Profile', user=user, form=form )


@app.route('/user/<login>/<namehero>', methods=['GET','POST'])
@login_required
def infohero(namehero,login):
    print('///////////////')
    print(namehero)
    #hero_user=Hero.query.filter_by(namehero=namehero).all()
    hero_user=Hero.query.get_or_404(namehero)
    skills=Dnd.session.query(SkillHero.skill).filter_by(namehero=namehero).all()
    artefacts=Dnd.session.query(Artefact.artefactname).filter_by(namehero=namehero).all()
    print(skills)
    form=InfoHero()
    if form.validate_on_submit():
        hero_user.strength= form.strength.data
        hero_user.dexterity= form.dexterity.data
        hero_user.physique=form.physique.data
        hero_user.intelligence=form.intelligence.data
        hero_user.wisdom=form.wisdom.data
        hero_user.charisma=form.charisma.data
        hero_user.herolevel=form.herolevel.data
        Dnd.session.commit()
        return redirect(url_for('user',login=login))
    form.strength.data=hero_user.strength
    form.dexterity.data=hero_user.dexterity
    form.physique.data=hero_user.physique
    form.intelligence.data=hero_user.intelligence
    form.wisdom.data=hero_user.wisdom
    form.charisma.data=hero_user.charisma
    form.herolevel.data=hero_user.herolevel
    return render_template('hero.html',title='Hero',form=form,hero=hero_user,skills=skills,artefacts=artefacts)


@app.route('/user/<login>/<namehero>/addskillhero', methods=['GET','POST'])
def addskillhero(namehero,login):
    form=AddSkillHeroForm()
    skills = Dnd.session.query(Skill.skill)
    all_skills=skills.all()
    skill_user=[i[0] for i in all_skills]
    form.skill.choices=skill_user
    skillhero= SkillHero.query.filter_by(namehero=namehero,skill=form.skill.data).first()
    if skillhero is not None:
        flash('У этого персонажа уже есть этот скилл')
        return redirect(url_for('addskillhero',login=login,namehero=namehero))
    if form.validate_on_submit():
        skill = SkillHero(namehero=namehero,skill=form.skill.data)
        Dnd.session.add(skill)
        Dnd.session.commit()
        flash('Congratulations, you are add new Skill!')
        return redirect(url_for('user',login=login))
    return render_template('addskillhero.html', title='AddSkillHero',form=form,login=login,namehero=namehero)
    

@app.route('/admin',methods=['GET','POST'])
@login_required
def admin():
    admin=RoleUser.query.filter_by(login=current_user.login).first_or_404()
    if admin.namerole =='Admin':
        form=EditorForm()
        company = Dnd.session.query(Company.namecompany)
        all_company=company.all()
        companys_user=[i[0] for i in all_company]
        form.namecompany.choices=companys_user
        if form.validate_on_submit():
            print(form.namecompany.data)
            return redirect(url_for('infocompany',namecompany=form.namecompany.data)) 
        return render_template('admin.html',form=form)
    else:
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/admin/addplace', methods=['GET', 'POST'])
def addplace():
    form = AddPlaceForm()
    if form.validate_on_submit():
        place = Place(numberroom=form.place.data) 
        Dnd.session.add(place)
        Dnd.session.commit()
        flash('Congratulations, you are add new Place!')
        return redirect(url_for('admin'))
    return render_template('addplace.html', title='Addplace',form=form)


@app.route('/admin/addskill', methods=['GET', 'POST'])
def addskill():
    form = AddSkillForm()
    if form.validate_on_submit():
        skill = Skill(skill=form.skill.data,discription=form.discription.data,skilllevel=form.skilllevel.data) 
        Dnd.session.add(skill)
        Dnd.session.commit()
        flash('Congratulations, you are add new Skill!')
        return redirect(url_for('admin'))
    return render_template('addskill.html', title='Addskill', form=form)


@app.route('/admin/addbook', methods=['GET', 'POST'])
def addbook():
    form = AddBookForm()
    if form.validate_on_submit():
        book = Book(namebook=form.namebook.data) 
        Dnd.session.add(book)
        Dnd.session.commit()
        flash('Congratulations, you are add new book!')
        return redirect(url_for('admin'))
    return render_template('addbook.html', title='Addbook', form=form)


@app.route('/admin/addnews', methods=['GET', 'POST'])
def addnews():
    form = AddNewsForm()
    date=datetime.utcnow()
    if form.validate_on_submit():
        news = News(title=form.title.data,discription=form.discription.data,login=current_user.login,datet=date) 
        Dnd.session.add(news)
        Dnd.session.commit()
        flash('Congratulations, you are add new News!')
        return redirect(url_for('admin'))
    return render_template('addnews.html', title='Addnews', form=form)


@app.route('/admin/giverole', methods=['GET', 'POST'])
def giverole():
    form = GiveRoleForm()
    user_ids = Dnd.session.query(Customers.login)
    all_ids = user_ids.all()
    users=[i[0] for i in all_ids]
    form.user.choices=users
    if form.validate_on_submit():
        book = RoleUser(login=form.user.data,namerole=form.namerole.data) 
        Dnd.session.add(book)
        Dnd.session.commit()
        flash('Congratulations, you are giverole!', book.login)
        return redirect(url_for('admin'))
    return render_template('giverole.html', title='Giverole', form=form)


@app.route('/admin/addcompanyadmin',methods=['GET','POST'])
def addcompanyadmin():
    form=AddCompanyForm()
    user_ids = Dnd.session.query(RoleUser.login).filter_by(namerole='Dangeon_master')
    #user_ids = Dnd.session.query(Customers.login)
    all_ids = user_ids.all()
    users=[i[0] for i in all_ids]
    form.dangeonmaster.choices=users
    if form.validate_on_submit():
        s=form.namecompany.data
        print(s)
        print('/////////////////')
        book=Company(namecompany=s,discription=form.discription.data,dungeonmaster=form.dangeonmaster.data)
        Dnd.session.add(book)
        Dnd.session.commit()
        flash('Congratulations, you are create company!')
        return redirect(url_for('admin'))
    return render_template('addcompany.html', title='AddCompany', form=form)


@app.route('/admin/addplayeradmin',methods=['GET','POST'])
def addplayeradmin():
    form = AddPlayerInCompanyForm()
    company = Dnd.session.query(Company.namecompany)
    all_company=company.all()
    company_user=[i[0] for i in all_company]
    form.namecompany.choices=company_user
    user_ids = Dnd.session.query(Customers.login)
    all_ids = user_ids.all()
    users=[i[0] for i in all_ids]
    form.player.choices=users
    playercompany=CustomersCompany.query.filter_by(namecompany=form.namecompany.data, login=form.player.data).first()  
    if playercompany is not None:
        flash('Данный игрок уже добавлена в компанию')
        return redirect(url_for('addplayeradmin'))
    if form.validate_on_submit():
        player = CustomersCompany(login=form.player.data,namecompany=form.namecompany.data) 
        Dnd.session.add(player)
        Dnd.session.commit()
        flash('Congratulations, you are add new player in company!')
        return redirect(url_for('admin'))
    return render_template('addplayercompany.html', title='AddPlayer', form=form)


@app.route('/admin/infocompany/<namecompany>',methods=['GET','POST'])
def infocompanyadmin(namecompany):
    form=EditCompanyForm()
    discription_company=Company.query.get_or_404(namecompany)
    players=Dnd.session.query(CustomersCompany.login).filter_by(namecompany=namecompany).all()
    if form.validate_on_submit():
        discription_company.discription=form.discription.data
        Dnd.session.commit()
        return redirect(url_for('editor'))
    form.discription.data=discription_company.discription
    return render_template('infocompany.html', title='EditCompany',players=players, form=form,namecompany=namecompany,dangeonmaster=discription_company.dungeonmaster)


@app.route('/editor',methods=['GET','POST'])
@login_required
def editor():
    admin=RoleUser.query.filter_by(login=current_user.login,namerole='Dangeon_master').first()
    if admin==None:
        return redirect(url_for('index'))
    else:
        form=EditorForm()
        company = Dnd.session.query(Company.namecompany).filter_by(dungeonmaster=current_user.login)
        all_company=company.all()
        companys_user=[i[0] for i in all_company]
        form.namecompany.choices=companys_user
        if form.validate_on_submit():
            print(form.namecompany.data)
            return redirect(url_for('infocompany',namecompany=form.namecompany.data)) 
        return render_template('editor.html',title='Editor',form=form)


@app.route('/editor/addcompanyeditor',methods=['GET','POST'])
def addcompanyeditor():
    form=AddCompanyForm()
    user_ids = Dnd.session.query(RoleUser.login).filter_by(login=current_user.login,namerole='Dangeon_master')
    #user_ids = Dnd.session.query(Customers.login)
    all_ids = user_ids.all()
    users=[i[0] for i in all_ids]
    form.dangeonmaster.choices=users
    if form.validate_on_submit():
        s=form.namecompany.data
        print(s)
        print('/////////////////')
        book=Company(namecompany=s,discription=form.discription.data,dungeonmaster=form.dangeonmaster.data)
        Dnd.session.add(book)
        Dnd.session.commit()
        flash('Congratulations, you are create company!')
        return redirect(url_for('editor'))
    return render_template('addcompany.html', title='AddCompany', form=form)


@app.route('/editor/addbook', methods=['GET', 'POST'])
def addbookcompany():
    form = AddBookCompanyForm()
    login=current_user.login
    company = Dnd.session.query(Company.namecompany).filter_by(dungeonmaster=login)
    all_company=company.all()
    company_user=[i[0] for i in all_company]
    form.namecompany.choices=company_user
    book = Dnd.session.query(Book.namebook)
    all_books=book.all()
    book_user=[i[0] for i in all_books]
    form.namebook.choices=book_user
    bookcompany=BookCompany.query.filter_by(namecompany=form.namecompany.data, namebook=form.namebook.data).first()  
    if bookcompany is not None:
        flash('Данная книга уже добавлена в компанию')
        return redirect(url_for('addbookcompany'))
    if form.validate_on_submit():
        book = BookCompany(namebook=form.namebook.data,namecompany=form.namecompany.data) 
        Dnd.session.add(book)
        Dnd.session.commit()
        flash('Congratulations, you are add new book in company!')
        return redirect(url_for('editor'))
    return render_template('addbookcompany.html', title='Addbook', form=form)


@app.route('/editor/addplayer', methods=['GET', 'POST'])
def addplayercompany():
    form = AddPlayerInCompanyForm()
    login=current_user.login
    company = Dnd.session.query(Company.namecompany).filter_by(dungeonmaster=login)
    all_company=company.all()
    company_user=[i[0] for i in all_company]
    form.namecompany.choices=company_user
    user_ids = Dnd.session.query(Customers.login)
    all_ids = user_ids.all()
    users=[i[0] for i in all_ids]
    form.player.choices=users
    playercompany=CustomersCompany.query.filter_by(namecompany=form.namecompany.data, login=form.player.data).first()  
    if playercompany is not None:
        flash('Данный игрок уже добавлена в компанию')
        return redirect(url_for('addplayercompany'))
    if form.validate_on_submit():
        player = CustomersCompany(login=form.player.data,namecompany=form.namecompany.data) 
        Dnd.session.add(player)
        Dnd.session.commit()
        flash('Congratulations, you are add new player in company!')
        return redirect(url_for('editor'))
    return render_template('addplayercompany.html', title='AddPlayer', form=form)


@app.route('/editor/addplay',methods=['GET','POST'])
def addplay():
    form = AddPlayForm()
    login=current_user.login
    room = Dnd.session.query(Place.numberroom)
    all_room=room.all()
    rooms=[i[0] for i in all_room]
    form.numberroom.choices=rooms
    company = Dnd.session.query(Company.namecompany).filter_by(dungeonmaster=login)
    all_company=company.all()
    company_user=[i[0] for i in all_company]
    form.namecompany.choices=company_user
    playcompany=Play.query.filter_by(namecompany=form.namecompany.data, numberroom=form.numberroom.data,datet=form.datet.data).first()
    if playcompany is not None:
        flash('Данная игра с этой комнатой в данное время уже добавлена в таблицу ')
        return redirect(url_for('addplay'))
    if form.validate_on_submit():
        play = Play(namecompany=form.namecompany.data,numberroom=form.numberroom.data,datet=form.datet.data) 
        Dnd.session.add(play)
        Dnd.session.commit()
        flash('Congratulations, you are add play!')
        return redirect(url_for('editor'))
    return render_template('addplay.html', title='AddPlay', form=form)


@app.route('/editor/addplayerplay',methods=['GET','POST'])
def addplayerplay():
    form = AddPlayerPlayForm()
    user_ids = Dnd.session.query(Customers.login)
    all_ids = user_ids.all()
    users=[i[0] for i in all_ids]
    form.login.choices=users
    idgame_ids = Dnd.session.query(Play.id)
    all_idagames = idgame_ids.all()
    idgames=[i[0] for i in all_idagames]
    form.idgame.choices=idgames
    playerplay= CustomersPlay.query.filter_by(login=form.login.data,idgame=form.idgame.data).first()
    if playerplay is not None:
        flash('Данный пользователь уже добавлен в данную игру')
        return redirect(url_for('addplayerplay'))
    if form.validate_on_submit():
        playerplays = CustomersPlay(login=form.login.data,idgame=form.idgame.data) 
        Dnd.session.add(playerplays)
        Dnd.session.commit()
        flash('Congratulations, you are add player id play!')
        return redirect(url_for('editor'))
    return render_template('addplayerplay.html', title='AddPlay', form=form)


@app.route('/editor/giveartefact',methods=['GET','POST'])
def giveartefact():
    form=GiveArtefact()
    hero = Dnd.session.query(Hero.namehero)
    all_hero=hero.all()
    heroes=[i[0] for i in all_hero]
    form.namehero.choices=heroes
    if form.validate_on_submit():
        artefact = Artefact(artefactname=form.artefact.data,namehero=form.namehero.data,discription=form.discription.data) 
        Dnd.session.add(artefact)
        Dnd.session.commit()
        flash('Congratulations, you are give arttefact!')
        return redirect(url_for('editor'))
    return render_template('giveartefact.html', title='GiveArtefact',form=form)


@app.route('/editor/infocompany/<namecompany>',methods=['GET','POST'])
def infocompany(namecompany):
    form=EditCompanyForm()
    discription_company=Company.query.get_or_404(namecompany)
    players=Dnd.session.query(CustomersCompany.login).filter_by(namecompany=namecompany).all()
    if form.validate_on_submit():
        discription_company.discription=form.discription.data
        Dnd.session.commit()
        return redirect(url_for('editor'))
    form.discription.data=discription_company.discription
    return render_template('infocompany.html', title='EditCompany',players=players, form=form,namecompany=namecompany,dangeonmaster=discription_company.dungeonmaster)
    

@app.route('/viewbook',methods=['GET','POST']) 
def viewbook():
    books=Dnd.session.query(Book.namebook)
    return render_template('viewbook.html', title='Viewbook',books=books)   


@app.route('/user/<login>/storygame',methods=['GET','POST']) 
def storygame(login):
    idgames=Dnd.session.query(CustomersPlay.idgame).filter_by(login=login).all()
    print(idgames)
    idgame=[i[0] for i in idgames]
    namegame=[]
    for id in idgame:
        print(id)
        game=Dnd.session.query(Play.namecompany,Play.datet,Play.numberroom).filter_by(id=id).first()
        print(game)
        namegame.append(game)
    print(namegame)
    return render_template('storygame.html', title='storygame',login=login,namegame=namegame)

@app.route('/user/<login>/company')
def mycompany(login):
    companys=Dnd.session.query(CustomersCompany.namecompany).filter_by(login=login).all()
    company=[i[0] for i in companys]
    namegame=[]
    for id in company:
        print(id)
        game=Dnd.session.query(Company.namecompany,Company.dungeonmaster, Company.discription).filter_by(namecompany=id).first()
        print(game)
        namegame.append(game)
    print(namegame)
    return render_template('mycompany.html', title='Mycompany',namegame=namegame)