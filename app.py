import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, g
import pymysql

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'lasmilibolibosibosibosibosilibo'

#koneksi database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  
app.config['MYSQL_DB'] = 'db_resphone'

#menyambungkan
def get_db():
    """Menyambungkan ke database."""
    if 'db' not in g:
        g.db = pymysql.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB']
        )
    return g.db

# Fungsi untuk menutup koneksi database
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.errorhandler(404)  # Tambahkan error handler untuk 404
def page_not_found(error):
    return render_template("404.html"), 404

@app.route("/")
@app.route("/index")
def index():
    year = datetime.datetime.now().year
    return render_template("index.html", year=year)

@app.route("/tentang")
def tentang():
    return render_template('tentang.html')

@app.route("/proyek")
def proyek():
    year = datetime.datetime.now().year
    return render_template('proyek.html', year=year)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validasi bahwa kedua kolom username dan password diisi
        if not username or not password:
            flash('Username dan password harus diisi', 'danger')
            return render_template('login.html')
        
        # Cek kredensial di database
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM tb_akun WHERE username=%s AND password=%s", (username, password))
        akun = cursor.fetchone()
    
        if akun:
            session['logged_in'] = True
            # session['username'] = akun['username']
            return redirect(url_for('index'))
        else:
            flash('Username atau password salah', 'danger')

    return render_template('login.html')

# Route untuk logout
@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route("/<path:path>")  # Tangkap semua request path yang tidak valid
def catch_all(path):
    return page_not_found(404)  # Lanjut halaman 404

if __name__ == '__main__':
    app.run(debug=True)
