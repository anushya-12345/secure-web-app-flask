from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "secret123"  # required for session

# Fake username and password for testing
USER = {"username": "admin", "password": "1234"}

# Simple HTML template for login
login_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
</head>
<body style="font-family: Arial; text-align: center; margin-top: 50px;">
    <h2>Login Page</h2>
    <form method="POST">
        <p><input type="text" name="username" placeholder="Username" required></p>
        <p><input type="password" name="password" placeholder="Password" required></p>
        <p><button type="submit">Login</button></p>
    </form>
    {% if error %}
    <p style="color:red;">{{ error }}</p>
    {% endif %}
</body>
</html>
"""

# Dashboard page
dashboard_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard</title>
</head>
<body style="font-family: Arial; text-align: center; margin-top: 50px;">
    <h2>Welcome, {{ user }}!</h2>
    <p>You are now logged in.</p>
    <a href="{{ url_for('logout') }}">Logout</a>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == USER["username"] and password == USER["password"]:
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid username or password!"

    return render_template_string(login_page, error=error)

@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return render_template_string(dashboard_page, user=session["user"])
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)
