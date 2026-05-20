    from flask import Flask, render_template, request, session, jsonify
import time

app = Flask(__name__)
app.secret_key = "replace-with-a-strong-secret-key"

# Initialize the task list in the user session
def get_tasks():
    if "tasks" not in session:
        session["tasks"] = []
    return session["tasks"]

# Home route renders the main page
@app.route("/")
def home():
    tasks = get_tasks()
    return render_template("index.html", tasks=tasks)

# Add a new task to session
@app.route("/add", methods=["POST"])
def add_task():
    tasks = get_tasks()
    data = request.get_json() or {}
    title = data.get("title", "").strip()
    if not title:
        return jsonify({"success": False, "message": "Task title cannot be empty."}), 400

    task = {
        "id": str(int(time.time() * 1000)),
        "title": title,
        "completed": False,
    }
    tasks.append(task)
    session["tasks"] = tasks
    return jsonify({"success": True, "task": task, "tasks": tasks})

# Toggle completed state for a task
@app.route("/complete/<task_id>", methods=["POST"])
def complete_task(task_id):
    tasks = get_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]
            session["tasks"] = tasks
            return jsonify({"success": True, "task": task, "tasks": tasks})
    return jsonify({"success": False, "message": "Task not found."}), 404

# Delete a task from session
@app.route("/delete/<task_id>", methods=["POST"])
def delete_task(task_id):
    tasks = get_tasks()
    tasks = [task for task in tasks if task["id"] != task_id]
    session["tasks"] = tasks
    return jsonify({"success": True, "tasks": tasks})

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
