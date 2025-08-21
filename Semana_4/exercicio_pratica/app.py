import os
from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.fields import DateField
from wtforms.validators import ValidationError
import datetime
from wtforms.validators import DataRequired, Email

# --- Configuração da Aplicação Flask ---
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# --- Definição do Formulário com WTForms ---
class EventoForm(FlaskForm):
	nome_evento = StringField(
		'Nome do Evento',
		validators=[DataRequired(message="O campo nome do evento é obrigatório.")]
	)
	tipo_evento = SelectField(
		'Tipo do Evento',
		choices=[
			('Palestra', 'Palestra'),
			('Workshop', 'Workshop'),
			('Meetup', 'Meetup'),
			('Outro', 'Outro')
		],
		validators=[DataRequired(message="O campo tipo do evento é obrigatório.")]
	)
	data_evento = DateField(
		'Data do Evento',
		validators=[DataRequired(message="O campo data do evento é obrigatório.")]
	)

	def validate_data_evento(self, field):
		if field.data and field.data < datetime.date.today():
			raise ValidationError("A data do evento não pode ser no passado.")

	organizador = StringField(
		'Organizador',
		validators=[DataRequired(message="O campo organizador é obrigatório.")]
	)
	email = StringField(
		'E-mail',
		validators=[
			DataRequired(message="O campo e-mail é obrigatório."),
			Email(message="Por favor, insira um e-mail válido.")
		]
	)
	descricao = TextAreaField('Descrição')
	enviar = SubmitField('Enviar')

	def validate_descricao(self, field):
		if self.tipo_evento.data == 'Outro' and not field.data:
			raise ValidationError('O campo descrição é obrigatório para eventos do tipo "Outro".')

# --- Definição de um Objeto para Simulação ---
class Usuario:
	def __init__(self, nome, email, mensagem=""):
		self.nome = nome
		self.email = email
		self.mensagem = mensagem

# --- Rotas da Aplicação ---
@app.route("/")
def index():
	return render_template('index.html')

@app.route("/vazio", methods=['GET', 'POST'])
def formulario_vazio():
	form = EventoForm()
	# Esta condição agora verifica se o formulário foi submetido e é válido.
	# Se não for válido, a renderização da página abaixo irá incluir os erros.
	if form.validate_on_submit():
		# Se a validação passar, podemos processar os dados.
		# Por exemplo, mostrar uma mensagem de sucesso.
		nome_usuario = form.organizador.data
		return render_template('sucesso.html', nome_usuario=nome_usuario)
	# Se a requisição for GET ou a validação falhar, renderiza o template.
	# Se a validação falhou, form.errors terá as mensagens para o template exibir.
	return render_template(
		'formulario.html',
		form=form,
		title="1. Formulário Vazio"
	)

@app.route("/via-argumentos", methods=['GET', 'POST'])
def formulario_via_argumentos():
	form = EventoForm()  # Instancia vazio primeiro para receber dados do POST
	# validate_on_submit processa os dados enviados. Se for um GET, ele pula.
	if form.validate_on_submit():
		nome_usuario = form.organizador.data
		return render_template('sucesso.html', nome_usuario=nome_usuario)
	# Se for uma requisição GET (primeira visita à página), preenchemos com dados iniciais.
	elif not form.is_submitted():
		dados_iniciais = {
			'organizador': 'João da Silva',
			'email': 'joao.silva@email.com',
			'mensagem': 'Esta é uma mensagem preenchida por argumentos.'
		}
		form = EventoForm(**dados_iniciais)
	return render_template(
		'formulario.html',
		form=form,
		title="2. Formulário Preenchido via Argumentos"
	)

@app.route("/via-objeto", methods=['GET', 'POST'])
def formulario_via_objeto():
	form = EventoForm()
	if form.validate_on_submit():
		nome_usuario = form.organizador.data
		return render_template('sucesso.html', nome_usuario=nome_usuario)
	elif not form.is_submitted():
		usuario_mock = Usuario(
			nome="Maria Oliveira",
			email="maria.o@email.net",
			mensagem="Mensagem vinda de um objeto."
		)
		# Passar o nome do organizador corretamente
		form = EventoForm(data={
			'organizador': usuario_mock.nome,
			'email': usuario_mock.email,
			'mensagem': usuario_mock.mensagem
		})
	return render_template(
		'formulario.html',
		form=form,
		title="3. Formulário Preenchido via Objeto"
	)

# --- Execução da Aplicação ---
if __name__ == '__main__':
	app.run(debug=True)
