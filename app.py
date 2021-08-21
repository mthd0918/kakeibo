# splite3をimportする
import sqlite3
# flaskをimportしてflaskを使えるようにする
from flask import Flask , render_template , request, redirect, session
from flask.templating import render_template_string
# appにFlaskを定義して使えるようにしています。Flask クラスのインスタンスを作って、 app という変数に代入しています。
app = Flask(__name__)

app.secret_key = "kakeibo"

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=["GET","POST"])
def register():
    if request.method == "GET":
        if 'id' in session :
            return redirect ('/zandaka')
        else:
            return render_template("register.html")

    else:
        name = request.form.get("name")
        password = request.form.get("password")
        conn = sqlite3.connect('kakeibo.db')
        c = conn.cursor()
        c.execute("insert into user_info values(null,?,?)", (name,password))
        conn.commit()
        conn.close()
        return redirect('/login')


@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == "GET":
        if "id" in session:
            return redirect("/zandaka")
        else:
            return render_template('login.html')
    else:
        name = request.form.get('name')
        password = request.form.get('password')
        conn = sqlite3.connect("kakeibo.db")
        c = conn.cursor()
        c.execute('select id from user_info where name = ? and password = ?',(name,password))
        user_id = c.fetchone()
        conn.close()
        print(user_id)

        if user_id is None:
            return render_template('login.html')
        else:
            session['user_id'] = user_id[0]
            return redirect('/zandaka')


@app.route('/logout')
def logout():
    session.pop('id',None)
    return redirect('/login')
        

@app.route("/zandaka")
def zandaka():
    if "user_id" in session:
        user_id = session["user_id"]
        conn = sqlite3.connect('kakeibo.db')
        c = conn.cursor()
        c.execute('select name from user_info where id = ?', (user_id,))
        user_info = c.fetchone()        
        
        c.execute('select * from zandaka')
        zandaka_list = []
        for row in c.fetchall():
            zandaka_list.append({"id": row[0], "date" : row[1], "ac" : row[2], "kingaku" : row[3]})
        print(zandaka_list)
        c.close()
        return render_template('zandaka.html', user_info = user_info, zandaka_list = zandaka_list)
    else:
        return redirect('/login')


@app.route('/update', methods=["GET","POST"])
def update():
    date = request.form.get("date")
    ac = request.form.get("ac")
    kingaku = request.form.get("kingaku")
    conn = sqlite3.connect('kakeibo.db')
    c = conn.cursor()
    c.execute("insert into zandaka values(null,?,?,?)", (date,ac,kingaku))
    conn.commit()
    conn.close()
    return render_template('update.html')


@app.route('/del', methods=["GET", "POST"])
def del_task():
    id = request.form.get("id")
    conn = sqlite3.connect('kakeibo.db')
    c = conn.cursor()
    c.execute("update zandaka set del_flag = 1 where id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/zandaka")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)