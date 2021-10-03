from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_gravatar import Gravatar
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user,logout_user,login_required,LoginManager,UserMixin,current_user
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap
from forms import CreateForm,Createprofile,Createrequest
from functools import wraps
import datetime

import os


UPLOAD_FOLDER = '/portfolio projects/Rental/static/assets/images/upload/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////portfolio projects/Rental/data.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SECRET_KEY'] = 'adadaodkdiqqkdoqoqdoq11215'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
Bootstrap(app)


gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    use_ssl=False,
                    base_url=None)



@login_manager.user_loader
def load_user(user_id):
    return Rents.query.get(int(user_id))






def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('error'))
        elif current_user.id != 1:
            return redirect(url_for('error'))
        return f(*args, **kwargs)
    return decorated_function



class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer,primary_key=True)
    image = db.Column(db.String(100),nullable=False)
    name = db.Column(db.String(100),nullable=False)



db.create_all()
db.session.commit()


class Rents(db.Model, UserMixin):
    __tablename__ = "rents"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100),nullable=False)
    password = db.Column(db.String(100),nullable=False)
    profile = db.relationship("Profile", back_populates="user")
    request = db.relationship("Request", back_populates="user")



db.create_all()
db.session.commit()






class Request(db.Model):
    __tablename__ = "requests"
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("rents.id"))
    user = db.relationship("Rents", back_populates="request")
    move_in = db.Column(db.String(100),nullable=False)
    move_out = db.Column(db.String(100),nullable=False)
    phnumber = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text,nullable=False)
    post_id = db.Column(db.Integer,nullable=False)
    owner =  db.Column(db.String(100),nullable=False)



db.create_all()
db.session.commit()

class Profile(db.Model):
    __tablename__ = "profile"
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("rents.id"))
    user = db.relationship("Rents", back_populates="profile")
    birth = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(100), nullable=False)
    about = db.Column(db.Text, nullable=False)
    social = db.Column(db.String(100), nullable=False)
    employment = db.Column(db.String(100), nullable=False)

db.create_all()
db.session.commit()





class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    description = db.Column(db.String(200),nullable=False)
    about = db.Column(db.Text,nullable=False)
    rule = db.Column(db.Text,nullable=False)
    map = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Integer,nullable=False)
    exterior = db.Column(db.String(200),nullable=False)
    living_room = db.Column(db.String(200),nullable=False)
    bedroom = db.Column(db.String(200),nullable=False)
    bathroom = db.Column(db.String(200),nullable=False)
    kitchen = db.Column(db.String(200),nullable=False)
    backyard = db.Column(db.String(200),nullable=False)
    owner = db.Column(db.String(200),nullable=False)
    category_id = db.Column(db.Integer,db.ForeignKey('category.id'),nullable=False)
    category = db.relationship('Category',backref = db.backref('post', lazy=True))



db.create_all()
db.session.commit()

@app.route('/')
def home():
    categories = Category.query.all()
    post = Post.query.all()
    return render_template('index.html',posts=post,categories=categories)


@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        e = Rents.query.filter_by(email=email).first()
        if e:
            if check_password_hash(e.password,password):
                login_user(e)
                flash("you are successfully login")
                p = False
                if not Profile.query.filter_by(user=current_user).first():
                    p = True
                if p:
                    return redirect(url_for('createpp'))
                return redirect(url_for('home'))
            else:
                flash("password is incorrect")
                return redirect(url_for('login'))
        else:
            flash("email doesn't exists")
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/register',methods=["GET","POST"])
def register():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        e = Rents.query.filter_by(email=email).first()
        n = Rents.query.filter_by(name=name).first()
        if e:
            flash("email is already exists")
            return redirect(url_for('register'))
        elif n:
            flash("username is already exists")
            return redirect(url_for('register'))
        else:
            hash_password = generate_password_hash(password,salt_length=8)
            new = Rents(
                name= name.upper(),
                email= email,
                password= hash_password,
            )
            db.session.add(new)
            db.session.commit()
            login_user(new)
            flash("you are successfully sign up")
            p = False
            if not Profile.query.filter_by(user=current_user).first():
                p = True
            if p:
                return redirect(url_for('createpp'))
            return redirect(url_for('home'))
    return render_template('register.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/rentals')
