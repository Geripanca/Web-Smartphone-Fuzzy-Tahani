import datetime
from flask import Flask, render_template

app = Flask(__name__)

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
    return render_template('proyek.html')

if __name__ == '__main__':
    app.run(debug=True)		