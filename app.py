from flask import Flask, render_template,request, redirect,url_for, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'marc123'

app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(

        SGBD= 'mysql+mysqlconnector',
        usuario= 'root',
        senha= '',
        servidor= 'localhost',
        database= 'jogoteca'
    )



db = SQLAlchemy(app)



    




@app.route('/')
def index():
    return render_template('inicio.html')


@app.route('/jogos')
def jogos():
    
    lista = Jogos.query.order_by(Jogos.id)
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

    jogo = Jogos.query.filter_by(nome=nome).first()
    if jogo:
        flash('Jogo já cadastrado no sistema!')
        return redirect(url_for('jogos'))
    
    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console) 
    db.session.add(novo_jogo)
    db.session.commit()

    flash('Jogo cadastrado com sucesso!')
    return redirect(url_for('jogos'))
   


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)



@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario = Usuarios.query.filter_by(username=request.form['usuario']).first()
    if usuario:
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
    