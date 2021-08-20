# splite3をimportする
import sqlite3
# flaskをimportしてflaskを使えるようにする
from flask import Flask , render_template , request, redirect, session
# appにFlaskを定義して使えるようにしています。Flask クラスのインスタンスを作って、 app という変数に代入しています。
app = Flask(__name__)

app.secret_key = "kakeibo"

print('Hello, World')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=["GET","POST"])
def register():
    #  登録ページを表示させる
    if request.method == "GET":
        if 'id' in session :
            return redirect ('/zandaka')
        else:
            return render_template("register.html")

    # ここからPOSTの処理
    else:
        # 登録ページで登録ボタンを押した時に走る処理
        name = request.form.get("name")
        password = request.form.get("password")

        conn = sqlite3.connect('kakeibo.db')
        c = conn.cursor()
        # 課題4の答えはここ
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

@app.route('/edit/<int:id>')
def edit(id):
    if 'user_id' in session :
        conn = sqlite3.connect('kakkeibo.db')
        c = conn.cursor()
        c.execute("select id from user_info where id = ?", (id,) )
        user_info = c.fetchone()
        conn.close()

        if user_info is not None:
            # None に対しては インデクス指定できないので None 判定した後にインデックスを指定
            user = comment[0] # "りんご" ○   ("りんご",) ☓
            # fetchone()で取り出したtupleに 0 を指定することで テキストだけをとりだす
        else:
            return "アイテムがありません" # 指定したIDの name がなければときの対処

        item = { "id":id, "comment":comment }

        return render_template("edit.html", comment=item)
    else:
        return redirect("/login")


# /add ではPOSTを使ったので /edit ではあえてGETを使う
@app.route("/edit")
def update_item():
    if 'user_id' in session :
        # ブラウザから送られてきたデータを取得
        item_id = request.args.get("item_id") # id
        print(item_id)
        item_id = int(item_id) # ブラウザから送られてきたのは文字列なので整数に変換する
        comment = request.args.get("comment") # 編集されたテキストを取得する

        # 既にあるデータベースのデータを送られてきたデータに更新
        conn = sqlite3.connect('service.db')
        c = conn.cursor()
        c.execute("update bbs set comment = ? where id = ?",(comment,item_id))
        conn.commit()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)