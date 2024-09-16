import random
import time
import threading
import socket
import Pyro5.client
import Pyro5.server
import Pyro5.core

online_users = {}
id_partida = -1
partidas = {}

# GERENCIAMENTO DAS REQUISIÇÕES
def criar_conta(username, senha):
    database = Pyro5.client.Proxy("PYRONAME:db-server")
    try: 
        response = database.verificar_username(username)

        if response == 'Username está disponível!':
            cartas_response = database.get_cartas_disponiveis()

            if cartas_response != "Nenhuma Carta Cadastrada":
                vetor_nome_emocoes = cartas_response.split(',')

                if len(vetor_nome_emocoes) >= 9:
                    cartas_sorteadas = random.sample(vetor_nome_emocoes, 9)
                    cartas = ','.join(cartas_sorteadas) 
                else:
                    return "Não há cartas suficientes para criar a conta."
            else:
                return "Nenhuma carta disponível para sortear."
            
            response = database.adicionar_usuario(username,senha,cartas)        
        return response
    
    except Exception as e:
        return f"Erro ao tentar criar conta: {str(e)}"

def login(username, senha):       
    database = Pyro5.client.Proxy("PYRONAME:db-server")
    
    # quando tiver certeza que sempre que usuário sair vai fazer logout
    # response = database.get_status(username)
    # if response == 'online':
    #     return "Você já está logado no sistema!"
            
    try:
        response = database.verificar_login(username,senha) 

        if response == 'Login Correto!':
            online_users[username] = {username}
            status = 'online'
            database.set_status(username,status)
            response = f"Login feito com sucesso!"
        
        else:
            response = f"{response}"

        print("usuarios online:",online_users)
        return response
    
    except Exception as e:
        return f"Erro ao tentar fazer login: {str(e)}"

def logout(username):
    database = Pyro5.client.Proxy("PYRONAME:db-server")
    response = database.get_status(username)

    if response != 'Usuário não encontrado':
        status = 'offline'
        response = database.set_status(username, status)
            
        if username in online_users:
            del online_users[username]

        response = 'Logout feito com sucesso!'
    
    return response

def adicionar_baralho(username, baralho):
    database = Pyro5.client.Proxy("PYRONAME:db-server")

    response  = database.get_qtd_baralhos(username)

    if response != 'Usuário não encontrado':
        qtd_baralhos = int(response)

        if qtd_baralhos == 3:
            response = 'Quantidade máxima de baralhos atingida!'
            return response
            
        response = database.adicionar_baralho(username, baralho)
        
    return response

def excluir_baralho(username, indice):
    database = Pyro5.client.Proxy("PYRONAME:db-server")

    response = database.get_qtd_baralhos(username)

    if response != 'Usuário não encontrado':
        qtd_baralhos = response

        if qtd_baralhos == 0:
            response = 'Não existem baralhos para excluir!'
            return response

        response = database.excluir_baralho(username, indice)
        if response == 'Baralho excluído com sucesso':
                
            response = database.buscar_usuario(username)

            response_atualizada = f'excluido,{response}'

            return response_atualizada
                    
    return response

def adicionar_carta_colecao(username, carta):
    database = Pyro5.client.Proxy("PYRONAME:db-server")

    response = database.adicionar_carta_na_colecao(username, carta)

    return response

def exibir_perfil(username):
    database = Pyro5.client.Proxy("PYRONAME:db-server")

    response = database.buscar_usuario(username)
    
    if response == "Usuário não encontrado":
        return response
    
    try:
        user_data = eval(response)
        filtered_data = {
            'colecao_cartas': user_data.get('colecao_cartas'),
            'baralhos': user_data.get('baralhos'),
            'qtd_baralhos': user_data.get('qtd_baralhos')
        }
        return filtered_data
    
    except Exception as e:
        return f"Erro ao processar a resposta do banco de dados: {str(e)}"
    
def montar_baralho(username):    
    database = Pyro5.client.Proxy("PYRONAME:db-server")

    response = database.get_colecao(username)

    return response

def exibir_baralhos(username):
    database = Pyro5.client.Proxy("PYRONAME:db-server")
    response = database.get_baralhos(username)

    return response
    
def set_status_jogador(username, status):
    database = Pyro5.client.Proxy("PYRONAME:db-server")
    response = database.set_status(username,status)

    return response

