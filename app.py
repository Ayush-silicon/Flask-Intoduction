from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime   

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Task {self.id}"

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form.get('content')
        if task_content:
            new_task = MyTask(content=task_content)
            try:
                db.session.add(new_task)
                db.session.commit()
                return redirect("/")
            except Exception as e:
                print(f"Error adding task: {e}")
                return f"An error occurred while adding the task: {e}"

    tasks = MyTask.query.order_by(MyTask.created).all()
    return render_template('index.html', tasks=tasks)

@app.route("/delete/<int:id>", methods=['GET', 'POST'])
def delete(id: int):
    task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"ERROR: {e}"

@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id: int):
    task = MyTask.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"Error: {e}"
    else:
        return render_template("edit.html", task=task)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
