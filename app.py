from flask import Flask, render_template,request, redirect,url_for, flash, session

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
    return redirect(url_for('jogos'))
   


@app.route('/login')
def login():
    return render_template('login.html')



@app.route('/autenticar', methods=['GET', 'POST'])
def autenticar():
    if 'eusoufodao' == request.form['senha']:
        session["usuario_logado"] = request.form['usuario']
        flash('Usuário' + session["usuario_logado"] + 'logado com sucesso')
        return redirect('/jogos')
    flash('Usuário não logado')
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)
    