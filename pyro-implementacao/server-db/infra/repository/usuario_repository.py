from infra.configs.connection import DBConnectionHandler
from infra.entities.usuario import Usuario

class UsuarioRepository: #vai ser como a interface direta para a tabela Carta
    
    def select_all(self):
        with DBConnectionHandler() as db: #as instanciar o objeto assim:
            #chama o método enter: retorna self, que vai estar em db
            usuarios = db.session.query(Usuario).all()
            return usuarios
            #chama o método exit
    
    #metodo para inserir um novo usuario no banco de dados, se ainda não existir usuŕio com o mesmo username.
    def add_usuario(self, username, senha, cartas): #-> confirmacao, mensagem
        try:  
            with DBConnectionHandler() as db:
                #confere se ainda não existe usuário com mesmo username
                if db.session.query(Usuario).filter_by(username=username).first():
                    return False, 'Usuário já existe!'
                
                novo_usuario = Usuario(username=username, 
                                      senha=senha, 
                                      status='online', 
                                      colecao_cartas=cartas, 
                                      qtd_baralhos=0, 
                                      baralhos='')
                db.session.add(novo_usuario)
                db.session.commit()
                return True, 'Usuário adicionado com sucesso!'
                
        except Exception as e:
            db.session.rollback() #volte o banco ao estado anterior, caso ela tenha sido alterado
            return False, f"Erro ao adicionar usuário: {str(e)}"
    
    #metodo para buscar usuario no banco de dados a partir do username
    def get_usuario(self, username):
         with DBConnectionHandler() as db:
            usuario = db.session.query(Usuario).filter_by(username=username).first()
            return usuario #se retornar None: usuário não existe no banco de dados    
    
    #metodo para verificar se login e senha estão cadastrados no banco e confirmar login
    def check_login(self, username, senha): # -> confirmacao
        with DBConnectionHandler() as db:
            if db.session.query(Usuario).filter_by(username=username, senha=senha).first():
                return True #username existe no banco de dados
            return False    
     
    #metodo para editar o status de um usuario no banco de dados a partir do username 
    def set_status(self, username, status):
        try:
            with DBConnectionHandler() as db:
                usuario = db.session.query(Usuario).filter_by(username=username).first()
                if usuario:
                    usuario.status = status
                    db.session.commit()
                    return True,"Status atualizado com sucesso!"
                return False, "Usuário não encontrado"
        except Exception as e:
            db.session.rollback() #volte o banco ao estado anterior, caso ela tenha sido alterado
            return False, f"Erro ao atualizar status do usuário: {str(e)}"
    
    #metodo para atualizar a colecao de cartas de um usuario no banco de dados a partir do usename 
    def add_carta_na_colecao(self, username, emocao): # -> confirmacao
        try:
            with DBConnectionHandler() as db:
                usuario = db.session.query(Usuario).filter_by(username=username).first()
                if usuario:
                    colecao = usuario.colecao_cartas.split(',') #quebra string que representa a colecao de cartas
                    colecao.append(emocao) #adicionar nome da emocao na colecao de cartas
                    usuario.colecao_cartas = ','.join(colecao) #transforma vetor em string
                    db.session.commit()
                    return True, "Carta adicionada com sucesso!"
                return False, "Usuário não encontrado"
        except Exception as e:
            db.session.rollback() #volte o banco ao estado anterior, caso ela tenha sido alterado
            return False, f"Erro ao adicionar carta: {str(e)}"
    
    #metodo para atualizar os baralhos de um usuario no banco de dados a partir do usename 
    def add_baralho(self, username, baralho):
        try:
            with DBConnectionHandler() as db:
                usuario = db.session.query(Usuario).filter_by(username=username).first()
                if usuario:
                    if usuario.qtd_baralhos == 0:
                        usuario.baralhos = baralho
                    else:
                        baralhos = usuario.baralhos.split('-')
                        baralhos.append(baralho)
                        usuario.baralhos = '-'.join(baralhos)
                        
                    usuario.qtd_baralhos += 1 #atualizar contador 
                    db.session.commit()
                    return True, "Baralho adicionado com sucesso"
                
                return False, "Usuário não encontrado"
        except Exception as e:
            db.session.rollback() #volte o banco ao estado anterior, caso ela tenha sido alterado
            return False, f"Erro ao adicionar baralho: {str(e)}"
    
    #metodo para atualizar os baralhos de um usuario no banco de dados a partir do usename
    def excluir_baralho(self, username, indice):
        try:
            with DBConnectionHandler() as db:
                    usuario = db.session.query(Usuario).filter_by(username=username).first()
                    if usuario:
                        if usuario.qtd_baralhos == 0:
                            return False, "usuário Não Possui Nenhum Baralho"
                        
                        baralhos = usuario.baralhos.split('-')
                        if 0 <= indice < len(baralhos):
                            baralhos.pop(indice)
                            usuario.baralhos = '-'.join(baralhos)
                            usuario.qtd_baralhos -= 1 #atualizar contador 
                            db.session.commit()
                            return True, "Baralho excluído com sucesso"
                        return False, "Índice do baralho inválido"
                    
                    return False, "Usuário não encontrado"
        except Exception as e:
            db.session.rollback() #volte o banco ao estado anterior, caso ela tenha sido alterado
            return False, f"Erro ao excluir baralho: {str(e)}"