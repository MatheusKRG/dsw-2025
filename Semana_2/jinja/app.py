from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    usuario = 'Matheus'
    return render_template('index.html', nome_usuario = usuario)

if __name__ == 'main' :
    app.run(host='0.0.0.0', port=5000, debug=True)