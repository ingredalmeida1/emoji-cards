from infra.configs.base import Base
from sqlalchemy import Column, Integer, String

class Carta(Base):
    __tablename__ = 'carta'
    emocao = Column(String, primary_key=True)
    atributos = Column(String) #manter um atributo como um dicionario
    # tempo = Column(String)
    # impacto_social = Column(String)
    # efeito_cognitivo = Column(String) 
    # qtd_emocoes_opostas = Column(Integer) #pro sistema não importa quais, só importa quantas
    # qtd_emocoes_relacionadas = Column(Integer) #pro sistema não importa quais, só importa quantas
    # intensidade = Column(Integer)
