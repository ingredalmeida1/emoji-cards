from collections import Counter
import threading

import random
import json
import ast
import re

import Pyro5.client

import Pyro5.server
import Pyro5.core

class Client(object):
    def __init__(self):
        self.listenServer = None
        self.colecao = None
        self.baralho_escolhido = None
        self.count_turnos = 0
        self.username = None
        self.mensagem_servidor = None
        
        self.daemon = None  # Guardar a referência do daemon


    def get_username(self):
        return self.username

    def __verificar_condicao_baralho(self, baralho):
        if len(baralho) != 9:
            return False, "Baralho deve ter 9 cartas"
        contagem = Counter(baralho)
        for count in contagem.values():
            if count > 3:
                return False, "Deve ter no máximo 3 cartas da mesma emoção"
        return True, "Baralho OK!"
    
    def manipular_baralhos(self, baralhos):
        lista_baralho = []
        if baralhos == '':
            return lista_baralho
        if '-' in baralhos:
            baralhos_aux = baralhos.split('-')
        else:
            baralhos_aux = [baralhos]
        baralhos_aux = baralhos.split('-')
        for baralho in baralhos_aux:
            lista_baralho.append(baralho.split(','))
        return lista_baralho
    
    def validar_username(self, username):
        if len(username) < 5 or len(username) > 15:
            return False, 'Username Inválido: deve ter entre 5 e 15 caracteres'
        if re.match("^[a-zA-Z0-9]*$", username) and re.search("[a-zA-Z]", username):
            return True, 'Username Válido!'
        return False, 'Username Inválido: deve conter apenas letras e números e pelo menos uma letra'
    
    def validar_senha(self,senha):
        if len(senha) != 8:
            return False, f'Senha Inválida: deve ter 8 caracteres'
        if senha.isalnum():
            return True, 'Senha Válida!'
        return False, 'Senha Inválida: deve conter apenas letras e números!'

    # GERENCIAMENTO
    def criar_conta(self, username, senha):
        #validar dados informados
        username_valido, msg = self.validar_username(username)
        if (not username_valido):
            return False, msg
        senha_valida, msg = self.validar_senha(senha)
        if (not senha_valida):
            return False, msg
        
        try:
            server = Pyro5.client.Proxy("PYRONAME:server")
            response = server.criar_conta(username, senha)
            if response == "Usuário adicionado com sucesso!":
                self.login(username,senha)
                return True, response
            return False, response
        except Exception as e:
            print(f"Erro ao criar conta: {str(e)}")
            return False, f"Servidor Indisponível: Reinicie o Sistema!"
    
    @Pyro5.server.expose
    def set_mensagem_servidor(self, mensagem):
        self.mensagem_servidor = mensagem
        
    def start_listen_server(self):
        try:
            self.daemon = Pyro5.server.Daemon(host="localhost")
            ns = Pyro5.core.locate_ns()
            uri = self.daemon.register(self)
            ns.register(self.username, uri)
            print(f"Ready {self.username}. Object uri = {uri}")
            self.daemon.requestLoop()
        except Exception as e:
            print(f"Erro ao iniciar o servidor de escuta: {str(e)}")

    def login(self, username, senha):
        try:
            server = Pyro5.client.Proxy("PYRONAME:server")
            response = server.login(username, senha)
            
            if response == "Login feito com sucesso!":
                self.username = username
                # Inicia o servidor de escuta em uma thread separada
                listen_thread = threading.Thread(target=self.start_listen_server)
                listen_thread.start()
                
                return True, response
            return False, response
        except Exception as e:
            print(f"Erro ao realizar login:{str(e)}")
            return False, f"Servidor Indisponível: Reinicie o Sistema!"

    def logout(self):
        try:
            server = Pyro5.client.Proxy("PYRONAME:server")
            response = server.logout(self.username)
            print(response)
            
            if response == 'Logout feito com sucesso!':
                # Encerrar o daemon do servidor do cliente
                if self.daemon:
                    self.daemon.shutdown()
                    print(f"Servidor cliente {self.username} encerrado.")
                    
                return True, response
            return False, response
        
        except Exception as e:
            print(f"Erro  ao realizar logout:{str(e)}")
            return False, f"Erro  ao realizar logout:{str(e)}"


    def exibir_perfil(self):
        try:
            server = Pyro5.client.Proxy("PYRONAME:server")
            response = server.exibir_perfil(self.username)
            try:
                data = json.loads(response)
                if isinstance(data, dict):
                    response = data
                else:
                    return False, response
            except json.JSONDecodeError:
                # Se não for JSON, trata como string
                return False, response
            qtd_baralhos = int(response.get('qtd_baralhos'))
            colecao_cartas = response.get('colecao_cartas').split(',')
            baralhos = self.manipular_baralhos(response.get('baralhos'))
            perfil = {
                'colecao_cartas': colecao_cartas,
                'baralhos': baralhos,
                'qtd_baralhos': qtd_baralhos
            }
            return True, perfil
        except Exception as e:
            print(f"Erro  ao exibir o perfil do usuário:{str(e)}")
            return False, f"Erro  ao exibir o perfil do usuário:{str(e)}"


    def adicionar_baralho(self, baralho):
        confirmacao, mensagem = self.__verificar_condicao_baralho(baralho)
        if not confirmacao:
            return confirmacao, mensagem
        try:
            baralho = ",".join(baralho)
            server = Pyro5.client.Proxy("PYRONAME:server")
            response = server.adicionar_baralho(self.username, baralho)
            if response == "Baralho adicionado com sucesso":
                return True, response
            return False, response
        except Exception as e:
            return False, f"Erro  ao adicionar baralho:{str(e)}"


    def excluir_baralho(self, indice):
        try:
            server = Pyro5.client.Proxy("PYRONAME:server")
            response = server.excluir_baralho(self.username, indice)
            if ',' not in response:
                return False, response

            resposta, perfil = response.split(',', 1)

            perfil = ast.literal_eval(perfil)
            qtd_baralhos = int(perfil.get('qtd_baralhos'))
            colecao_cartas = perfil.get('colecao_cartas').split(',')
            baralhos = self.manipular_baralhos(perfil.get('baralhos'))
            perfil = {
                'colecao_cartas': colecao_cartas,
                'baralhos': baralhos,
                'qtd_baralhos': qtd_baralhos
            }

            if resposta == "excluido":
                return True, perfil
            return False, resposta

        except Exception as e:
            print(f"Erro  ao excluir baralho: {str(e)}")
            return False, f"Erro  ao excluir baralho: {str(e)}"

    
    def montar_baralho(self):
        try:
            server = Pyro5.client.Proxy("PYRONAME:server")
            response = server.montar_baralho(self.username)
            if response not in ("Usuário Não Existe", ""):
                colecao_cartas = response.split(',')
                return True, colecao_cartas
            return False, response
        except Exception as e:
            print(f"Erro ao buscar colecao para montar baralho:{str(e)}")
            return False, f"Erro ao buscar colecao para baralho:{str(e)}"


    def exibir_baralhos(self):
        try:
            server = Pyro5.client.Proxy("PYRONAME:server")
            response = server.exibir_baralhos(self.username)
            if response not in ("Usuário ainda não tem baralhos", "Usuário não encontrado."):
                baralhos = self.manipular_baralhos(response)
                return True, baralhos
            return False, response
        except Exception as e:
            print(f"Erro  ao exibir baralhos:{e}")
            return False, f"Erro  ao exibir baralhos:{str(e)}"


    def criar_partida(self, username2, username3):
        try:
            server = Pyro5.client.Proxy("PYRONAME:server")
            server.criar_partida(self.username, username2, username3)
            return f"Tentando Criar Partida"
        except Exception as e:
            print(f"Erro ao tentar criar partida:{str(e)}")
            return f"Erro ao tentar criar partida:{str(e)}"


    def gerar_baralho_aleatorio(self):
        s, info_usuario = self.exibir_perfil()
        colecao = info_usuario['colecao_cartas']
        contador = Counter()
        resultado = []
        total=9
        max_repeticoes=3
        
        while len(resultado) < total:
            emocao = random.choice(colecao)
            
            if contador[emocao] < max_repeticoes:
                resultado.append(emocao)
                contador[emocao] += 1
        
        return resultado
        

    def responder_convite(self, resposta, id_partida):
        server = Pyro5.client.Proxy("PYRONAME:server")
        server.resposta_convite(self.username, id_partida, resposta)
    
    #avisar que jogador já escolheu o baralho, mas servidor não precisa saber qual foi
    def responder_baralho_escolhido(self, id_partida):
        server = Pyro5.client.Proxy("PYRONAME:server")
        server.escolha_baralho(self.username, id_partida)

    def responder_jogada_turno(self, emocao, id_partida):
        server = Pyro5.client.Proxy("PYRONAME:server")
        server.jogada_turno(self.username, emocao, id_partida)

