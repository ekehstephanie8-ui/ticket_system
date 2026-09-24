from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import date

app = Flask(__name__)

def get_db_connection():
    connection = sqlite3.connect("tickets.db")
    connection.row_factory = sqlite3.Row
    return connection

@app.route("/")
def index():
    connection = get_db_connection()
    tickets = connection.execute("SELECT * FROM tickets ORDER BY id ASC").fetchall()
    connection.close()
    return render_template("index.html", tickets=tickets)

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        user_name = request.form["user_name"]
        title = request.form["title"]
        description = request.form["description"]
        category = request.form["category"]
        priority = request.form["priority"]
        today = date.today().strftime("%Y-%m-%d")

        connection = get_db_connection()
        connection.execute(
            "INSERT INTO tickets (user_name, title, description, category, priority, status, date_created) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (user_name, title, description, category, priority, "Pending", today)
        )
        connection.commit()
        connection.close()
        return redirect(url_for("index"))

    return render_template("create.html")

@app.route("/update/<int:ticket_id>", methods=["GET", "POST"])
def update(ticket_id):
    connection = get_db_connection()

    if request.method == "POST":
        new_status = request.form["status"]
        connection.execute(
            "UPDATE tickets SET status = ? WHERE id = ?",
            (new_status, ticket_id)
        )
        connection.commit()
        connection.close()
        return redirect(url_for("index"))

    ticket = connection.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,)).fetchone()
    connection.close()
    return render_template("update.html", ticket=ticket)

@app.route("/delete/<int:ticket_id>")
def delete(ticket_id):
    connection = get_db_connection()
    connection.execute("DELETE FROM tickets WHERE id = ?", (ticket_id,))
    connection.commit()
    connection.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)