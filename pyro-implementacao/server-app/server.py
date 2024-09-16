import json
import Pyro5.server
import Pyro5.core
import funcionalidades

@Pyro5.server.expose
class Server(object):
    
    def criar_conta(self, username, senha):
        return funcionalidades.criar_conta(username, senha)
    
    def login(self, username, senha):
        return funcionalidades.login(username, senha)
    
    def logout(self, username):
        return funcionalidades.logout(username)
    
    def adicionar_baralho(self, username, baralho):
        return funcionalidades.adicionar_baralho(username, baralho)
    
    def excluir_baralho(self, username, indice):
        return funcionalidades.excluir_baralho(username, indice)
    
    def adicionar_carta(self, username, carta):
        return funcionalidades.adicionar_carta_colecao(username, carta)
    
    def exibir_perfil(self, username):
        confirmation = funcionalidades.exibir_perfil(username)
        if isinstance(confirmation, dict):
            confirmation = json.dumps(confirmation) 
        return confirmation
    
    def montar_baralho(self, username):
        return funcionalidades.montar_baralho(username)

    def exibir_baralhos(self, username):
        return funcionalidades.exibir_baralhos(username)

    def criar_partida(self, username_dono, username2, username3):
        return funcionalidades.criar_partida(username_dono, username2, username3)

    def resposta_convite(self, username, id_partida, resposta):
        funcionalidades.set_resposta_usuario(int(id_partida), username, resposta)
        
    def escolha_baralho(self, username, id_partida):
        resposta = 'preparado'
        funcionalidades.set_resposta_usuario(int(id_partida), username, resposta)

    def jogada_turno(self, username, emocao, id_partida):
        resposta = 'escolheu'
        funcionalidades.set_resposta_usuario(int(id_partida), username, resposta)
        funcionalidades.cartas_jogadas_turno(int(id_partida), username, emocao)

def start_server():
    daemon = Pyro5.server.Daemon(host="localhost")
    ns = Pyro5.core.locate_ns()
    uri = daemon.register(Server)
    ns.register("server", uri)
    print("Ready. Object uri =", uri)
    daemon.requestLoop()

if __name__ == "__main__":
    start_server()
    