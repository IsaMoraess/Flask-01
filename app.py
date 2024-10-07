from flask import Flask, request, jsonify
from flask_appbuilder import AppBuilder, SQLA, Model
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config import Config

#INICIANDO O FLASK E O BD
app = Flask(__name__)
app.config.from_object(Config)
db = SQLA(app)
appbuilder = AppBuilder(app, db.session)

#DEFININDO ALUNO
class Aluno(Model):
    __tablename__ = 'aluno'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    escola_id = Column(Integer, ForeignKey('escola.id'), nullable=True)

    #RELACIONAMENTO CM ESCOLA
    escola = relationship('Escola', back_populates='alunos')

#DEFININDO ESCOLA
class Escola(Model):
    __tablename__ = 'escola'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)

    #RELACIONAMENTO CM ALUNO
    alunos = relationship('Aluno', back_populates='escola')

#CRIANDO TABELAS NO BD
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "Bem-vindo ao seu aplicativo Flask!"

@app.route('/alunos', methods=['POST'])
def cadastrar_aluno():
    data = request.get_json()#TEM DADOS DO JSON EM REQUISIÇÃO
    nome = data.get('nome')#PEGA O NOME DO ALUNO NO JSON
    escola_id = data.get('escola_id')#PEGA ID DA ESCOLA NO JSON

    if not nome:
        return jsonify({'error': 'Nome é obrigatório!'}), 400

    novo_aluno = Aluno(nome=nome, escola_id=escola_id)#INSTANCIA NOVA DE ALUNO
    db.session.add(novo_aluno)#COLOCA NOVO ALUNO NO BD
    db.session.commit()#SALVA NO BD

    return jsonify({'message': 'Aluno cadastrado com sucesso!', 'id': novo_aluno.id}), 201

@app.route('/escolas', methods=['POST'])
def cadastrar_escola():
    data = request.get_json()  
    nome = data.get('nome')  

    if not nome:
        return jsonify({'error': 'Nome é obrigatório!'}), 400

    nova_escola = Escola(nome=nome)  
    db.session.add(nova_escola) 
    db.session.commit() 

    return jsonify({'message': 'Escola cadastrada com sucesso!', 'id': nova_escola.id}), 201

#ROTA P/ LISTAR TDS ALUNOS
@app.route('/alunos', methods=['GET'])
def listar_alunos():
    alunos = Aluno.query.all()  #CONSULTAR TDS ALUNOS
    alunos_list = [{'id': aluno.id, 'nome': aluno.nome, 'escola_id': aluno.escola_id} for aluno in alunos]
    return jsonify(alunos_list), 200

#ROTA P/ LISTAR TDS ESCOLAS
@app.route('/escolas', methods=['GET'])
def listar_escolas():
    escolas = Escola.query.all()#CONSULTA TDS ESCOLAR
    escolas_list = [{'id': escola.id, 'nome': escola.nome} for escola in escolas]
    return jsonify(escolas_list), 200

if __name__ == "__main__":
    app.run(debug=True)