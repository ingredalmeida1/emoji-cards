from funcionalidades import *
import socket
import threading
import json

def handle_client(client_socket):
    request = client_socket.recv(1024).decode('utf-8')
    print(f"requisicao recebida pelo servidor de app: {request}")

    try:
        if request.startswith('criar_conta'):
            _, username, senha = request.split(',')
            confirmation = criar_conta(username, senha)
            client_socket.send(confirmation.encode('utf-8'))

        if request.startswith('login'):
            _, username, senha = request.split(',')
            client_ip, client_port = client_socket.getpeername()
            confirmation = login(username, senha, client_ip, client_port)
            client_socket.send(confirmation.encode('utf-8'))

        if request.startswith('logout'):
            _, username = request.split(',')
            confirmation = logout(username)
            client_socket.send(confirmation.encode('utf-8'))

        if request.startswith('adicionar_baralho'):
            _, username, baralho = request.split(',', 2)
            print(f'baralho que recebi: {baralho}')
            confirmation = adicionar_baralho(username, baralho)
            client_socket.send(confirmation.encode('utf-8'))

        if request.startswith('excluir_baralho'):
            _, username, indice = request.split(',')
            confirmation = excluir_baralho(username, indice)
            client_socket.send(confirmation.encode('utf-8'))

        if request.startswith('adicionar_carta'):
            _, username, carta = request.split(',')
            confirmation = adicionar_carta_colecao(username, carta)
            client_socket.send(confirmation.encode('utf-8'))

        if request.startswith('exibir_perfil'):
            _, username = request.split(',')
            confirmation = exibir_perfil(username)
            
            if isinstance(confirmation, dict):
                confirmation = json.dumps(confirmation) 

            client_socket.send(confirmation.encode('utf-8')) 

        if request.startswith('montar_baralho'):
            _, username = request.split(',')
            confirmation = montar_baralho(username)
            client_socket.send(confirmation.encode('utf-8'))

        if request.startswith('exibir_baralhos'):
            _, username = request.split(',')
            confirmation = exibir_baralhos(username)
            client_socket.send(confirmation.encode('utf-8'))

        if request.startswith('criar_partida'):
            _, username_dono, username2, username3 = request.split(',')
            confirmation = criar_partida(username_dono, username2, username3)
            # client_socket.send(confirmation.encode('utf-8')) # a criar partida retorna a resposta pelo canal aberto com o cliente

        if request.startswith('resposta_convite'):
            _, username, id_partida, resposta = request.split(',')
            set_resposta_usuario(int(id_partida), username, resposta)

        if request.startswith('escolha_baralho'):
            _, username, id_partida = request.split(',')
            resposta = 'preparado'
            set_resposta_usuario(int(id_partida), username, resposta)

        if request.startswith('jogada_turno'):
            _, username, emocao, id_partida = request.split(',')
            resposta = 'escolheu'
            set_resposta_usuario(int(id_partida), username, resposta)
            cartas_jogadas_turno(int(id_partida), username, emocao)
            
    except Exception as e:
        confirmation = f"erro ao lidar com requisicao {request}: {str(e)}"
        print(confirmation)
        client_socket.send(confirmation.encode('utf-8'))
    finally:
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind(("0.0.0.0", 5000))
        server.listen()
        print("servidor de aplicação ouvindo na porta 5000...")
    except socket.error as e:
        print(f"erro ao inicializar o servidor de aplicacao: {str(e)}")
        return
    

    while True:
        client_socket, addr = server.accept()
        print(f"conexão aceita de {addr}")

        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