def rentals():
    posts = Post.query.all()
    return render_template('blog.html',posts=posts)


@app.route('/cat/<int:id>')
def cat(id):
    category = Category.query.get(id)
    posts = Post.query.filter_by(category_id=id).all()
    return render_template('cat.html',posts=posts,category=category)


@app.route("/search",methods=["GET","POST"])
def search():
    if request.method == "GET":
        q = request.args.get('q')
        if q:
            posts = Post.query.filter(Post.title.contains(q)|Post.price.contains(q)|Post.description.contains(q)|Post.about.contains(q))

        return render_template('search.html',
                               posts=posts)




@app.route('/createcity',methods=["GET","POST"])
@admin_required
def createcity():
    if request.method == "POST":
        name = request.form.get('name')
        image = request.files['image']
        image_filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
        new = Category(
            name=name,
            image=image_filename
        )
        db.session.add(new)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('cc.html')



@app.route('/create', methods=['GET', 'POST'])
@admin_required
def create():
    form = CreateForm()
    choice_list = [(i.id, i.name) for i in Category.query.all()]
    form.category.choices = choice_list
    if form.validate_on_submit():
        exterior_filename = secure_filename(form.exterior.data.filename)
        form.exterior.data.save(os.path.join(app.config['UPLOAD_FOLDER'], exterior_filename))

        living_room_filename = secure_filename(form.living_room.data.filename)
        form.living_room.data.save(os.path.join(app.config['UPLOAD_FOLDER'], living_room_filename))

        bedroom_filename = secure_filename(form.bedroom.data.filename)
        form.bedroom.data.save(os.path.join(app.config['UPLOAD_FOLDER'], bedroom_filename))

        bathroom_filename = secure_filename( form.bathroom.data.filename)
        form.bathroom.data.save(os.path.join(app.config['UPLOAD_FOLDER'], bathroom_filename))

        kitchen_filename = secure_filename(form.kitchen.data.filename)
        form.kitchen.data.save(os.path.join(app.config['UPLOAD_FOLDER'], kitchen_filename))

        backyard_filename = secure_filename(form.backyard.data.filename)
        form.backyard.data.save(os.path.join(app.config['UPLOAD_FOLDER'], backyard_filename))

        new = Post(
            title=form.title.data,
            description=form.description.data,
            about=form.about.data,
            rule=form.rule.data,
            map=form.map.data,
            price=int(form.price.data),
            exterior = exterior_filename,
            living_room=living_room_filename,
            bathroom=bathroom_filename,
            bedroom=bedroom_filename,
            kitchen=kitchen_filename,
            owner=form.owner.data,
            category = Category.query.get(form.category.data),
            backyard=backyard_filename,

        )
        db.session.add(new)
        db.session.commit()
        flash("you are successfully created")
        return redirect(url_for('create'))
    return render_template('create.html',form=form)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit(id):
    post = Post.query.get(id)
    form = CreateForm(
        title = post.title,
        description=post.description,
        map = post.map,
        price= post.price,
        exterior = post.exterior,
        bedroom=post.bedroom,
        bathroom = post.bathroom,
        living_room = post.living_room,
        kitchen= post.kitchen,
        backyard=post.backyard,
        about=post.about,
        rule=post.rule,
        owner=post.owner,
        category=post.category,

    )
    choice_list = [(i.id, i.name) for i in Category.query.all()]
    form.category.choices = choice_list
    if form.validate_on_submit():
        exterior_filename = secure_filename(form.exterior.data.filename)
        form.exterior.data.save(os.path.join(app.config['UPLOAD_FOLDER'], exterior_filename))

        living_room_filename = secure_filename(form.living_room.data.filename)
        form.living_room.data.save(os.path.join(app.config['UPLOAD_FOLDER'], living_room_filename))

        bedroom_filename = secure_filename(form.bedroom.data.filename)
        form.bedroom.data.save(os.path.join(app.config['UPLOAD_FOLDER'], bedroom_filename))

        bathroom_filename = secure_filename(form.bathroom.data.filename)
        form.bathroom.data.save(os.path.join(app.config['UPLOAD_FOLDER'], bathroom_filename))

        kitchen_filename = secure_filename(form.kitchen.data.filename)
        form.kitchen.data.save(os.path.join(app.config['UPLOAD_FOLDER'], kitchen_filename))

        backyard_filename = secure_filename(form.backyard.data.filename)
        form.backyard.data.save(os.path.join(app.config['UPLOAD_FOLDER'], backyard_filename))

        post.title = form.title.data
        post.description = form.description.data
        post.about = form.about.data
        post.rule = form.rule.data
        post.owner = form.owner.data
        post.map = form.map.data
        post.price = int(form.price.data)
        post.exterior = exterior_filename
        post.living_room = living_room_filename
        post.bedroom = bedroom_filename
        post.bathroom = bathroom_filename
        post.kitchen = kitchen_filename
        post.backyard = backyard_filename
        post.category = Category.query.get(form.category.data)

        db.session.commit()


        flash("you are successfully edited")
        return redirect(url_for('home'))
    return render_template('create.html',form=form,edit = True)


