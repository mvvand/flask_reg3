from flask import Flask, redirect, request, render_template, url_for
from psycopg2 import connect

conn = connect(database="test_db2",
               user="postgres",
               password="123",
               host="localhost",
               port="5432")

cursor = conn.cursor()

app = Flask(__name__)


@app.route("/login", methods=["POST", "GET"])
def login_page():
    if request.method == "POST":
        print(request.form)
        if request.form.get('login'):
            login = request.form.get("username")
            password = request.form.get("password")

            error = ''
            if not (login and password):
                error = "Заполните все поля"
                return render_template("login.html", error=error)
            cursor.execute(f"SELECT * FROM public.users WHERE login='{login}'")
            records = cursor.fetchall()
            if not records:
                error = "Такого логина не существует"
                return render_template("login.html", error=error)
            elif records[0][2] != password:
                error = "Пароль неправильный"
                return render_template("login.html", error=error)
            else:
                return f"Привет, {records[0][1]}"

        else:
            return redirect(url_for('reg_page'))

    return render_template("login.html")


@app.route("/reg", methods=["POST", "GET"])
def reg_page():
    if request.method == "POST":
        name = request.form.get("name")
        login = request.form.get("login")
        password = request.form.get("password")

        error = ''
        if not (name and login and password):
            error = "Заполните все поля"
            return render_template("reg.html", error=error)

        cursor.execute(f"SELECT * FROM public.users WHERE login='{login}'")

        if cursor.fetchall():
            error = "Такой уже етсь"
            return render_template("reg.html", error=error)

        cursor.execute(f"INSERT INTO public.users (login, name, password) VALUES ('{login}', '{name}', '{password}')")
        conn.commit()
        return redirect(url_for('login_page'))

    return render_template("reg.html")
