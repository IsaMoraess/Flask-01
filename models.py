from flask_appbuilder import SQLA, Model
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

db = SQLA()

class Aluno(Model):
    __tablename__ = 'aluno'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    escola_id = Column(Integer, ForeignKey('escola.id'), nullable=True)#FK

    escola = relationship('Escola', back_populates='alunos')

class Escola(Model):
    __tablename__ = 'escola'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)

    alunos = relationship('Aluno', back_populates='escola')