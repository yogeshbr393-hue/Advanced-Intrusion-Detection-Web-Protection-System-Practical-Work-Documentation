from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Login Page
@app.route('/', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Simple Login Check
        if username == "admin" and password == "admin":
            return redirect(url_for('dashboard'))

    return render_template('login.html')


# Dashboard Page
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


# Admin Page
@app.route('/admin')
def admin():
    return render_template('admin.html')


# About Page
@app.route('/about')
def about():
    return render_template('about.html')


# Attack Logs Page
@app.route('/attack_logs')
def attack_logs():
    return render_template('attack_logs.html')


if __name__ == '__main__':
    app.run(debug=True)
