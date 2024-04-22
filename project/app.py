from flask import Flask, render_template, request, redirect
from data import db_session
from data.users import User
from data.feedbacks import Feedbacks
from flask_login import LoginManager, login_user, logout_user, login_required


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/osh.db")

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST' and request.form['email'] and request.form['password']:
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == request.form['email']).first()
        if user and user.check_password(request.form['password']):
            if request.form.get('checkbox') == 'checked':
                login_user(user, remember=True)
            else:
                login_user(user, remember=False)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль")
    return render_template('login.html')


@app.route('/registration', methods=["GET", "POST"])
def registration():
    if request.method == 'POST' and request.form['name'] and request.form['email'] and \
            request.form['password1'] and request.form['password2']:
        if not request.form['name'] or not request.form['email'] or not \
                request.form['password1'] or not request.form['password2']:
            return render_template('registration.html', message="Заполните все поля!")
        elif request.form['password1'] != request.form['password2']:
            return render_template('registration.html', message="Пароли не совпадают!")
        elif len(request.form['password1']) < 8:
            return render_template('registration.html', message="Пароль слишком короткий!")
        elif '@' not in request.form['email']:
            return render_template('registration.html', message="Неверный адрес электронной почты!")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == request.form['email']).first():
            return render_template('registration.html', message="Такой пользователь уже существует!")
        user = User(
            name=request.form['name'],
            email=request.form['email']
        )
        user.set_password(request.form['password1'])
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('registration.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/catalog')
def catalog():
    return render_template('catalog.html')


@app.route('/basket')
def basket():
    return render_template('basket.html')


@app.route('/feedback', methods=["GET", "POST"])
def feedback():
    if request.method == 'POST' and request.method['1'] and request.method['2']:
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == request.form['1']).first():
            fb = Feedbacks(
                content=request.form['2'],
                user_email=request.form['1']
            )
            db_sess.add(fb)
            db_sess.commit()
            return redirect('/')
        return render_template('login.html', message="Неправильный email")
    return render_template('feedback.html')


@app.route('/support')
def support():
    return render_template('support.html')


if __name__ == '__main__':
    app.run(debug=True)
