from flask import Flask, request, jsonify
from flask_cors import CORS
from database import engine, SessionLocal
from models import Base, Task

app = Flask(__name__)
CORS(app)

Base.metadata.create_all(bind=engine)


@app.route("/tasks", methods=["GET"])
def get_tasks():

    db = SessionLocal()
    tasks = db.query(Task).all()

    return jsonify([
        {"id":t.id,"title":t.title} for t in tasks
    ])


@app.route("/tasks", methods=["POST"])
def create_task():

    data = request.json
    db = SessionLocal()

    task = Task(title=data["title"])

    db.add(task)
    db.commit()
    db.refresh(task)

    return jsonify({"id":task.id,"title":task.title})


@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):

    db = SessionLocal()

    task = db.query(Task).filter(Task.id==id).first()

    db.delete(task)
    db.commit()

    return {"message":"deleted"}


if __name__ == "__main__":
    app.run(debug=True)
