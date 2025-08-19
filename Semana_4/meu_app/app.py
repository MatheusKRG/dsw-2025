from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo

app = Flask(__name__)

app.config['SECRET_KEY']= 'uma_chave_de_segurança_muito_dificil'

class MeuFormulario(FlaskForm):
    nome = StringField('Nome completo', validators=[DataRequired(message='Campo obrigatório')])
    email = StringField('E-mail', validators=[DataRequired('Campo obrigatório'), Email(message='Por favor, insira um e-mail valido.')])
    submit = SubmitField("Enviar")

class FormularioRegistro(FlaskForm):
    nome = StringField('Nome completo', validators=[DataRequired(message="Este campo é obrigatório")])
    email = StringField('Insira seu E-mail', validators=[
        DataRequired(message="Este campo é obrigatório."),
        Email(message="Por favor, insira um e-mail válido.")])
    senha= PasswordField('Senha', validators=[DataRequired(message="Este campo é obrigatório"), Length(min=8, message="A senha deve ter no mínimo 8 caracteres")])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[DataRequired(message="Este campo é obrigatório"), EqualTo('senha', message="As senhas devem ser iguais")])
    biografia = TextAreaField('Biografia (Opcional)')
    aceitar_termos = BooleanField('Aceito os termos de serviço', validators=[DataRequired(message="Você deve aceitar os termos.")])
    submit = SubmitField('Registrar')



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    form = MeuFormulario()

    if form.validate_on_submit():
        nome_usuario = form.nome.data
        email_usuario = form.email.data
        flash(f'Cadastro recebido para {nome_usuario} e {email_usuario}')
        return redirect(url_for('formulario'))
    return render_template('formulario.html', form=form)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form = FormularioRegistro()
    if form.validate_on_submit():
        nome_usuario = form.nome.data
        biografia = form.biografia.data if form.biografia.data else "Nenhuma biografia fornecida."
        flash(f'Registro bem-sucedido para {nome_usuario}! Biografia: {biografia}', 'success')
        return redirect(url_for('registro'))
    return render_template('registro.html', form=form)


if __name__ == '__main__':
    app.run(debug = True)