@app.route('/delete/<int:id>')
def delete(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/detail/<int:id>')
def detail(id):
    post = Post.query.get(id)
    return render_template('post-details.html',post=post)


@app.route('/about')
def about():
    return render_template('about.html')



@app.route('/contact')
def contact():
    return render_template('contact.html')



@app.route('/error')
def error():
    return render_template("error.html")

@app.route("/profile/")
def profile():
    pp = Profile.query.filter_by(user=current_user).first()
    p = False
    if not Profile.query.filter_by(user=current_user).first():
        p = True
    return render_template("profile.html",p=p,pp=pp)

@app.route("/createpp",methods=["GET","POST"])
def createpp():
    pp = Profile.query.filter_by(user=current_user).first()
    form = Createprofile()
    if form.validate_on_submit():
        birth = form.birth.data
        gender = form.gender.data
        about = form.about.data
        social = form.social.data
        employment = form.employment.data
        new = Profile(
            user=current_user,
            birth=birth,
            gender = gender,
            about=about,
            social = social,
            employment = employment
        )
        db.session.add(new)
        db.session.commit()
        return redirect(url_for('profile'))
    return render_template('createpp.html',form=form,pp=pp)


@app.route("/editpp",methods=["GET","POST"])
def editpp():
    pp = Profile.query.filter_by(user=current_user).first()
    pb = datetime.datetime.strptime(pp.birth, "%Y-%m-%d")
    form = Createprofile(
        birth=pb,
        gender = pp.gender,
        about = pp.about,
        social = pp.social,
        employment = pp.employment,
    )
    if form.validate_on_submit():
        pp.birth = form.birth.data
        pp.gender = form.gender.data
        pp.about = form.about.data
        pp.social = form.social.data
        pp.employment = form.employment.data
        db.session.commit()
        return redirect(url_for('profile'))
    return render_template('createpp.html',form=form,pp=pp)


@app.route('/request/<int:id>',methods=["GET","POST"])
def book(id):
    if not current_user.is_authenticated:
        flash("you need to first login")
        return redirect(url_for('login'))
    post = Post.query.get(id)
    form = Createrequest()
    if form.validate_on_submit():
        new = Request(
            user = current_user,
            move_in = form.move_in.data,
            move_out = form.move_out.data,
            message = form.about.data,
            phnumber=form.phnumber.data,
            post_id = post.id,
            owner = post.owner.upper(),
        )
        db.session.add(new)
        db.session.commit()
        flash("your request has been sent.we will contact you as soon as possible")
        return redirect(url_for('requests'))
    return render_template('request.html',form=form,post=post)


@app.route('/host')
def host():
    return render_template('host.html')

@app.route('/rentalrequest')
def rental_request():
    r = Request.query.all()
    return render_template('rental_request.html',r=r)

@app.route('/requests')
def requests():
    r = Request.query.filter_by(user=current_user)
    return render_template('requests.html',r=r)



@app.route('/hostrequest')
def hostrequest():
    r = Request.query.filter_by(owner=current_user.name)
    return render_template('host_request.html',r=r)




if __name__ == "__main__":
    app.run(debug=True)