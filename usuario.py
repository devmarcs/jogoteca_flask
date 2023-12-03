from flask import render_template,request, redirect,url_for, flash, session, send_from_directory
from app import app, db 
from models.modelos import Usuarios, Jogos
from views import *



#--------------- Tela Cadastrar Usuário --------------------
@app.route('/cad_usuario')
def cad_usuario():
    return render_template('novo_usuario.html')



#---------------- Rota cadastrar cliente -----------------------

@app.route('/cadastar-se',methods=['POST', 'GET'])
def cadastro_cliente():
    
    nome = request.form['nome']
    username = request.form['username']
    senha = request.form['senha']

    usuario = Usuarios.query.filter_by(nome=nome).first()
    if usuario:
        flash('Usuário já cadastrado no sistema!')
        return redirect(url_for('login'))

    novo_usuario = Usuarios(nome=nome, username=username, senha=senha)
    db.session.add(novo_usuario)
    db.session.commit()

    arquivo = request.files['arquivo']
    upload_path_user = app.config['UPLOAD_PATH_USER']
    arquivo.save(f'{upload_path_user}/capa{novo_usuario.id}.jpg')

    flash('Usuário cadastrado com sucesso!')
    return redirect(url_for('login'))
    

#------------------- Tela Editar Usuário ----------------------

@app.route('/editar_usuario/<int:id>')  
def editar_usuario(id):
    from views import verificação
    verificação('editar_usuario')
    usuario = Usuarios.query.filter_by(id=id).first()
    flash('Usuário atualizado com sucesso!')
    return render_template('editar_usuario.html',usuario=usuario)



#---------------- Função que faz a edição do usuário ---------------------

@app.route('/atualizar_user', methods= ['POST']) 
def atualizar_user():
    usuario = Usuarios.query.filter_by(id=request.form['id']).first()
    usuario.nome = request.form['nome']
    usuario.username = request.form['username']
    usuario.senha = request.form['senha']

    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for('jogos'))


#===== Função que deleta o Usuário =====
@app.route('/deletar_usuario/<int:id>')
def deletar_usuario(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    
    Usuarios.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Usuário deletado com sucesso!')
    return redirect(url_for('index'))





