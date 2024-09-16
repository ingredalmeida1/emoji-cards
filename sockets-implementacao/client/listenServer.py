import socket
import threading
from lidarSocket import ManipularSocket
import random
from time import sleep

class ListenServer(ManipularSocket):
    def __init__(self, server_ip="127.0.0.1", server_porta=5000):
        self.username = None
        self.mensagem_servidor = None
        super().__init__(server_ip, server_porta)


    def handle_server(self, client_ip, client_port):
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind(('0.0.0.0', int(client_port)))
            server.listen(1)

            print(f"cliente escutando em {client_ip}:{client_port}\n")

            while True:
                try:
                    server_socket, addr = server.accept()
                    print(f"Conexão recebida de {addr}")
                    request = self.receber_dados(server_socket)
                    if request:
                        thread = threading.Thread(target=self.__manipular_mensagem, args=(request,))
                        thread.start()
                        
                    
                except Exception as e:
                    print(f"Erro ao ouvir mensagem do servidor: \n{e}")
        except Exception as e:
                    print(f"Erro ao tentar criar conexão disponível ao servidor {client_ip}:{client_port} \n{e}")
    

    def __manipular_mensagem(self, request):
        #t = random.choice(range(1,6))
        #sleep(t)
        #print(f'{request}')
        print(f"mensagem recebida do servidor: {request}")
        if request.startswith('convite_partida'):
            #_, username_dono, id_partida = request.split(',')
            self.mensagem_servidor = request
        
        elif request.startswith('partida_criada'):
            # _, id_partida, baralhos = request.split(',', 2)
            self.mensagem_servidor = request
            
        #tem que voltar e olhar resposta
        elif request.startswith('atributo_turno'):
            # _, atributo, id_partida, pontuacao = request.split(',')
            self.mensagem_servidor = request
        
        elif request.startswith('fim_turno'):
            
            #_; vencedor; atributo; id_partida; escolhas_cada_jogador; pontuacao = request.split(';')
            self.mensagem_servidor = request
    
        elif request.startswith('fim_partida'):
           # _, vencedor, carta_adicionada, pontuacao = request.split(',',3)
            self.mensagem_servidor = request
        
        elif request.startswith('fim_partida_empate'):
            #_, vencedor, carta_adicionada = request.split(',')
            self.mensagem_servidor = request

        elif request.lower().startswith('erro'):
            self.mensagem_servidor = request
            

    def responder_convite(self, resposta, id_partida): 
        server_socket =  self.criar_conexao()
        request = f'resposta_convite,{self.username},{id_partida},{resposta}'
        #server_socket.send(request.encode('utf-8'))
        self.enviar_dados(server_socket, request)
        self.fechar_conexao(server_socket)

    
    #avisar que jogador já escolheu o baralho, mas servidor não precisa saber qual foi
    def responder_baralho_escolhido(self, id_partida):
        server_socket = self.criar_conexao()
        request = f'escolha_baralho,{self.username},{id_partida}'
        self.enviar_dados(server_socket, request)
        self.fechar_conexao(server_socket)


    def responder_jogada_turno(self, emocao, id_partida):
        server_socket = self.criar_conexao()
        request = f'jogada_turno,{self.username},{emocao},{id_partida}'
        self.enviar_dados(server_socket, request)
        self.fechar_conexao(server_socket)
