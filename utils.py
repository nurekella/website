import os
import hashlib

import psycopg2



# 
def connect():
	connection = psycopg2.connect(user='postgres', password='1111', host='127.0.0.1', port='3306', database='postgres')
	cursor = connection.cursor()
	return connection, cursor

# 
def is_table_exists(name):
	connection, cursor = connect()

	query = '''SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_catalog='postgres' AND table_schema='public' AND table_name='%s');''' % name
	cursor.execute(query)
	record = cursor.fetchone()
	# Закрытие курсора и соеденения 
	cursor.close()
	connection.close()
	return record[0]

# 
def create_post_table():
	connection, cursor = connect()

	query = '''CREATE TABLE posts (id BIGSERIAL, post_title TEXT, post_preview TEXT, post_text TEXT, date VARCHAR(50));'''

	cursor.execute(query)
	connection.commit()
	# Закрытие курсора и соеденения 
	cursor.close()
	connection.close()

# 
def create_safety_table():
	connection, cursor = connect()

	query = '''CREATE TABLE safety (login VARCHAR(255), password VARCHAR(255));'''

	cursor.execute(query)
	connection.commit()
	# Закрытие курсора и соеденения 
	cursor.close()
	connection.close()


# 
def insert_data_form_safety_table():
	sha256_login_hash = '0FFE1ABD1A08215353C233D6E009613E95EEC4253832A761AF28FF37AC5A150C' # 1111
	sha256_password_hash = '03AC674216F3E15C761EE1A5E255F067953623C8B388B4459E13F978D7C846F4' # 1234

	connection, cursor = connect()

	query = """INSERT INTO safety (login, password) VALUES ('%s', '%s') """ % (sha256_login_hash, sha256_password_hash)

	cursor.execute(query)
	connection.commit()
	# Закрытие курсора и соеденения 
	cursor.close()
	connection.close()

# 
def append_post(post_title, post_preview, post_text, date):
	connection, cursor = connect()

	query = """INSERT INTO posts (post_title, post_preview, post_text, date) VALUES ('%s', '%s', '%s', '%s') """ % (post_title, post_preview, post_text, date)

	cursor.execute(query)
	connection.commit()
	# Закрытие курсора и соеденения 
	cursor.close()
	connection.close()

# 
def update_post(post_id, post_title, post_preview, post_text):
	connection, cursor = connect()

	query = """UPDATE posts SET post_title = '%s', post_preview = '%s', post_text = '%s' WHERE id = '%s'""" % (post_title, post_preview, post_text, post_id)
	cursor.execute(query)
	connection.commit()
	# Закрытие курсора и соеденения 
	cursor.close()
	connection.close()

# 
def select_posts(offset, sample):
	connection, cursor = connect()
	cursor.execute("""SELECT * FROM posts ORDER BY id DESC OFFSET %s FETCH NEXT %s ROWS ONLY """ % (offset, sample))
	result = cursor.fetchall()
	# Закрытие курсора и соеденения 
	cursor.close()
	connection.close()

	return result


# 
def select_post(post_id):
	connection, cursor = connect()
	cursor.execute("""SELECT * FROM posts WHERE id = '%s'""" % post_id)
	result = cursor.fetchone()
	# Закрытие курсора и соеденения 
	cursor.close()
	connection.close()

	return result

# 
def select_login_and_password():
	connection, cursor = connect()
	cursor.execute("""SELECT (login, password) FROM safety""")
	result = cursor.fetchone()
	# Закрытие курсора и соеденения 
	cursor.close()
	connection.close()

	return result

# 
def delete_post(post_id):
	connection, cursor = connect()

	query = """DELETE FROM posts WHERE id = '%s'""" % post_id
	cursor.execute(query)
	connection.commit()
	# Закрытие курсора и соеденения 
	cursor.close()
	connection.close()

# 
def get_amount_posts():
	connection, cursor = connect()
	cursor.execute("""SELECT * FROM posts""")
	result = cursor.fetchall()
	# Закрытие курсора и соеденения 
	cursor.close()
	connection.close()

	return len(result)

# 
def valid_data(login, password):
	sha256_login_hash = hashlib.sha256(login.encode()).hexdigest().upper()
	sha256_password_hash = hashlib.sha256(password.encode()).hexdigest().upper()

	data = select_login_and_password()
	if(data):
		data = data[0][1:-1].split(',')
		secret_login, secret_password = data

	if(sha256_login_hash == secret_login and sha256_password_hash == secret_password):
		return True

	return False

# 
def create_random_token(length=128):
	random_bytes = os.urandom(length)
	return hashlib.sha256(random_bytes).hexdigest()

# 
def firs_start():
	if(not is_table_exists('posts')):
		create_posts_table()

		append_post('Статья № 1', 'Анонс статьи 1', 'Текст статьи 1', time.ctime(time.time()))
		append_post('Статья № 2', 'Анонс статьи 2', 'Текст статьи 2', time.ctime(time.time()))
		append_post('Статья № 3', 'Анонс статьи 3', 'Текст статьи 3', time.ctime(time.time()))
		append_post('Статья № 4', 'Анонс статьи 4', 'Текст статьи 4', time.ctime(time.time()))

		print('[i] Успешно записано 4 статьи')	

	# Создание таблицы с логином и паролем от админки 
	if(not is_table_exists('safety')):
		create_safety_table()
		
		insert_data_form_safety_table()
		print('[i] Логин и пароль администратора. Логин: 1111, пароль: 1234')

