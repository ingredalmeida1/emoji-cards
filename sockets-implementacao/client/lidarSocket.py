import socket

class ManipularSocket:
    def __init__(self, server_ip="127.0.0.1", server_porta=5000):
        self.__server_ip = server_ip
        self.__server_porta = server_porta
        self.__buffer = 1024

    def criar_conexao(self):
        try: 
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((self.__server_ip, self.__server_porta))
            return client
        except Exception as e:
            print(f"Erro ao criar conexao com o servidor: {e}")
            return None
    

    def fechar_conexao(self, client):
        try: 
            client.close()
        except Exception as e:
            print(f"Erro ao fechar conexao como o servidor: {e}")


    def enviar_dados(self, client, request):
        try:
            client.send(request.encode("utf-8"))
        except Exception as e:
            print(f"Erro ao enviar dados: {e}")


    def receber_dados(self, client):
        try:
            response = client.recv(self.__buffer).decode("utf-8")
            return response
        except Exception as e:
            print(f"Erro ao receber dados do socket: {e}")
            return None
