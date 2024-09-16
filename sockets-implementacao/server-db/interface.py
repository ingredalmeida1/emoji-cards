#interface intermediária entre servidor e interface direta do banco de dados

from infra.configs.base import Base
from infra.configs.connection import DBConnectionHandler

from  infra.repository.carta_repository import CartaRepository
from  infra.repository.usuario_repository import UsuarioRepository

repoCarta = CartaRepository()
repoUsuario = UsuarioRepository()

def iniciar_banco_dados():
    # criando tabelas (caso ainda não existam)
    Base.metadata.create_all(DBConnectionHandler().get_engine())
    
    #adicionar cartas
    cartas = repoCarta.select_all()
    if len(cartas) == 0: #se ainda nao tem as cartas cadastradas
        repoCarta.add_all_cartas()

# ------------------------------------------------------------------------------------------
# metodos relacionados às cartas
# ------------------------------------------------------------------------------------------
def get_emocoes_cadastradas():
    emocoes_cadastradas = repoCarta.get_emocoes()
    if len(emocoes_cadastradas)>0:
        return True, ','.join(emocoes_cadastradas)
    else:
        return False, "Nenhuma Carta Cadastrada"
    

def get_atributos_carta(emocao):
    carta = repoCarta.get_carta(emocao)
    if carta == None :
        return False, f"Carta não existe!"
    else:
        return True, carta.atributos #string no formato de dicionario

# ------------------------------------------------------------------------------------------
# metodos relacionados aos usuarios
# ------------------------------------------------------------------------------------------
def adicionar_usuario(username, senha, cartas):
    confirmacao, msg = repoUsuario.add_usuario(username, senha, cartas)
    return confirmacao, msg
    '''
    #possibilidades:
    True, "Usuário adicionado com sucesso!"
    False, "Usuário já existe!"
    False, "Erro ao adicionar usuário: {excecao}"
    '''

def verificar_username_existe(username):
    usuario = repoUsuario.get_usuario(username)
    if usuario == None:
        return False, "Username está disponível!" 
    else:
        return True, "Username já existe!"

def verificar_login(username, senha):
    confimacao = repoUsuario.check_login(username, senha)   
    if confimacao:
        return confimacao, "Login Correto!"
    else:
        username_existe, _ = verificar_username_existe(username)
        if username_existe:
            #se o usuario existe, então é a senha que está incorreta
            return confimacao, "Senha Incorreta!"
        else:
            return confimacao, "Username Inválido!"

def buscar_usuario(username):
    usuario = repoUsuario.get_usuario(username)
    if usuario == None:
        return False, "Usuário não encontrado"
    
    usuario_info = { 'username': usuario.username,
                     'status': usuario.status,
                     'colecao_cartas': usuario.colecao_cartas,
                     'qtd_baralhos': usuario.qtd_baralhos,
                     'baralhos': usuario.baralhos
                    }
    
    return True, str(usuario_info)

def get_status(username):
    usuario = repoUsuario.get_usuario(username)
    if usuario == None:
        return False, "Usuário não encontrado"
    else:
        return True, usuario.status
    
def set_status(username, status):
    confirmacao, msg = repoUsuario.set_status(username, status)
    return confirmacao, msg
    '''
    #possibilidades:
    True,"Status atualizado com sucesso!"
    False, "Usuário não encontrado"
    False, "Erro ao atualizar status do usuário: {excecao}"
    '''

def get_colecao(username):
    usuario = repoUsuario.get_usuario(username)
    if usuario == None:
        return False, "Usuário não encontrado"
    else:
        return True, usuario.colecao_cartas #lá no cliente: usuario.colecao_cartas.split(',')

def adicionar_carta_na_colecao(username, emocao):
    confirmacao, msg = repoUsuario.add_carta_na_colecao(username, emocao)
    return confirmacao, msg
    '''
    #possibilidades:
    True, "Carta adicionada com sucesso!"
    False, "Usuário não encontrado"
    False, "Erro ao adicionar carta: {excecao}'
    '''
    
def get_baralhos(username):
    usuario = repoUsuario.get_usuario(username)
    if usuario == None:
        return False, "Usuário não encontrado" 
    else:
        return True, usuario.baralhos #lá no cliente: usuario.colecao_cartas.split('-')

def get_qtd_baralhos(username):
    usuario = repoUsuario.get_usuario(username)
    if usuario == None:
        return False, "Usuário não encontrado" 
    else:
        return True, str(usuario.qtd_baralhos)

def adicionar_baralho(username, baralho):
    #vai adicionar baralho no final da lista, ou seja, no indice 2, considerando 0-1-2
    confirmacao, msg = repoUsuario.add_baralho(username, baralho)
    return confirmacao, msg
    '''
    #possibilidades:
    True, "Baralho adicionado com sucesso"
    False, "Usuário não encontrado"
    False, "Erro ao adicionar baralho: {excecao}"
    '''

