# Criar as rotas do site (links)
from flask import render_template, url_for, redirect
from fakepinterest import app, database, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from fakepinterest.forms import FormLogin, FormCadastro
from fakepinterest.models import Usuario, Foto


@app.route("/", methods=["GET","POST"]) #Caminho (rota) do link para o meu site
def homepage():
    form_login = FormLogin()
    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario)
            return redirect(url_for("perfil", usuario=usuario.username))
    return render_template("homepage.html", form=form_login)

@app.route("/cadastro", methods=["GET","POST"])
def cadastro():
    form_cadastro = FormCadastro()
    if form_cadastro.validate_on_submit():
        senha = bcrypt.generate_password_hash(form_cadastro.senha.data)
        usuario= Usuario(username=form_cadastro.username.data, 
                         email=form_cadastro.email.data, 
                         senha=senha)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("perfil", usuario=usuario.username))
    return render_template("cadastro.html", form=form_cadastro)


@app.route("/perfil/<usuario>")
@login_required
def perfil(usuario):
    return render_template("perfil.html", usuario=usuario)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))