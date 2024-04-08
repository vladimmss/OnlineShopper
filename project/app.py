from flask import Flask, render_template


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/catalog')
def catalog():
    return render_template('catalog.html')


@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


@app.route('/feedback')
def feedback():
    return render_template('feedback.html')


@app.route('/support')
def support():
    return render_template('support.html')


if __name__ == '__main__':
    app.run(debug=True)
