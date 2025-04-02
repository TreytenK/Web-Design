from flask import Flask, request, jsonify, render_template, send_from_directory
import sqlite3
import os

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('mlb.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        message TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

@app.route('/')
def index():
    return send_from_directory('.', 'Index.html')

@app.route('/contact', methods=['POST'])
def contact():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    conn = sqlite3.connect('mlb.db')
    c = conn.cursor()
    c.execute('INSERT INTO messages (name, email, message) VALUES (?, ?, ?)', (name, email, message))
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "message": "Message received."})

@app.route('/api/players')
def players():
    players_data = [
        {"name": "Shohei Ohtani", "years": 10},
        {"name": "Juan Soto", "years": 12},
        {"name": "Zack Wheeler", "years": 6},
        {"name": "Aaron Judge", "years": 9},
        {"name": "Jacob deGrom", "years": 5},
        {"name": "Blake Snell", "years": 7},
        {"name": "Gerrit Cole", "years": 9},
        {"name": "Mike Trout", "years": 12},
        {"name": "Anthony Rendon", "years": 7},
        {"name": "Francisco Lindor", "years": 10}
    ]
    return jsonify(players_data)

@app.route('/api/messages')
def get_messages():
    conn = sqlite3.connect('mlb.db')
    c = conn.cursor()
    c.execute('SELECT name, email, message FROM messages')
    messages = [
        {"name": row[0], "email": row[1], "message": row[2]}
        for row in c.fetchall()
    ]
    conn.close()
    return jsonify(messages)

if __name__ == '__main__':
    app.run(debug=True)
