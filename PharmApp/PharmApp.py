from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Creiamo il database e la tabella se non esistono
def init_db():
    conn = sqlite3.connect("pharmapp.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS medicines (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 type TEXT,
                 availability TEXT,
                 expiry DATE
                 )""")
    conn.commit()
    conn.close()

init_db()

# Pagina principale
@app.route("/")
def index():
    conn = sqlite3.connect("pharmapp.db")
    c = conn.cursor()
    c.execute("SELECT * FROM medicines")
    medicines = c.fetchall()
    conn.close()
    return render_template("index.html", medicines=medicines)

# Aggiungi nuovo medicinale
@app.route("/add", methods=["POST"])
def add_medicine():
    name = request.form.get("name")
    med_type = request.form.get("type")
    availability = request.form.get("availability")
    expiry = request.form.get("expiry")
    conn = sqlite3.connect("pharmapp.db")
    c = conn.cursor()
    c.execute("INSERT INTO medicines (name, type, availability, expiry) VALUES (?, ?, ?, ?)",
              (name, med_type, availability, expiry))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

# Elimina medicinale
@app.route("/delete/<int:med_id>")
def delete_medicine(med_id):
    conn = sqlite3.connect("pharmapp.db")
    c = conn.cursor()
    c.execute("DELETE FROM medicines WHERE id=?", (med_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

# Modifica medicinale
@app.route("/edit/<int:med_id>", methods=["GET", "POST"])
def edit_medicine(med_id):
    conn = sqlite3.connect("pharmapp.db")
    c = conn.cursor()
    if request.method == "POST":
        name = request.form.get("name")
        med_type = request.form.get("type")
        availability = request.form.get("availability")
        expiry = request.form.get("expiry")
        c.execute("UPDATE medicines SET name=?, type=?, availability=?, expiry=? WHERE id=?",
                  (name, med_type, availability, expiry, med_id))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    else:
        c.execute("SELECT * FROM medicines WHERE id=?", (med_id,))
        medicine = c.fetchone()
        conn.close()
        return render_template("edit.html", medicine=medicine)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")