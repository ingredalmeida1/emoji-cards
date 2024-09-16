import Pyro5.server
import Pyro5.core

import interface

@Pyro5.server.expose
class Database(object):
    def get_cartas_disponiveis(self):
        return interface.get_emocoes_cadastradas()
    
    def get_atributos_carta(self,emocao):
        return interface.get_atributos_carta(emocao)
    
    def adicionar_usuario(self, username, senha, cartas):
        return interface.adicionar_usuario(username, senha, cartas) 
    
    def verificar_username(self,username):
        return interface.verificar_username_existe(username)
    
    def verificar_login(self,username,senha):
        return interface.verificar_login(username,senha)
    
    def buscar_usuario(self,username):
        return interface.buscar_usuario(username) 

    def get_status(self, username):
        return interface.get_status(username)
    
    def set_status(self, username, status):
        return interface.set_status(username, status)
    
    def get_colecao(username):
        return interface.get_colecao(username)

    def adicionar_carta_na_colecao(self, username, emocao):
        return interface.adicionar_carta_na_colecao(username, emocao)

    def get_baralhos(self, username):
        return interface.get_baralhos(username)

    def get_qtd_baralhos(self, username):
        return interface.get_qtd_baralhos(username)
    
    def adicionar_baralho(self, username, baralho):
        return interface.adicionar_baralho(username, baralho)
    
    def excluir_baralho(self, username, indice):
        return interface.excluir_baralho(username, indice)

def start_db_server():
    daemon = Pyro5.server.Daemon(host="localhost")
    ns = Pyro5.core.locate_ns()
    uri = daemon.register(Database)
    ns.register("db-server", uri)
    print("Ready. Object uri =", uri)
    daemon.requestLoop()

def main():
    interface.iniciar_banco_dados() #se não existe banco de dados, cria as tabelas e adiciona as 24 cartas disponíveis
    start_db_server()

if __name__ == "__main__":
    main()
