from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DBConnectionHandler:
    
    def __init__(self) -> None:
        self.__connection_string = 'sqlite:///database.db'
        self.__engine = self.__create_database_engine()
        self.session = None
        
    def __create_database_engine(self):
        engine = create_engine(self.__connection_string)
        return engine
    
    def get_engine(self):
        return self.__engine
    
    def __enter__(self): #toda vez que 'entrar' na classe a partir do contexto with, vai executar esse método
        session_make = sessionmaker(bind=self.__engine) # vincular uma sessao na engine
        self.session = session_make() # criando uma sessao basica
        return self #vamos retornar o contexto self
    
    def __exit__(self, exc_type, exc_val, exc_tb): #sempre que sair da classe
        self.session.close() #fecha a sessao
    
    
        