def selecionar_atributo():
    database = Pyro5.client.Proxy("PYRONAME:db-server")
    emocoes = []

    try:
        cartas_response = database.get_cartas_disponiveis()
            
        if cartas_response != "Nenhuma Carta Cadastrada":
            emocoes = cartas_response.split(',')

            emocao_aleatoria = random.choice(emocoes)
            
            response = database.get_atributos_carta(emocao_aleatoria)

            if response != 'Carta não existe!':
                dicionario_atributos = eval(response)
                atributo_aleatorio = random.choice(list(dicionario_atributos.keys()))

                return atributo_aleatorio

    except Exception as e:
        return f"erro na seleção de atributo: {str(e)}"

def convidar_jogador(username, host, id_partida):
    database = Pyro5.client.Proxy("PYRONAME:db-server")
    response = database.buscar_usuario(username)

    if response != 'Usuário não encontrado':
        response = database.get_status(username)

        if response == 'online':
            enviar_mensagem(username, f'convite_partida,{host},{id_partida}')

def criar_partida(username_dono, username2, username3):
    database = Pyro5.client.Proxy("PYRONAME:db-server")
    id = gerar_id_partida()

    partidas[id_partida] = {
        'dono': username_dono,
        'turno_atual': 1,
        'pontuacao': {username_dono: 0, username2: 0, username3: 0},
        'atributo_turno': selecionar_atributo(),
        'map_users': {0: username_dono, 1: username2, 2: username3},
        'cartas_ganhas': {username_dono: [], username2: [], username3: []},
        'responses': {},
        'cartas_jogadas_turno': {},
    }

    info_partida = partidas[id]

    def convidar_jogador_thread(username,username_dono,id):
        convidar_jogador(username,username_dono,id)

    threads = []
    for username in [username2, username3]:
        thread = threading.Thread(target=convidar_jogador_thread, args=(username,username_dono,id,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    inicio = time.time()
    fim = inicio
    status = 'jogando'

    while(fim - inicio < 40):
        resposta_esperada = 'aceito'
        usernames = [username2, username3]

        confirmacao_usuarios = get_confirmacao_resposta(info_partida, usernames, resposta_esperada)

        if confirmacao_usuarios:
            break

        fim = time.time() 

    # se um dos jogadores não aceitou
    if info_partida['responses'].get(username2) not in ['aceito']:
        mensagem = f'Erro: não foi possível criar a partida.'
        enviar_mensagem(username_dono, mensagem)
        enviar_mensagem(username3, mensagem)
        usernames = [username2, username_dono, username3]
        finalizar_partida(id_partida, usernames)
        return
        
    if info_partida['responses'].get(username3) not in ['aceito']:
        mensagem = f'Erro: não foi possível criar a partida.'
        enviar_mensagem(username_dono, mensagem)
        enviar_mensagem(username2, mensagem)
        usernames = [username2, username_dono, username3]
        finalizar_partida(id_partida, usernames)
        return
    
    # nenhum dos dois aceitou
    if info_partida['responses'].get(username3) not in ['aceito'] and info_partida['responses'].get(username2) not in ['aceito']:
        mensagem = f'Erro: não foi possível criar a partida.'
        enviar_mensagem(username_dono, mensagem)
        usernames = [username2, username_dono, username3]
        finalizar_partida(id_partida, usernames)
        return

    # se os dois jogadores aceitaram
    usernames = [username_dono, username2, username3]

    for username in usernames:
        user_baralho = database.get_baralhos(username)

        mensagem = f'partida_criada,{id_partida},{user_baralho}'

        enviar_mensagem(username, mensagem)
        set_status_jogador(username, status)
        
    info_partida['responses'] = {}
    iniciar_partida(id_partida, username_dono, username2, username3)


# FUNÇÕES AUXILIARES
def gerar_id_partida():
    global id_partida
    id_partida += 1
    return id_partida

def iniciar_partida(id_partida, username_dono, username2, username3):
    usernames = [username_dono, username2, username3]

    info_partida = partidas[id_partida]
    atributo = info_partida['atributo_turno']

    inicio = time.time()
    fim = inicio

    while(fim - inicio < 40):
        resposta_esperada = 'preparado'
        confirmacao_usuarios = get_confirmacao_resposta(info_partida, usernames, resposta_esperada)
         
        if confirmacao_usuarios:
            break

        fim = time.time()
    
    print("confirmaram a mensagem")
    
    if not confirmacao_usuarios:
        for username in usernames:
            mensagem = 'Erro ao gerenciar a partida'
            enviar_mensagem(username_dono, mensagem) 

        info_partida['responses'] = {}
        finalizar_partida(id_partida, usernames)
        return

    mensagem = f"atributo_turno,{atributo},{id_partida}, {partidas[id_partida]['pontuacao']}"
    print(mensagem)

    for _ in range(7):
        for username in usernames:
            enviar_mensagem(username, mensagem)

        info_partida['responses'] = {}
        mensagem = gerenciar_turno(id_partida)

    for username in usernames:
        enviar_mensagem(username, mensagem)

def gerenciar_turno(id_partida):
    info_partida = partidas[id_partida]

    turno_atual = info_partida['turno_atual']
    atributo_turno = info_partida['atributo_turno']
    lista_usuarios_partida = info_partida['map_users']

    usernames = get_usuarios_partida(lista_usuarios_partida)

    inicio = time.time()
    fim = inicio

    while(fim - inicio < 40):
        resposta_esperada = 'escolheu'
        confirmacao_usuarios = get_confirmacao_resposta(info_partida, usernames, resposta_esperada)

        if confirmacao_usuarios:
            break
    
        fim = time.time()

    if confirmacao_usuarios:
        mensagem = determinar_ganhador_turno(id_partida, atributo_turno, usernames) #=

        if(turno_atual == 7):
            # mensagem = f"fim_turno;{vencedor};{novo_atributo};{id_partida};{cartas_jogadas};{partida['pontuacao']}"
            resultado_turno = mensagem
            resultado_partida = determinar_ganhador_partida(id_partida, usernames)
            if resultado_turno.startswith("fim_turno") and resultado_partida.startswith("fim_partida"):
                _, vencedor_turno, novo_atributo, id_partida, escolhas_cada_jogador, pontuacao = resultado_turno.split(';')
                _, resultado, carta_adicionada = resultado_partida.split(',')
                mensagem = f"fim_partida;{vencedor_turno};{novo_atributo};{id_partida};{escolhas_cada_jogador};{pontuacao};{resultado};{carta_adicionada}"

    else:
        mensagem = 'Erro ao gerenciar a partida'

    info_partida['responses'] = {}
    return mensagem

def cartas_jogadas_turno(id_partida, username, carta):
    partidas[id_partida]['cartas_jogadas_turno'][username] = carta

def determinar_ganhador_turno(id_partida, atributo_turno, usernames):
    database = Pyro5.client.Proxy("PYRONAME:db-server")
    partida = partidas[id_partida]
    atributos_cartas = {}
    cartas_jogadas = partida['cartas_jogadas_turno']
    
    for username in usernames:
        carta = partida['cartas_jogadas_turno'].get(username)
        
        if not carta:
            mensagem = f"Erro: Carta não encontrada para o usuário {username}"
            continue

        try:       
            atributos_response = database.get_atributos_carta(carta)
            
            if atributos_response == "Carta não existe!":
                mensagem = f"Erro: {carta} não existe no banco de dados!"
                continue
            
            atributos_cartas[username] = eval(atributos_response)
        except Exception as e:
            mensagem = f"Erro ao obter atributos da carta {carta} para o usuário {username}: {e}"
            continue
    
    if not atributos_cartas:
        mensagem = "Erro: Não foi possível obter atributos de nenhuma carta."
        return mensagem
    
    vencedor = comparar_atributos(atributos_cartas, atributo_turno)

    if vencedor != 'empate':
        # mensagem = f'fim_turno,empate,none,{atributo_turno},{id_partida}'
    # else:
        partida['pontuacao'][vencedor] += 1
        cartas_outros_jogadores = [cartas_jogadas[user] for user in usernames if user != vencedor]
        carta_ganha = random.choice(cartas_outros_jogadores)
        partida['cartas_ganhas'][vencedor].append(carta_ganha)
        
        carta_vencedor = cartas_jogadas[vencedor]
        # mensagem = f'fim_turno,{vencedor},{carta_vencedor},{atributo_turno},{id_partida}'

    novo_atributo = selecionar_atributo()
    
    mensagem = f"fim_turno;{vencedor};{novo_atributo};{id_partida};{cartas_jogadas};{partida['pontuacao']}"

    set_novo_turno(id_partida)
    partida['atributo_turno'] = novo_atributo

    return mensagem

def determinar_ganhador_partida(id_partida, usernames):
    database = Pyro5.client.Proxy("PYRONAME:db-server")
    info_partida = partidas[id_partida]
    pontuacoes = info_partida['pontuacao']
    max_pontuacao = max(pontuacoes.values())
    vencedores = [user for user, pontuacao in pontuacoes.items() if pontuacao == max_pontuacao]

    if len(vencedores) == 1:
        vencedor = vencedores[0]
        carta_ganhas_vencedor = info_partida['cartas_ganhas'][vencedor]
        carta_adicionada = random.choice(carta_ganhas_vencedor)
        
        try:            
            response = database.adicionar_carta_na_colecao(vencedor,carta_adicionada)
                
            if response != "Carta adicionada com sucesso!":
                raise Exception("Erro ao adicionar carta no banco de dados")
        
        except Exception as e:
            return f"Erro ao adicionar carta no banco de dados: {str(e)}"

        mensagem = f"fim_partida,{vencedor},{carta_adicionada}"
    else:
        mensagem = f"fim_partida,empate,empate"
    
    finalizar_partida(id_partida, usernames)

    return mensagem

def finalizar_partida(id_partida, usernames):
    del partidas[id_partida]

    status = 'online'
    for username in usernames:
        set_status_jogador(username, status)

def enviar_mensagem(username, mensagem):

    print(f'tentando mandar: {mensagem}')

    if username in online_users:
        cliente = Pyro5.client.Proxy(f"PYRONAME:{username}")
        
        cliente.set_mensagem_servidor(mensagem)         
       
        print(f'mensagem "{mensagem}" enviada com sucesso!')

def get_usuarios_partida(lista_usuarios_partida):
    usernames = [username for username in lista_usuarios_partida.values()]
    return usernames

def get_confirmacao_resposta(partida, usernames, resposta_esperada):
    confirmacao = True

    for username in usernames:
        if partida['responses'].get(username, None) != resposta_esperada:
            confirmacao = False
            break

    return confirmacao

def set_resposta_usuario(id_partida, username, resposta):
    partidas[id_partida]['responses'][username] = resposta

def set_novo_turno(id_partida):
    partida = partidas[id_partida]
    turno = partida['turno_atual'] + 1

    partida['cartas_jogadas_turno'] = {}
    partida['turno_atual'] = turno
    partida['responses'] = {}

def comparar_categorico(valor1, valor2, prioridade):
        if valor1 == valor2:
            return 0
        return 1 if prioridade.index(valor1) > prioridade.index(valor2) else -1

def comparar_atributos(atributos_cartas, atributo_turno):
    vencedor = None
    maior_valor = None
    
    for username, atributos in atributos_cartas.items():
        valor = atributos[atributo_turno]

        if atributo_turno == 'intensidade':
            if maior_valor is None or valor > maior_valor:
                maior_valor = valor
                vencedor = username
            elif valor == maior_valor:
                vencedor = 'empate'

        elif atributo_turno == 'tempo':
            prioridade = ["segundos", "minutos", "horas", "dias", "semanas", "meses", "anos"]
            if maior_valor is None or comparar_categorico(valor, maior_valor, prioridade) > 0:
                maior_valor = valor
                vencedor = username
            elif valor == maior_valor:
                vencedor = 'empate'

        elif atributo_turno == 'impacto_social':
            if maior_valor is None or comparar_categorico(valor, maior_valor, ["negativo", "positivo"]) > 0:
                maior_valor = valor
                vencedor = username
            elif valor == maior_valor:
                vencedor = 'empate'

        elif atributo_turno == 'efeito_cognitivo':
            prioridade = ["confusao", "duvida", "clareza", "certeza"]
            if maior_valor is None or comparar_categorico(valor, maior_valor, prioridade) > 0:
                maior_valor = valor
                vencedor = username
            elif valor == maior_valor:
                vencedor = 'empate'

        elif atributo_turno == 'qtd_emocoes_opostas':
            if maior_valor is None or valor < maior_valor:
                maior_valor = valor
                vencedor = username
            elif valor == maior_valor:
                vencedor = 'empate'

        elif atributo_turno == 'qtd_emocoes_relacionadas':
            if maior_valor is None or valor > maior_valor:
                maior_valor = valor
                vencedor = username
            elif valor == maior_valor:
                vencedor = 'empate'

    return vencedor
