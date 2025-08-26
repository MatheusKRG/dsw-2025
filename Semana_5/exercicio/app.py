from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/nova-receita', methods=['GET', 'POST'])
def nova_receita():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        ingredientes = request.form.get('ingredientes', '').strip()
        modo_preparo = request.form.get('modo_preparo', '').strip()
        if not nome or not ingredientes or not modo_preparo:
            flash('Todos os campos são obrigatórios!')
            return render_template('receita.html')
        return redirect(url_for('receita_criada', nome=nome, ingredientes=ingredientes, modo_preparo=modo_preparo))
    return render_template('receita.html')

@app.route('/receita-criada')
def receita_criada():
    nome = request.args.get('nome', '')
    ingredientes = request.args.get('ingredientes', '')
    modo_preparo = request.args.get('modo_preparo', '')
    return render_template('receita_criada.html', nome=nome, ingredientes=ingredientes, modo_preparo=modo_preparo)

if __name__ == '__main__':
    app.run(debug=True)