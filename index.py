from flask import *
from settings import *
app = Flask(__name__)



@app.route("/", methods=('GET', 'POST'))
def index():
	messages = []
	if request.method == 'POST':
		login = request.form['login']
		password = request.form['password']
		account = IsAccountCreated(login, password)
		if account == 2:
			session['user'] = login
			return redirect(url_for('home'))
		elif account == 0:	
			messages.append('Аккаунт не найден!')
		elif account == 1:
			messages.append('Неверный пароль!')
		else:
			messages.append('Неизвестная ошибка!')

	return render_template('main.html', messages=messages)

@app.route("/home")
def home():
	return render_template('home.html')