from flask import Flask, render_template,request, redirect,url_for, flash, session
from models.usuarios import Usuario, usuario1, usuario2, usuario3, usuario4

class Jogo():
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

jogo1 = Jogo('Tetris', 'Puzzle', 'Atari')
jogo2 = Jogo('Clash Royale', 'Estratégia', 'Mobile')
lista = [jogo1, jogo2]

app = Flask(__name__)
app.secret_key = 'marc123'

@app.route('/')
def index():
    return render_template('inicio.html')


@app.route('/jogos')
def jogos():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('cadastro')))
    return render_template('lista.html',jogos= lista)

@app.route('/cadastre')
def cadastro():
    return render_template('novo_jogo.html')



@app.route('/criar', methods= ['POST'])
def criado():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    flash('Jogo cadastrado com sucesso!')
    return redirect(url_for('jogos'))
   


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)



@app.route('/autenticar', methods=['GET', 'POST'])
def autenticar():
    usuarios = {
        usuario1.username : usuario1,
        usuario2.username : usuario2,
        usuario3.username : usuario3
        }
    
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.username
            flash(f'{usuario.username}   logado com sucesso')
            proxima_pagina =request.form['proxima']
            return redirect('/jogos')
    flash('Usuário não logado')
    return redirect(url_for(proxima_pagina))
       

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Usuário deslogado com sucesso!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
    