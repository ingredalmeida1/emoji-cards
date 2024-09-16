import threading
from collections import Counter
import random
import json
from listenServer import ListenServer
import ast

class Client(ListenServer):
    def __init__(self, server_ip="127.0.0.1", server_porta=5000):
        super().__init__(server_ip, server_porta)
        self.colecao = None
        self.baralho_escolhido = None
        self.count_turnos = 0

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
            #lista_baralho.append(self.__adicionar_caminho_cartas(baralho))
            lista_baralho.append(baralho.split(','))
        return lista_baralho


    def criar_conta(self, username, senha):
        try:
            client = self.criar_conexao()
            request = f"criar_conta,{username},{senha}"
            self.enviar_dados(client, request)
            response = self.receber_dados(client)
            if response == "Usuário adicionado com sucesso!":
                self.login(username,senha) #já faz o login do usuário
                return True, response
            return False, response
        except Exception as e:
            print(f"Erro ao criar conta: {str(e)}")
            return False, f"Servidor Indisponível: Reinicie o Sistema!"
        finally:
            if client:
                self.fechar_conexao(client)

    def login(self, username, senha):
        try:
            client = self.criar_conexao()
            request = f"login,{username},{senha}"
            self.enviar_dados(client, request)
            response = self.receber_dados(client)
            port, response = response.split(",")
            if response == "Login feito com sucesso!":
                self.username = username
                client_ip, client_port = client.getsockname()
                client_port = port
                client.close()
                listen_thread = threading.Thread(target=self.handle_server, args=(client_ip, client_port))
                listen_thread.daemon = True
                listen_thread.start()
                return True, response
            return False, response
        except Exception as e:
            self.fechar_conexao(client)
            print(f"Erro ao realizar login:{str(e)}")
            return False, f"Servidor Indisponível: Reinicie o Sistema!"


    def logout(self):
        try:
            client = self.criar_conexao()
            request = f"logout,{self.username}"
            self.enviar_dados(client, request)
            response = self.receber_dados(client)
            if response == 'Logout feito com sucesso!':
                return True, response
            return False, response
        
        except Exception as e:
            print(f"Erro  ao realizar logout:{str(e)}")
            return False, f"Erro  ao realizar logout:{str(e)}"
        finally:
            if client:
                self.fechar_conexao(client)


    def exibir_perfil(self):
        try:
            client = self.criar_conexao()
            request = f"exibir_perfil,{self.username}"
            self.enviar_dados(client, request)
            response = self.receber_dados(client)
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
        finally:
            if client:
                self.fechar_conexao(client)


    def adicionar_baralho(self, baralho):
        confirmacao, mensagem = self.__verificar_condicao_baralho(baralho)
        if not confirmacao:
            return confirmacao, mensagem
        try:
            client = self.criar_conexao()
            baralho = ",".join(baralho)
            request = f"adicionar_baralho,{self.username},{baralho}"
            self.enviar_dados(client, request)
            response = self.receber_dados(client)
            if response == "Baralho adicionado com sucesso":
                return True, response
            return False, response
        except Exception as e:
            return False, f"Erro  ao adicionar baralho:{str(e)}"
        finally:
            if client:
                self.fechar_conexao(client)


    def excluir_baralho(self, indice):
        try:
            client = self.criar_conexao()
            request = f"excluir_baralho,{self.username},{indice}"
            self.enviar_dados(client, request)
            response = self.receber_dados(client)
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
        finally:
            if client:
                self.fechar_conexao(client)

    #Talvez mudar o nome da função para: exibir_colecao; Mais facil identificar
    def montar_baralho(self):
        try:
            client = self.criar_conexao()
            request = f"montar_baralho,{self.username}"
            self.enviar_dados(client, request)
            response = self.receber_dados(client)

            if response not in ("Usuário Não Existe", ""):
                colecao_cartas = response.split(',')
                return True, colecao_cartas
            return False, response
        except Exception as e:
            print(f"Erro ao buscar colecao para montar baralho:{str(e)}")
            return False, f"Erro ao buscar colecao para baralho:{str(e)}"
        finally:
            if client:
                self.fechar_conexao(client)


    def exibir_baralhos(self):
        try:
            client = self.criar_conexao()
            request = f"exibir_baralhos,{self.username}"
            self.enviar_dados(client, request)
            response = self.receber_dados(client)
            if response not in ("Usuário ainda não tem baralhos", "Usuário não encontrado."):
                baralhos = self.manipular_baralhos(response)
                return True, baralhos
            return False, response
        except Exception as e:
            print(f"Erro  ao exibir baralhos:{e}")
            return False, f"Erro  ao exibir baralhos:{str(e)}"
        finally:
            if client:
                self.fechar_conexao(client)


    def criar_partida(self, username2, username3):
        try:
            client = self.criar_conexao()
            request = f"criar_partida,{self.username},{username2},{username3}"
            self.enviar_dados(client, request)
            #response = self.receber_dados(client)
            # if response == "True":
            #     return True
            return f"Tentando Criar Partida"
        except Exception as e:
            print(f"Erro ao tentar criar partida:{str(e)}")
            return f"Erro ao tentar criar partida:{str(e)}"
        finally:
            if client:
                self.fechar_conexao(client)


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
        