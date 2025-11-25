import sqlite3
from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

# Fungsi koneksi database
def get_db():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

# Buat tabel jika belum ada
with get_db() as conn:
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT)')

@app.route('/')
def index():
    conn = get_db()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template_string('''
        <h1>Data Users</h1>
        <table border="1">
            <tr><th>ID</th><th>Name</th><th>Email</th></tr>
            {% for user in users %}
            <tr><td>{{ user['id'] }}</td><td>{{ user['name'] }}</td><td>{{ user['email'] }}</td></tr>
            {% endfor %}
        </table>
        <a href="/add">Tambah User</a>
    ''', users=users)

@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        conn = get_db()
        conn.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template_string('''
        <h1>Tambah User</h1>
        <form method="post">
            Name: <input type="text" name="name"><br>
            Email: <input type="text" name="email"><br>
            <input type="submit" value="Tambah">
        </form>
    ''')

if __name__ == '__main__':
    app.run(debug=True)
