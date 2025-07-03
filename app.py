from flask import Flask, render_template, request, redirect, session, flash, url_for
from db_config import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = '2024@darsh'


@app.route('/')
def home():
    return render_template('index.html')
@app.route('/templates/register.html', methods=['GET', 'POST'])

def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            flash('Email already registered.')
            return redirect(url_for('register'))

        # InsertUser
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                       (name, email, password))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)