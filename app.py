from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
db = SQLAlchemy(app)

class Todo(db.Model):  
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    desc = db.Column(db.String(900), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"{self.sno}-{self.title}"

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
 
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()

        return redirect(url_for('hello_world'))

    alltodo = Todo.query.all()
    return render_template("index.html", alltodo=alltodo)

@app.route('/show')
def products():
    alltodo = Todo.query.all()
    print(alltodo)
    return 'Hello, product!'

@app.route('/delete/<int:sno>', methods=['GET', 'POST'])
def delete(sno):
    todo = Todo.query.get_or_404(sno)
    if request.method == 'POST':
        db.session.delete(todo)
        db.session.commit()
        return redirect(url_for('hello_world'))
    return render_template('delete.html', todo=todo)

@app.route('/edit/<int:sno>', methods=['GET', 'POST'])
def edit(sno):
    todo = Todo.query.get_or_404(sno)
    if request.method == 'POST':
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        db.session.commit()
        return redirect(url_for('hello_world'))
    return render_template('edit.html', todo=todo)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
