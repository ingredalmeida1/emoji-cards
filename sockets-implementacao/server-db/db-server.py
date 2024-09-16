'''
Threads deverão ser utilizadas nesta implementação de forma bastante simples: o
processo servidor deverá utilizar uma thread para recepcionar as requisições recebidas e
outra(s) para processá-las.
'''

import socket
import threading

import interface #arquivo interface.py vai funcionar como uma biblioteca

# função para lidar com as requisições dos clientes
def handle_client(client_socket):
    request = client_socket.recv(1024).decode('utf-8')  # convert bytes to string
    print(f"requisicao recebida pelo db: {request}")

    if request.startswith('cartas_disponiveis'):
        try:
            _, response = interface.get_emocoes_cadastradas() 
            client_socket.send(response.encode('utf-8')) # convert string to bytes
        except Exception as e:
            response = f"erro: {str(e)}"
            client_socket.send(response.encode('utf-8')) # convert string to bytes
        
    elif request.startswith('atributos_carta'):
        try:
            _, emocao = request.split(' ')
            _, response = interface.get_atributos_carta(emocao) 
            client_socket.send(response.encode('utf-8')) # convert string to bytes
        except Exception as e:
            response = f"erro: {str(e)}"
            client_socket.send(response.encode('utf-8')) # convert string to bytes
    
    
    elif request.startswith('adicionar_usuario'):
        try:
            _, username, senha, cartas = request.split(' ')
            _, response = interface.adicionar_usuario(username, senha, cartas) 
            client_socket.send(response.encode('utf-8')) # convert string to bytes
        except Exception as e:
            response = f"erro: {str(e)}"
            client_socket.send(response.encode('utf-8')) # convert string to bytes
    
    elif request.startswith('verificar_username'):
        try:
            _, username = request.split(' ')
            _, response = interface.verificar_username_existe(username) 
            client_socket.send(response.encode('utf-8')) # convert string to bytes
        except Exception as e:
            response = f"erro: {str(e)}"
            client_socket.send(response.encode('utf-8')) # convert string to bytes
    
    elif request.startswith('verificar_login'):
        try:
            _, username,senha = request.split(' ')
            _, response = interface.verificar_login(username,senha) 
            client_socket.send(response.encode('utf-8')) # convert string to bytes
        except Exception as e:
            response = f"erro: {str(e)}"
            client_socket.send(response.encode('utf-8')) # convert string to bytes
    
    elif request.startswith('buscar_usuario'):
        try:
            _, username = request.split(' ')
            _, response = interface.buscar_usuario(username) 
            client_socket.send(response.encode('utf-8')) # convert string to bytes
        except Exception as e:
            response = f"erro: {str(e)}"
            client_socket.send(response.encode('utf-8')) # convert string to bytes
    
    elif request.startswith('get_status'):
        try:
            _, username = request.split(' ')
            _, response = interface.get_status(username) 
            client_socket.send(response.encode('utf-8')) # convert string to bytes
        except Exception as e:
            response = f"erro: {str(e)}"
            client_socket.send(response.encode('utf-8')) # convert string to bytes
    
    elif request.startswith('set_status'):
        try:
            _, username,status = request.split(' ')
            _, response = interface.set_status(username,status) 
            client_socket.send(response.encode('utf-8')) # convert string to bytes
        except Exception as e:
            response = f"erro: {str(e)}"
            client_socket.send(response.encode('utf-8')) # convert string to bytes
    
    elif request.startswith('get_colecao'):
        try:
            _, username = request.split(' ')
            _, response = interface.get_colecao(username) 
            client_socket.send(response.encode('utf-8')) # convert string to bytes
        except Exception as e:
            response = f"erro: {str(e)}"
            client_socket.send(response.encode('utf-8')) # convert string to bytes
    
    
    elif request.startswith('adicionar_carta_na_colecao'):
        try:
            _, username,emocao = request.split(' ')
            _, response = interface.adicionar_carta_na_colecao(username, emocao)
            client_socket.send(response.encode('utf-8')) # convert string to bytes
        except Exception as e:
            response = f"erro: {str(e)}"
            client_socket.send(response.encode('utf-8')) # convert string to bytes
    
    elif request.startswith('get_baralhos'):
        try:
            _, username = request.split(' ')
            _, response = interface.get_baralhos(username) 
            client_socket.send(response.encode('utf-8')) # convert string to bytes
        except Exception as e:
            response = f"erro: {str(e)}"
            client_socket.send(response.encode('utf-8')) # convert string to bytes
    
    elif request.startswith('get_qtd_baralhos'):
        try:
            _, username = request.split(' ')
            _, response = interface.get_qtd_baralhos(username) 
            client_socket.send(response.encode('utf-8')) # convert string to bytes
        except Exception as e:
            response = f"erro: {str(e)}"
            client_socket.send(response.encode('utf-8')) # convert string to bytes
    
    elif request.startswith('adicionar_baralho'):
        try:
            _, username,baralho = request.split(' ')
            _, response = interface.adicionar_baralho(username, baralho)
            client_socket.send(response.encode('utf-8')) # convert string to bytes
        except Exception as e:
            response = f"erro: {str(e)}"
            client_socket.send(response.encode('utf-8')) # convert string to bytes
    
    elif request.startswith('excluir_baralho'):
        try:
            _, username,indice = request.split(' ')
            _, response = interface.excluir_baralho(username, indice)
            client_socket.send(response.encode('utf-8')) # convert string to bytes
        except Exception as e:
            response = f"erro: {str(e)}"
            client_socket.send(response.encode('utf-8')) # convert string to bytes
    
    else:
        response = f"erro: mensagem não foi combinada"
        client_socket.send(response.encode('utf-8')) # convert string to bytes
    
    print(f"\nresposta db: {response}")
    
    #finaliza thread
    client_socket.close()

# SERVIDOR DB
'''
usando um loop infinito na thread principal para aceitar conexões e, 
em seguida, cria uma nova thread para lidar com cada conexão do cliente. 
'''
def start_db_server():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        server_ip = '0.0.0.0'
        server_port = 6000
        server.bind((server_ip, server_port))
        server.listen(10)
        print("servidor de banco de dados ouvindo na porta 6000...")
    except socket.error as e:
        print(f"erro ao inicializar o servidor de aplicacao: {str(e)}")
        return
    
    while True:
        client_socket, addr = server.accept()
        print(f"conexão aceita de {addr}")
        
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

def main():
    interface.iniciar_banco_dados() #se não existe banco de dados, cria as tabelas e adiciona as 24 cartas disponíveis
    start_db_server()

if __name__ == "__main__":
    main()