def excluir_baralho(username, indice):
    confirmacao, msg = repoUsuario.excluir_baralho(username, int(indice))
    return confirmacao, msg
    '''
    #possibilidades:
    True, "Baralho excluído com sucesso"
    False, "usuário Não Possui Nenhum Baralho"
    False, "Índice do baralho inválido"
    False, "Usuário não encontrado"
    False, "Erro ao excluir baralho: {excecao}"
    '''  

# # testes:
# print('iniciar banco de dados')
# iniciar_banco_dados()

# print('\nemocoes cadastradas:')
# print(get_emocoes_cadastradas())

# print('\natributos de uma carta')
# confirmacao, msg = get_atributos_carta('alivio')
# print(confirmacao, msg)
# confirmacao, msg = get_atributos_carta('teste')
# print(confirmacao, msg)

# print('\nadicionar usuario:')
# confirmacao, msg = adicionar_usuario('lleticiasilvaa', '123456', 'alegria, alivio, amor, ansiedade, autoestima, ciume, culpa, curiosidade, desespero, desgosto, desprezo')
# print(confirmacao, msg)

# print('\nverificar se username existe:')
# confirmacao, msg = verificar_username_existe('lleticiasilvaa')
# print(confirmacao, msg)
# confirmacao, msg = verificar_username_existe('emilylopes')
# print(confirmacao, msg)

# print('\nverificar login:')
# confirmacao, msg = verificar_login('lleticiasilvaa', '123456')
# print(confirmacao, msg)
# confirmacao, msg = verificar_login('lleticiasilvaa', '123')
# print(confirmacao, msg)
# confirmacao, msg = verificar_login('emilylopes', '123456')
# print(confirmacao, msg)

# print('\nbuscar usuario')
# confirmacao, msg = buscar_usuario('lleticiasilvaa')
# print(confirmacao, msg)
# confirmacao, msg = buscar_usuario('emilylopes')
# print(confirmacao, msg)

# print('\nget status')
# confirmacao, msg = get_status('lleticiasilvaa')
# print(confirmacao, msg)
# confirmacao, msg = get_status('emilylopes')
# print(confirmacao, msg)

# print('\nset status')
# confirmacao, msg = set_status('lleticiasilvaa','offline')
# print(confirmacao, msg)
# confirmacao, msg = set_status('emilylopes','jogando')
# print(confirmacao, msg)
# print('confirmar alteracao status')
# confirmacao, msg = buscar_usuario('lleticiasilvaa')
# print(confirmacao, msg)

# print('\nget colecao')
# confirmacao, msg = get_colecao('lleticiasilvaa')
# print(confirmacao, msg)
# confirmacao, msg = get_colecao('emilylopes')
# print(confirmacao, msg)

# print('\nadicionar carta na colecao')
# confirmacao, msg = adicionar_carta_na_colecao('lleticiasilvaa', 'gratidao')
# print(confirmacao, msg)
# confirmacao, msg = adicionar_carta_na_colecao('emilylopes', 'gratidao')
# print(confirmacao, msg)

# print('\nget baralhos')
# confirmacao, msg = get_baralhos('lleticiasilvaa')
# print(confirmacao, msg)
# confirmacao, msg = get_baralhos('emilylopes')
# print(confirmacao, msg)

# print('\nget qtd baralhos')
# confirmacao, msg = get_qtd_baralhos('lleticiasilvaa')
# print(confirmacao, msg)
# confirmacao, msg = get_qtd_baralhos('emilylopes')
# print(confirmacao, msg)

# print('\nadicionar baralho')
# confirmacao, msg = adicionar_baralho('lleticiasilvaa','alegria, alivio, amor, ansiedade, autoestima, ciume, culpa, curiosidade, desespero')
# print(confirmacao, msg)
# confirmacao, msg = adicionar_baralho('emilylopes','alegria, alivio, amor, ansiedade, autoestima, ciume, culpa, curiosidade, desespero')
# print(confirmacao, msg)
# print('\nget baralhos')
# confirmacao, msg = get_baralhos('lleticiasilvaa')
# print(confirmacao, msg)
# print()
# confirmacao, msg = get_baralhos('emilylopes')
# print(confirmacao, msg)
# print()
# print('\nconfirmar alteracao baralho')
# confirmacao, msg = buscar_usuario('lleticiasilvaa')
# print(confirmacao, msg)

# print('\nexcluir baralho')
# confirmacao, msg = excluir_baralho('emilylopes',0)
# print(confirmacao, msg)
# confirmacao, msg = excluir_baralho('emilylopes',2)
# print(confirmacao, msg)

# confirmacao, msg = excluir_baralho('lleticiasilvaa',2)
# print(confirmacao, msg)
# confirmacao, msg = excluir_baralho('lleticiasilvaa',0)
# print(confirmacao, msg)

# print('confirmar alteracao baralho')
# confirmacao, msg = buscar_usuario('lleticiasilvaa')
# print(confirmacao, msg)