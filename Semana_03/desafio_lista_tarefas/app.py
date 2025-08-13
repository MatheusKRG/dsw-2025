from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

tarefas=[]

@app.route("/")
def index():
    return render_template('index.html', tarefas=tarefas)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    tarefa = request.form['tarefa']
    data_limite = request.form['data_limite']
    
    tarefas.append({'tarefa': tarefa, 'data_limite': data_limite})
    
    return redirect(url_for('sucesso', nome_tarefa=tarefa))

@app.route('/sucesso')
def sucesso():
    nome_tarefa = request.args.get('nome_tarefa', '')
    return render_template('sucesso.html', nome_tarefa=nome_tarefa)


if __name__ == "__main__":
    app.run(debug=True)
