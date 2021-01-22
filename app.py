import os
import sys
import time

from flask import (Flask, request, session, redirect, abort,
						render_template, url_for, send_from_directory)

import utils



# Количество постов отображаемых на одной новостной странице
AMOUNT_POSTS_IN_NEWS_PAGE = 4


app = Flask(__name__)

# 
app.secret_key = b'\xc4\x88]\xe6\x97\xb3\x8bb:R\x0b\n\xce}a\xd6'


@app.route('/')
def redirect_to_index():
	return redirect(url_for('index'))


@app.route('/index')
def index():
	return render_template('index.html', session=session)


@app.route('/news', methods=['GET'])
def news():
	page = request.args.get('page', 0)

	amount_posts = utils.get_amount_posts()

	pages = list(range(0, amount_posts+1, AMOUNT_POSTS_IN_NEWS_PAGE))

	items = []
	for n, i in enumerate(pages, 1):
		items.append((n, i))

	posts = utils.select_posts(offset=page, sample=AMOUNT_POSTS_IN_NEWS_PAGE)

	return render_template('news.html', session=session, posts=posts, pages=items)


@app.route('/add_post')
def add_post():
	# Проверка подлинности присланого токена
	if(request.args.get('token') != session.get('token')):
		return abort(403)

	return render_template('add_post.html', session=session)


@app.route('/add_post_api', methods=['POST'])
def add_post_api():
	# Проверка подлинности присланого токена
	if(request.form.get('token') != session.get('token')):
		return abort(403)

	title = request.form.get('post_title')
	preview = request.form.get('post_preview')
	text = request.form.get('post_text')
	# Проверка даных 
	if(all([title, preview, text])):
		utils.append_post(title, preview, text, time.ctime(time.time()))

	return redirect(url_for('news'))


@app.route('/view_post', methods=['GET'])
def view_post():
	post_id = request.args.get('id')
	if(post_id):
		post = utils.select_post(post_id)
		if(post):
			return render_template('view_post.html', session=session, post=post)
	# В случае ошибки делает редирект на новостную страницу 
	return redirect(url_for('news'))


@app.route('/update_post', methods=['GET'])
def update_post():
	# Проверка подлинности присланого токена
	if(request.args.get('token') != session.get('token')):
		return abort(403)

	post_id = request.args.get('id')
	if(post_id):
		post = utils.select_post(post_id)
		if(post):
			return render_template('add_post.html', session=session, post=post)
	# В случае ошибки делает редирект на новостную страницу 
	return redirect(url_for('news'))


@app.route('/update_post_api', methods=['POST'])
def update_post_api():
	# Проверка подлинности присланого токена
	if(request.form.get('token') != session.get('token')):
		return abort(403)

	post_id = request.form.get('post_id')
	title = request.form.get('post_title')
	preview = request.form.get('post_preview')
	text = request.form.get('post_text')
	# Проверка даных 
	if(all([post_id, title, preview, text])):
		utils.update_post(post_id, title, preview, text)

	return redirect(url_for('news'))


@app.route('/delete_post', methods=['GET'])
def delete_post():
	# Проверка подлинности присланого токена
	if(request.args.get('token') != session.get('token')):
		return abort(403)

	post_id = request.args.get('id')
	if(post_id):
		utils.delete_post(post_id)
	# Возвращение на страницу
	return redirect(url_for('news'))


@app.route('/gallery')
def gallery():
	return render_template('gallery.html', session=session)


@app.route('/about')
def about():
	return render_template('about.html', session=session)


@app.route('/login')
def login():
	# Выдача одноразового токена для каждой формы при авторизации нужна лишь для усложнения подбора логина и пароля от админ. панели.
	# Без одноразового токена можно осуществить отправку множества АСИНХРОННЫХ post запросов с рандомными логином и паролем.
	# Но с использованием одноразового токена, придется каждый раз отправлять get запрос на поддомен /login,
	# парсить одноразовый токен со страницы, добавлять его в пост запрос и лишь тогда отправлять. 

	# Создание одноразового токена
	temp_token = utils.create_random_token(64)
	# Запись одноразового токена в сессию
	session['temp_token'] = temp_token
	# Отправка шаблона
	return render_template('login.html', token=temp_token)


@app.route('/login', methods=['POST'])
def login_api():
	if(request.form.get('temp_token') != session.get('temp_token')):
		return abort(403)

	if(utils.valid_data(request.form.get('login', ''), request.form.get('password', ''))):
		# Удаления одноразового токена
		session.pop('temp_token')
		# Назначение рандомного секретного токена для подписи форм или для передачи параметром в get запросах, 
		# для подтверждения что их отправил именно администратор.
		session['token'] = utils.create_random_token(128)
		# 
		return redirect(url_for('index'))

	return render_template('login.html', error='Неверно указан логин или проль')


@app.route('/logout')
def logout():
	# Проверка подлинности присланого токена
	if(request.args.get('token') != session.get('token')):
		return abort(403)

	session.pop('token')

	return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# 
if(__name__=='__main__'):
	# 
	os.chdir(os.path.dirname(sys.argv[0]))
	# Для первого запуска выпонить функцыю указаную ниже. 
	# Она создаст нужные таблицы в базе данных и заполнит их базовыми значениями
	# Для входа в админ панель перейдите по адресу http://127.0.0.1:5000/login
	# Логин 1111, пароль 1234
	# utils.firs_start()
	
	# Запуск сервера
	app.run()