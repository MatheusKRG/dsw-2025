from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        msg = request.form.get("msg")
        return render_template("resultado.html", nome = nome, email = email, msg = msg)
    
    return render_template("index.html")
if __name__ == "__main__":
    app.run(debug=True)