from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


def get_db_connection():
    connection = sqlite3.connect("tasks.db")
    connection.row_factory = sqlite3.Row
    return connection


def create_table():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT,
            priority TEXT,
            completed INTEGER DEFAULT 0
        )
    """)

    connection.commit()
    connection.close()


@app.route("/")
def home():
    connection = get_db_connection()

    tasks = connection.execute(
        "SELECT * FROM tasks"
    ).fetchall()

    connection.close()

    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
    title = request.form["title"]
    category = request.form["category"]
    priority = request.form["priority"]

    connection = get_db_connection()

    connection.execute(
        """
        INSERT INTO tasks (title, category, priority)
        VALUES (?, ?, ?)
        """,
        (title, category, priority)
    )

    connection.commit()
    connection.close()

    return redirect("/")


@app.route("/complete/<int:task_id>")
def complete_task(task_id):
    connection = get_db_connection()

    connection.execute(
        "UPDATE tasks SET completed = 1 WHERE id = ?",
        (task_id,)
    )

    connection.commit()
    connection.close()

    return redirect("/")


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    connection = get_db_connection()

    connection.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    connection.commit()
    connection.close()

    return redirect("/")


if __name__ == "__main__":
    create_table()
    app.run(debug=True)
