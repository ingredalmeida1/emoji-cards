from infra.configs.base import Base
from sqlalchemy import Column, Integer, String

class Usuario(Base):
    __tablename__ = 'usuario'
    username = Column(String, primary_key=True)
    senha = Column(String)
    status = Column(String) #jogando - online - offline
    colecao_cartas = Column(String) #string: 'carta1', 'carta2',.. -> fazer split(,) para pegar cada carta
    qtd_baralhos = Column(Integer)
    baralhos = Column(String) #string: 'baralho1'-'baralho2'-'baralho3' -> fazer split(-) para pegar cada baralho
