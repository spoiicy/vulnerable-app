from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Create an SQLite database and table
conn = sqlite3.connect('vulnerable.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
conn.commit()

@app.route('/')
def index():
    return render_template_string("""
        <h1>Welcome to the Vulnerable App</h1>
        <form action="/search" method="GET">
            <input type="text" name="username" placeholder="Enter username">
            <button type="submit">Search</button>
        </form>
        <form action="/login" method="POST">
            <input type="text" name="username" placeholder="Username">
            <input type="password" name="password" placeholder="Password">
            <button type="submit">Login</button>
        </form>
    """)

@app.route('/search')
def search():
    username = request.args.get('username')
    # SQL Injection Vulnerability
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    users = cursor.fetchall()
    return f"Users found: {users}"

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    # XSS Vulnerability (insecure rendering of user input)
    return render_template_string(f"""
        <h1>Welcome, {username}!</h1>
        <p>Your password is: {password}</p>
        <script>alert('Welcome to the vulnerable app, {username}!');</script>
    """)

if __name__ == '__main__':
    app.run(debug=True)
