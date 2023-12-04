from flask import render_template,request, redirect,url_for, flash, session, send_from_directory
from app import app, db
from models.modelos import Usuarios, Jogos

@app.route('/')
def index():
    return render_template('inicio.html')

#===== Tela lista de jogos =====
@app.route('/jogos' )
def jogos():
    nome = session['usuario_logado']
    lista = Jogos.query.order_by(Jogos.id)
    usuario = Usuarios.query.filter_by(username=nome).first()
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('cadastro')))
    return render_template('lista.html',jogos= lista, usuario=usuario)

@app.route('/cadastre')
def cadastro():
    return render_template('novo_jogo.html')


#===== Tela de criar jogos =====
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

    '''arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    arquivo.save(f'{upload_path}/capa{novo_jogo.id}.jpg')
    '''

    flash('Jogo cadastrado com sucesso!')
    return redirect(url_for('jogos'))
   
#===== Tela editar jogos =====
@app.route('/editar_jogo/<int:id>')
def editar_jogo(id):
    
    verificação('editar_jogo')
    jogo = Jogos.query.filter_by(id=id).first()
    return render_template('editar_jogo.html',jogo= jogo)

#===== Função que faz a edição dos jogos =====
@app.route('/atualizar', methods= ['POST']) 
def atualizar():
    jogo = Jogos.query.filter_by(id=request.form['id']).first()
    jogo.nome = request.form['nome']
    jogo.categoria = request.form['categoria']
    jogo.console = request.form['console']

    db.session.add(jogo)
    db.session.commit()
    return redirect(url_for('jogos'))


#===== Função que deleta os jogos =====
@app.route('/deletar_jogo/<int:id>')
def deletar_jogo(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    
    Jogos.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Jogo deletado com sucesso!')
    return redirect(url_for('jogos'))



#===== Tela de login do usuário =====
@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


#===== Função que verifica a autetticação do usuário =====
@app.route('/autenticar', methods=['POST',])
def autenticar():
    nome_usuario = request.form['usuario']
    usuario = Usuarios.query.filter_by(username=nome_usuario).first()
    if usuario:
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.username
            flash(f'{usuario.username}   logado(a) com sucesso')
            #proxima_pagina =request.form['proxima']
            return redirect('/jogos')
    flash('Usuário não logado')
    return redirect(url_for('login'))
       
#===== Função que faz o logout da sessão do usuário =====
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    session.clear()
    flash('Usuário deslogado com sucesso!')
    return redirect(url_for('index'))


def verificação(rota):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for(rota)))
    

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)