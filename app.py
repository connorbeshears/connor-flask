from flask import Flask, request, jsonify, render_template,redirect, url_for, session, g, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug import check_password_hash, generate_password_hash
import os, datetime, functools

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Book, Comment, User

# @app.route('/')
# def hello():
#     return("Hello World")

@app.route("/name/<name>")
def get_book_name(name):
    return("name : {}".format(name))

# @app.route("/details")
# def get_book_details():
#     author = request.args.get('author')
#     published = request.args.get('published')
#     return("Author : {}, Published: {}".format(author, published))

# @app.route("/add")
# def add_book():
#     name = request.args.get('name')
#     author = request.args.get('author')
#     published = request.args.get('published')

#     try:
#         book = Book(
#             name=name,
#             author=author,
#             published=published
#         )
#         db.session.add(book)
#         db.session.commit()
#         return("Book added. book id = {}".format(book.id))
#     except Exception as e:
#         return(str(e))

def login_req(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return(redirect(url_for('login')))
        return(view(**kwargs))
    return(wrapped_view)

@app.before_request
def check_logged():
    userId = session.get('user_id')

    if userId is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id = userId).first()

@app.route("/")
def get_all():
    session['logError'] = None
    try:
        if(session.get('username') == None):
            tmp = ''
        else:
            tmp = session.get('username')
        books = Book.query.all()
        comments = Comment.query.all()
        return render_template("getall.html", books=books, comments=comments, username=tmp)
    except Exception as e:
        return(str(e))

@app.route("/get/<id_>")
def get_by_id(id_):
    try:
        book = Book.query.filter_by(id=id_).first()
        return jsonify(book.serialize())
    except Exception as e:
        return(str(e))

@app.route("/add/form", methods=['GET', 'POST'])
@login_req
def add_book_form():
    if request.method == 'POST':
        name = request.form.get('name')
        author = session.get('username')
        published = request.form.get('published')
        now = datetime.datetime.now()
        createdOn = now.strftime("%b. %d, %Y at %I:%M %p")

        try:
            book = Book(
                name=name,
                author=author,
                published=published,
                createdOn = createdOn
            )
            db.session.add(book)
            db.session.commit()
            return(redirect(url_for('get_all')))
        except Exception as e:
            return(str(e))
    return render_template("addbook.html")

@app.route('/add/comment/<id_>', methods=['GET', 'POST'])
@login_req
def addComment(id_):
    if request.method == 'POST':
        content = request.form.get('content')
        createdBy = session.get('username')
        now = datetime.datetime.now()
        createdOn = now.strftime("%b. %d, %Y at %I:%M %p")
        bookId = id_
    
        try:
            comment = Comment(
                bookId = bookId,
                content = content,
                createdBy = createdBy,
                createdOn = createdOn
            )
            db.session.add(comment)
            db.session.commit()
            return(redirect(url_for('get_all')))
        except Exception as e:
            return(str(e))
    return(render_template('addcomment.html'))

@app.route('/register', methods=('GET', 'POST'))
def register():
    if(session.get('logError') == "Incorrect Username or Password"):
        session['logError'] = None
    if(request.method == 'POST'):
        username = request.form.get('username')
        password = generate_password_hash(request.form.get('password'))

        try:
            tmp = User.query.filter_by(username=username).first()
            if(tmp == None):
                user = User(
                    username = username,
                    passw = password
                )
                db.session.add(user)
                db.session.commit()
                return(redirect(url_for('login')))
            else:
                session['logError'] = "Username already taken"
                return(redirect(url_for('register')))
        except Exception as e:
            return(str(e))
    if(session.get('logError') == None):
        tmp = ''
    else:
        tmp = session.get('logError')
    return(render_template('register.html', error=tmp))

@app.route('/login', methods=('GET', 'POST'))
def login():
    if(session.get('logError') == "Username already taken"):
        session['logError'] = None
    if(request.method == 'POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            user = User.query.filter_by(username=username).first()
            if(user == None or not check_password_hash(user.passw, password)):
                session['logError'] = "Incorrect Username or Password"
                return(redirect(url_for('login')))
            elif(check_password_hash(user.passw, password)):
                session.clear()
                session['user_id'] = user.id
                session['username'] = user.username
                return(redirect(url_for('get_all')))
        except Exception as e:
            return(str(e))
    if(session.get('logError') == None):
        tmp = ''
    else:
        tmp = session.get('logError')
    return(render_template('login.html', error=tmp))

@app.route("/logout", methods=('GET', 'POST'))
@login_req
def logout():
    session['user_id'] = None
    session['username'] = None
    g.user = None
    return(redirect(url_for('get_all')))



if (__name__ == '__main__'):
    app.run()