from flask import Flask, redirect, render_template, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__)
app.secret_key = "djfljdfljfnkjdfhjfshjkfjfjfhhjdhdjhdfu"

userpass = "mysql+pymysql://root:@"
basedir = "127.0.0.1"
dbname = "/company"

app.config["SQLALCHEMY_DATABASE_URI"] = userpass + basedir + dbname
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Employes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telp = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255), nullable=False)

    def __init__(self, name, email, telp, address):
        self.name = name
        self.email = email
        self.telp = telp
        self.address = address

@app.route('/')
def index():
    data_employe = db.session.query(Employes)
    return render_template("index.html", data=data_employe)

@app.route('/input', methods=['GET', 'POST'])
def input_data():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        telp = request.form['telp']
        address = request.form['address']

        add_data = Employes(name, email, telp, address)

        db.session.add(add_data)
        db.session.commit()

        flash('input Data Bien Enregistre')

        return redirect(url_for('index'))
        
    return render_template('input.html')

@app.route('/edit/<int:id>')
def edit_data(id):
    data_employes = Employes.query.get(id)
    return render_template('edit.html', data=data_employes)

@app.route('/proses_edit', methods=['POST'])
def proses_edit():
    id = request.form.get('id')
    data_employe = Employes.query.get(id)

    data_employe.name = request.form['name']
    data_employe.email = request.form['email']
    data_employe.telp = request.form['telp']
    data_employe.address = request.form['address']

    db.session.commit()

    flash('Edit Data Bien Modifier')

    return redirect(url_for('index'))


from flask import redirect, url_for

from flask import redirect, url_for, abort

@app.route('/delete/<int:id>')
def delete(id):
    data_employe = Employes.query.get(id)
    
    if data_employe is None:
        flash("Employee data with ID {} not found.".format(id))
        return redirect(url_for('index'))
    
    db.session.delete(data_employe)
    db.session.commit()

    flash("Delete Data Bien Supprimer")
    return redirect(url_for('index'))



if __name__ == "__main__":
    app.run(debug=True)
