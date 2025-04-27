#---ОРИГИНАЛЬНЫЙ САЙТ, СДЕЛАННЫЙ PATARR19 (PATARRNINETEEN/ПАТАРРДЕВЯТНАДЦАТЬ/ПАТАРРНАЙНТИН)---#

from flask import Flask, render_template, request, redirect, url_for
import sqlite3, os

app = Flask(__name__)

db_path = "users.db"

def init_db():
    db_exists = os.path.exists(db_path)
    database = sqlite3.connect(db_path)
    cursor = database.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users' ")
    table_exists = cursor.fetchone()

    if not table_exists:
        cursor.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                login TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        database.commit()
        print("Таблица 'users' создана")
    
    database.close()

init_db()

@app.route("/", methods = ["POST","GET"])
def loginPage():
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")

        if not login or not password:
            return render_template("login.html", error="Поля не заполнены"), 400
        
        database = sqlite3.connect("users.db")
        cursor = database.cursor()
        cursor.execute('SELECT password FROM users WHERE login = ?', (login,))
        user = cursor.fetchone()
        database.close()

        if user and user[0] == password:
            return redirect(url_for("userPage", username=login))
        else:
            return render_template("login.html", error="Пользователь не найден")

    return render_template("login.html")

@app.route("/regist", methods = ["POST", "GET"])
def registPage():
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")
        repeat_password = request.form.get("repeat_password")

        if not login or not password or not repeat_password:
            return render_template("regist.html", error="Поля не заполнены"), 400
        
        if repeat_password != password:
            return render_template("regist.html", error="Пароли не совпадают"), 400
        
        database = sqlite3.connect("users.db")
        cursor = database.cursor()

        cursor.execute("SELECT login FROM users WHERE login = ?", (login,))

        if cursor.fetchone():
            database.close()
            return render_template("regist.html", error="Пользователь уже существует"), 400
        
        try:
            cursor.execute("INSERT INTO users (login, password) VALUES (?, ?)", (login,password))
            database.commit()
            database.close()
            return redirect(url_for("userPage", username=login))
        except Exception as e:
            database.close()
            return render_template("regist.html", error="Ошибка при регистрации"), 400

    return render_template("regist.html")

@app.route("/user/<username>")
def userPage(username):
    database = sqlite3.connect("users.db")
    cursor = database.cursor()
    cursor.execute("SELECT login, password FROM users WHERE login = ?", (username,))
    user = cursor.fetchone()

    if not user:
        return redirect(url_for("loginPage"))
    
    login, password = user
    
    database.close()
    
    return render_template("user.html", login=username, password=password)

if __name__ == '__main__':
    app.run(debug=True)


#---В БУДУЩИХ ОБНОВЛЕНИЯХ СДЕЛАТЬ ПРОВЕРКУ ПО ДЛИНЕ ПАРОЛЯ/ЛОГИНА И ПРОВЕРКУ НА ЗАПРЕЩЕННЫЕ СИМВОЛЫ---#
#---ПОДКЛЮЧИТЬ БД ДЛЯ НОРМАЛЬНОЙ ГЕНЕРАЦИИ АККАУНТОВ---#